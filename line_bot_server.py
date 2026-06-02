#!/usr/bin/env python3
"""
LINE Bot 火險保單查詢系統
主要功能：
1. 接收客戶訊息
2. 處理保單查詢請求
3. 與 Google Sheet 資料庫互動
4. 回覆查詢結果
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, PostbackAction,
    MessageAction, URIAction
)
import os
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設定")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Google Sheet 設定
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
GOOGLE_CREDENTIALS = os.environ.get('GOOGLE_CREDENTIALS_JSON')

class PolicyQueryManager:
    """保單查詢管理器"""
    
    def __init__(self, sheet_id, credentials_json):
        """
        初始化查詢管理器
        
        Args:
            sheet_id: Google Sheet ID
            credentials_json: Google 認證 JSON 字符串
        """
        self.sheet_id = sheet_id
        self.gc = None
        self.worksheet = None
        self.user_states = {}  # 追蹤用戶狀態
        
        try:
            if credentials_json:
                creds_dict = json.loads(credentials_json)
                creds = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.gc = gspread.authorize(creds)
                sh = self.gc.open_by_key(sheet_id)
                self.worksheet = sh.sheet1
                logger.info("✓ Google Sheet 連接成功")
        except Exception as e:
            logger.error(f"✗ Google Sheet 連接失敗: {e}")
    
    def query_policy(self, id_number, birth_date):
        """
        查詢保單資料
        
        Args:
            id_number: 身分證字號
            birth_date: 出生年月日 (格式: YYYY-MM-DD 或 YYYY/MM/DD)
            
        Returns:
            dict: 查詢結果
        """
        try:
            if not self.worksheet:
                return {
                    'success': False,
                    'message': '系統暫時無法連接資料庫，請稍後再試'
                }
            
            all_records = self.worksheet.get_all_records()
            
            # 標準化輸入
            id_number = id_number.strip().upper()
            birth_date = birth_date.strip().replace('/', '-')
            
            for record in all_records:
                sheet_id = record.get('身分證字號', '').strip().upper()
                sheet_birth = record.get('出生年月日', '').strip().replace('/', '-')
                
                if sheet_id == id_number and sheet_birth == birth_date:
                    return {
                        'success': True,
                        'data': {
                            'name': record.get('姓名', ''),
                            'address': record.get('標的物地址', ''),
                            'effective_date': record.get('保險生效日期', ''),
                            'phone': record.get('手機號碼', ''),
                            'premium': record.get('總保費', ''),
                            'agent_name': record.get('業務姓名', '')
                        }
                    }
            
            return {
                'success': False,
                'message': '查無資料'
            }
        except Exception as e:
            logger.error(f"查詢失敗: {e}")
            return {
                'success': False,
                'message': '查詢過程中發生錯誤，請稍後再試'
            }
    
    def set_user_state(self, user_id, state):
        """設定用戶狀態"""
        self.user_states[user_id] = state
    
    def get_user_state(self, user_id):
        """取得用戶狀態"""
        return self.user_states.get(user_id, None)
    
    def clear_user_state(self, user_id):
        """清除用戶狀態"""
        if user_id in self.user_states:
            del self.user_states[user_id]


# 初始化查詢管理器
query_manager = PolicyQueryManager(GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS)


@app.route("/callback", methods=['POST'])
def callback():
    """
    LINE Webhook 回調端點
    """
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    logger.info(f"收到 Webhook: {body}")
    
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("無效的簽名")
        abort(400)
    except Exception as e:
        logger.error(f"Webhook 處理錯誤: {e}")
        abort(500)
    
    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    處理文字訊息
    """
    user_id = event.source.user_id
    message_text = event.message.text.strip()
    
    logger.info(f"用戶 {user_id} 訊息: {message_text}")
    
    # 檢查用戶目前狀態
    user_state = query_manager.get_user_state(user_id)
    
    # 狀態機制
    if message_text == "火險保單查詢":
        # 開始查詢流程
        query_manager.set_user_state(user_id, "waiting_id")
        reply_message = TextSendMessage(
            text="請輸入您的身分證字號"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    
    elif user_state == "waiting_id":
        # 等待身分證字號
        query_manager.set_user_state(user_id, {"state": "waiting_birth", "id": message_text})
        reply_message = TextSendMessage(
            text="請輸入您的出生年月日（格式：YYYY-MM-DD，例如：1990-01-15）"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    
    elif isinstance(user_state, dict) and user_state.get("state") == "waiting_birth":
        # 等待出生年月日，進行查詢
        id_number = user_state.get("id")
        birth_date = message_text
        
        # 執行查詢
        result = query_manager.query_policy(id_number, birth_date)
        
        if result['success']:
            data = result['data']
            reply_text = (
                f"✓ 查詢成功\n\n"
                f"姓名：{data['name']}\n"
                f"標的物地址：{data['address']}\n"
                f"保險生效日期：{data['effective_date']}\n"
                f"手機號碼：{data['phone']}\n"
                f"總保費：{data['premium']}\n"
                f"業務姓名：{data['agent_name']}"
            )
        else:
            reply_text = (
                f"查無資料\n\n"
                f"如需進一步協助，請輸入「專人」，"
                f"將由業務協助查詢"
            )
        
        reply_message = TextSendMessage(text=reply_text)
        line_bot_api.reply_message(event.reply_token, reply_message)
        query_manager.clear_user_state(user_id)
    
    elif message_text == "專人":
        # 轉接業務
        reply_message = TextSendMessage(
            text="感謝您的查詢。我們的業務人員將盡快與您聯絡，請稍候..."
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
        query_manager.clear_user_state(user_id)
        
        # 可以在這裡新增通知業務的邏輯
        logger.info(f"用戶 {user_id} 要求轉接業務")


@app.route("/health", methods=['GET'])
def health_check():
    """健康檢查端點"""
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}


@app.route("/", methods=['GET'])
def index():
    """首頁"""
    return {
        'name': 'LINE Bot 火險保單查詢系統',
        'version': '1.0.0',
        'status': 'running'
    }


if __name__ == '__main__':
    # 開發環境
    app.run(host='0.0.0.0', port=5000, debug=False)
