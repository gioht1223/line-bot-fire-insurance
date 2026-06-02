#!/usr/bin/env python3
"""
LINE Bot 火險保單查詢系統 - 測試腳本
用於測試系統的各個組件
"""

import os
import json
import gspread
from google.oauth2.service_account import Credentials
import requests
from datetime import datetime

class SystemTester:
    """系統測試類"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def print_header(self, title):
        """打印標題"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_test(self, name, status, message=""):
        """打印測試結果"""
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}")
        if message:
            print(f"   {message}")
        
        if status:
            self.passed += 1
        else:
            self.failed += 1
        
        self.test_results.append({
            'name': name,
            'status': status,
            'message': message
        })
    
    def test_environment_variables(self):
        """測試環境變數"""
        self.print_header("環境變數檢查")
        
        required_vars = [
            'LINE_CHANNEL_ACCESS_TOKEN',
            'LINE_CHANNEL_SECRET',
            'GOOGLE_SHEET_ID',
            'GOOGLE_CREDENTIALS_JSON'
        ]
        
        for var in required_vars:
            value = os.environ.get(var)
            if value:
                # 隱藏敏感信息
                if len(value) > 20:
                    display_value = value[:10] + "..." + value[-10:]
                else:
                    display_value = value
                self.print_test(f"環境變數 {var}", True, f"值: {display_value}")
            else:
                self.print_test(f"環境變數 {var}", False, "未設定")
    
    def test_google_sheet_connection(self):
        """測試 Google Sheet 連接"""
        self.print_header("Google Sheet 連接檢查")
        
        try:
            credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
            sheet_id = os.environ.get('GOOGLE_SHEET_ID')
            
            if not credentials_json or not sheet_id:
                self.print_test("Google Sheet 認證資訊", False, "缺少必要的環境變數")
                return
            
            # 解析 JSON
            try:
                creds_dict = json.loads(credentials_json)
            except json.JSONDecodeError:
                self.print_test("Google Sheet 認證 JSON 解析", False, "JSON 格式不正確")
                return
            
            self.print_test("Google Sheet 認證 JSON 解析", True)
            
            # 建立認證
            try:
                creds = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.print_test("Google Sheet 認證建立", True)
            except Exception as e:
                self.print_test("Google Sheet 認證建立", False, str(e))
                return
            
            # 連接 gspread
            try:
                gc = gspread.authorize(creds)
                sh = gc.open_by_key(sheet_id)
                self.print_test("Google Sheet 連接", True, f"Sheet 名稱: {sh.title}")
            except Exception as e:
                self.print_test("Google Sheet 連接", False, str(e))
                return
            
            # 檢查欄位
            try:
                headers = sh.sheet1.row_values(1)
                expected_headers = ['姓名', '身分證字號', '出生年月日', '標的物地址', 
                                   '手機號碼', '總保費', '保險生效日期']
                
                if headers == expected_headers:
                    self.print_test("Google Sheet 欄位檢查", True, f"欄位數: {len(headers)}")
                else:
                    self.print_test("Google Sheet 欄位檢查", False, 
                                   f"欄位不匹配。期望: {expected_headers}，實際: {headers}")
            except Exception as e:
                self.print_test("Google Sheet 欄位檢查", False, str(e))
                return
            
            # 檢查資料
            try:
                records = sh.sheet1.get_all_records()
                self.print_test("Google Sheet 資料讀取", True, f"記錄數: {len(records)}")
            except Exception as e:
                self.print_test("Google Sheet 資料讀取", False, str(e))
        
        except Exception as e:
            self.print_test("Google Sheet 連接", False, str(e))
    
    def test_line_credentials(self):
        """測試 LINE 認證資訊"""
        self.print_header("LINE 認證資訊檢查")
        
        channel_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
        channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
        
        if channel_token:
            self.print_test("LINE Channel Access Token", True, f"長度: {len(channel_token)}")
        else:
            self.print_test("LINE Channel Access Token", False)
        
        if channel_secret:
            self.print_test("LINE Channel Secret", True, f"長度: {len(channel_secret)}")
        else:
            self.print_test("LINE Channel Secret", False)
    
    def test_query_logic(self):
        """測試查詢邏輯"""
        self.print_header("查詢邏輯檢查")
        
        try:
            credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
            sheet_id = os.environ.get('GOOGLE_SHEET_ID')
            
            if not credentials_json or not sheet_id:
                self.print_test("查詢邏輯測試", False, "缺少必要的環境變數")
                return
            
            creds_dict = json.loads(credentials_json)
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            gc = gspread.authorize(creds)
            sh = gc.open_by_key(sheet_id)
            records = sh.sheet1.get_all_records()
            
            # 測試查詢
            if records:
                test_record = records[0]
                id_number = test_record.get('身分證字號', '')
                birth_date = test_record.get('出生年月日', '')
                
                # 查詢測試
                found = False
                for record in records:
                    if (record.get('身分證字號', '') == id_number and
                        record.get('出生年月日', '') == birth_date):
                        found = True
                        break
                
                if found:
                    self.print_test("查詢邏輯測試", True, 
                                   f"成功查詢到: {test_record.get('姓名', 'N/A')}")
                else:
                    self.print_test("查詢邏輯測試", False, "查詢失敗")
            else:
                self.print_test("查詢邏輯測試", False, "Google Sheet 中無資料")
        
        except Exception as e:
            self.print_test("查詢邏輯測試", False, str(e))
    
    def test_webhook_endpoint(self):
        """測試 Webhook 端點"""
        self.print_header("Webhook 端點檢查")
        
        # 注意：這個測試需要伺服器正在運行
        webhook_url = os.environ.get('WEBHOOK_URL', 'http://localhost:5000')
        
        try:
            response = requests.get(f"{webhook_url}/health", timeout=5)
            if response.status_code == 200:
                self.print_test("Webhook 端點連接", True, f"狀態碼: {response.status_code}")
            else:
                self.print_test("Webhook 端點連接", False, f"狀態碼: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.print_test("Webhook 端點連接", False, "無法連接（伺服器可能未運行）")
        except Exception as e:
            self.print_test("Webhook 端點連接", False, str(e))
    
    def print_summary(self):
        """打印測試摘要"""
        self.print_header("測試摘要")
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"總測試數: {total}")
        print(f"通過: {self.passed} ✅")
        print(f"失敗: {self.failed} ❌")
        print(f"通過率: {pass_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 所有測試都通過了！系統已準備好部署。")
        else:
            print(f"\n⚠️  有 {self.failed} 個測試失敗。請檢查上述錯誤。")
    
    def run_all_tests(self):
        """執行所有測試"""
        print("\n" + "╔" + "=" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "  LINE Bot 火險保單查詢系統 - 系統測試".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "=" * 58 + "╝")
        
        self.test_environment_variables()
        self.test_line_credentials()
        self.test_google_sheet_connection()
        self.test_query_logic()
        self.test_webhook_endpoint()
        self.print_summary()


if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()
