#!/usr/bin/env python3
"""
使用應用程式密碼設定 Google Sheet 的腳本
"""

import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime

def setup_google_sheet_with_app_password(email, app_password):
    """
    使用應用程式密碼建立 Google Sheet
    
    注意：gspread 不直接支援應用程式密碼
    我們需要使用另一種方式
    """
    print("=" * 60)
    print("Google Sheet 設定指南")
    print("=" * 60)
    print()
    print("由於 gspread 不直接支援應用程式密碼，我們需要使用 Service Account。")
    print()
    print("請按照以下步驟操作：")
    print()
    print("步驟 1：建立 Google Cloud Project")
    print("-" * 60)
    print("1. 前往 https://console.cloud.google.com")
    print("2. 建立新的 Project（名稱：LINE Bot 火險查詢系統）")
    print("3. 啟用 Google Sheets API 和 Google Drive API")
    print()
    print("步驟 2：建立 Service Account")
    print("-" * 60)
    print("1. 在 Google Cloud Console 進入「服務帳戶」")
    print("2. 建立新的服務帳戶")
    print("3. 建立 JSON 金鑰")
    print("4. 下載 JSON 檔案")
    print()
    print("步驟 3：在 Google Sheet 中分享給 Service Account")
    print("-" * 60)
    print("1. 建立新的 Google Sheet（名稱：火險保單資料庫）")
    print("2. 複製 Sheet 的 ID（URL 中的長字符串）")
    print("3. 在 Sheet 中分享給 Service Account 的 email")
    print("   （格式：xxx@xxx.iam.gserviceaccount.com）")
    print()
    print("步驟 4：設定環境變數")
    print("-" * 60)
    print("export GOOGLE_SHEET_ID='<你的 Sheet ID>'")
    print("export GOOGLE_CREDENTIALS_JSON='<JSON 檔案內容>'")
    print("export LINE_CHANNEL_ACCESS_TOKEN='<你的 Channel Access Token>'")
    print("export LINE_CHANNEL_SECRET='<你的 Channel Secret>'")
    print()
    print("=" * 60)
    print()


def create_sheet_with_oauth_flow():
    """
    提供 OAuth 流程的替代方案
    """
    print("=" * 60)
    print("使用 OAuth 建立 Google Sheet 的替代方案")
    print("=" * 60)
    print()
    print("如果你想使用 OAuth 而不是 Service Account，請按照以下步驟：")
    print()
    print("1. 安裝必要的套件：")
    print("   pip install google-auth-oauthlib google-auth-httplib2")
    print()
    print("2. 在 Google Cloud Console 建立 OAuth 2.0 認證")
    print("   - 應用程式類型：桌面應用程式")
    print("   - 下載 JSON 認證檔案")
    print()
    print("3. 使用以下程式碼：")
    print()
    print("""
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

gc = gspread.authorize(creds)

# 建立新的 spreadsheet
sh = gc.create('火險保單資料庫')
sheet_id = sh.id
print(f'Sheet ID: {sheet_id}')

# 設定欄位
headers = ['姓名', '身分證字號', '出生年月日', '標的物地址', 
           '手機號碼', '總保費', '保險生效日期']
sh.sheet1.append_row(headers)
    """)
    print()


def create_sample_sheet_locally():
    """
    建立本地範例 Sheet 結構
    """
    print("=" * 60)
    print("本地 Sheet 結構範例")
    print("=" * 60)
    print()
    
    # 建立範例資料
    sample_data = {
        '姓名': ['王小明', '李小華', '陳小美'],
        '身分證字號': ['A123456789', 'B987654321', 'C111222333'],
        '出生年月日': ['1990-01-15', '1985-06-20', '1992-12-10'],
        '標的物地址': ['台北市信義區信義路5號', '台中市西屯區台灣大道3號', '高雄市前金區五福一路1號'],
        '手機號碼': ['0912345678', '0923456789', '0934567890'],
        '總保費': ['50000', '75000', '60000'],
        '保險生效日期': ['2024-01-01', '2024-02-15', '2024-03-01']
    }
    
    # 顯示表格
    print("| 姓名   | 身分證字號   | 出生年月日 | 標的物地址           | 手機號碼    | 總保費 | 保險生效日期 |")
    print("|--------|------------|----------|---------------------|-----------|--------|------------|")
    
    for i in range(len(sample_data['姓名'])):
        row = (f"| {sample_data['姓名'][i]:<6} | "
               f"{sample_data['身分證字號'][i]:<10} | "
               f"{sample_data['出生年月日'][i]:<8} | "
               f"{sample_data['標的物地址'][i]:<17} | "
               f"{sample_data['手機號碼'][i]:<9} | "
               f"{sample_data['總保費'][i]:<6} | "
               f"{sample_data['保險生效日期'][i]:<10} |")
        print(row)
    
    print()


if __name__ == "__main__":
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LINE Bot 火險保單查詢系統 - Google Sheet 設定".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # 顯示設定指南
    setup_google_sheet_with_app_password("gioht1223", "****")
    
    # 顯示 OAuth 替代方案
    print("\n")
    create_sheet_with_oauth_flow()
    
    # 顯示本地範例
    print("\n")
    create_sample_sheet_locally()
    
    print("\n" + "=" * 60)
    print("下一步：")
    print("1. 選擇上述其中一種方式建立 Google Sheet")
    print("2. 記錄 Sheet ID")
    print("3. 設定環境變數")
    print("4. 執行 LINE Bot 伺服器")
    print("=" * 60)
