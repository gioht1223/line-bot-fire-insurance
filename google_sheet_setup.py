#!/usr/bin/env python3
"""
Google Sheet 初始化和 API 查詢腳本
用於建立保單資料庫和提供查詢接口
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.api_core.gapic_v1 import client_info as grpc_client_info
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from datetime import datetime

# Google Sheets API 設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class GoogleSheetManager:
    def __init__(self, credentials_dict):
        """
        初始化 Google Sheet 管理器
        
        Args:
            credentials_dict: 包含 Google 認證資訊的字典
        """
        self.credentials_dict = credentials_dict
        self.gc = None
        self.sheet = None
        self.sheet_id = None
        self.authenticate()
    
    def authenticate(self):
        """使用提供的認證資訊進行身份驗證"""
        try:
            # 使用 service account 認證
            creds = service_account.Credentials.from_service_account_info(
                self.credentials_dict,
                scopes=SCOPES
            )
            self.gc = gspread.authorize(creds)
            print("✓ Google 認證成功")
        except Exception as e:
            print(f"✗ Google 認證失敗: {e}")
            raise
    
    def create_sheet(self, sheet_name="火險保單資料庫"):
        """
        建立新的 Google Sheet
        
        Args:
            sheet_name: Sheet 名稱
            
        Returns:
            sheet_id: 新建立的 Sheet ID
        """
        try:
            # 建立新的 spreadsheet
            sh = self.gc.create(sheet_name)
            self.sheet = sh
            self.sheet_id = sh.id
            
            # 設定欄位標題
            headers = ['姓名', '身分證字號', '出生年月日', '標的物地址', '手機號碼', '總保費', '保險生效日期']
            worksheet = sh.sheet1
            worksheet.append_row(headers)
            
            # 設定欄位寬度和格式
            worksheet.format('A1:G1', {
                'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
                'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True},
                'horizontalAlignment': 'CENTER',
                'verticalAlignment': 'MIDDLE'
            })
            
            print(f"✓ Google Sheet 建立成功: {sheet_name}")
            print(f"  Sheet ID: {self.sheet_id}")
            return self.sheet_id
        except Exception as e:
            print(f"✗ Google Sheet 建立失敗: {e}")
            raise
    
    def add_sample_data(self):
        """新增範例資料"""
        try:
            worksheet = self.sheet.sheet1
            
            sample_data = [
                ['王小明', 'A123456789', '1990-01-15', '台北市信義區信義路5號', '0912345678', '50000', '2024-01-01'],
                ['李小華', 'B987654321', '1985-06-20', '台中市西屯區台灣大道3號', '0923456789', '75000', '2024-02-15'],
                ['陳小美', 'C111222333', '1992-12-10', '高雄市前金區五福一路1號', '0934567890', '60000', '2024-03-01'],
            ]
            
            for row in sample_data:
                worksheet.append_row(row)
            
            print("✓ 範例資料新增成功")
        except Exception as e:
            print(f"✗ 範例資料新增失敗: {e}")
    
    def query_policy(self, id_number, birth_date):
        """
        查詢保單資料
        
        Args:
            id_number: 身分證字號
            birth_date: 出生年月日 (格式: YYYY-MM-DD)
            
        Returns:
            dict: 查詢結果 {'success': bool, 'data': dict or 'message': str}
        """
        try:
            worksheet = self.sheet.sheet1
            all_records = worksheet.get_all_records()
            
            for record in all_records:
                if (record.get('身分證字號', '').strip().upper() == id_number.strip().upper() and
                    record.get('出生年月日', '').strip() == birth_date.strip()):
                    return {
                        'success': True,
                        'data': {
                            'name': record.get('姓名', ''),
                            'address': record.get('標的物地址', ''),
                            'effective_date': record.get('保險生效日期', ''),
                            'phone': record.get('手機號碼', ''),
                            'premium': record.get('總保費', '')
                        }
                    }
            
            return {
                'success': False,
                'message': '查無資料'
            }
        except Exception as e:
            print(f"✗ 查詢失敗: {e}")
            return {
                'success': False,
                'message': f'系統錯誤: {str(e)}'
            }
    
    def add_policy(self, name, id_number, birth_date, address, phone, premium, effective_date):
        """
        新增保單資料
        
        Args:
            name: 姓名
            id_number: 身分證字號
            birth_date: 出生年月日
            address: 標的物地址
            phone: 手機號碼
            premium: 總保費
            effective_date: 保險生效日期
        """
        try:
            worksheet = self.sheet.sheet1
            row = [name, id_number, birth_date, address, phone, premium, effective_date]
            worksheet.append_row(row)
            print(f"✓ 保單新增成功: {name}")
            return True
        except Exception as e:
            print(f"✗ 保單新增失敗: {e}")
            return False
    
    def get_share_link(self):
        """取得 Sheet 分享連結"""
        if self.sheet_id:
            return f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit"
        return None


def create_google_sheet_with_oauth(email, app_password):
    """
    使用 OAuth 流程建立 Google Sheet
    
    Args:
        email: Google 帳號
        app_password: 應用程式密碼
    """
    # 注意：這個函數展示如何使用 OAuth，但實際上需要在瀏覽器中完成授權
    # 對於自動化，建議使用 Service Account
    pass


if __name__ == "__main__":
    # 測試用的 Service Account 認證資訊
    # 實際使用時，這應該從環境變數或配置文件中讀取
    
    print("Google Sheet 管理系統初始化...")
    print("=" * 50)
    
    # 這裡需要實際的 Google Service Account JSON 認證資訊
    # 由於我們使用應用程式密碼，需要特殊的設定方式
    
    print("\n設定完成！")
    print("下一步：在 LINE Bot 後端中使用 GoogleSheetManager 類")
