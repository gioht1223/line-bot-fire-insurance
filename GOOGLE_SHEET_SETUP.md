# Google Sheet 設定完整指南

## 概述

本指南將幫助你建立 Google Sheet 資料庫並與 LINE Bot 整合。

## 方案選擇

### 方案 A：使用 Service Account（推薦）

**優點**：
- 自動化程度高
- 安全性好
- 支持 API 調用
- 適合生產環境

**缺點**：
- 設定步驟較多
- 需要 Google Cloud 帳號

### 方案 B：使用 OAuth 2.0

**優點**：
- 設定相對簡單
- 使用個人 Google 帳號
- 不需要 Google Cloud Project

**缺點**：
- 需要手動授權
- 不適合完全自動化

## 詳細步驟

### 方案 A：Service Account 設定

#### 步驟 1：建立 Google Cloud Project

1. 前往 [Google Cloud Console](https://console.cloud.google.com)
2. 點擊頂部的「選擇專案」
3. 點擊「新增專案」
4. 輸入專案名稱：`LINE Bot 火險查詢系統`
5. 點擊「建立」
6. 等待專案建立完成

#### 步驟 2：啟用必要的 API

1. 在 Google Cloud Console 中，進入「API 和服務」
2. 點擊「啟用 API 和服務」
3. 搜尋並啟用以下 API：
   - **Google Sheets API**
   - **Google Drive API**

#### 步驟 3：建立 Service Account

1. 在 Google Cloud Console 中，進入「服務帳戶」
2. 點擊「建立服務帳戶」
3. 填入以下資訊：
   - **服務帳戶名稱**：`line-bot-service`
   - **服務帳戶 ID**：自動生成
   - **服務帳戶說明**：`LINE Bot 火險查詢系統服務帳戶`
4. 點擊「建立並繼續」
5. 在「授予此服務帳戶存取專案的權限」中，跳過此步驟
6. 點擊「完成」

#### 步驟 4：建立 JSON 金鑰

1. 在「服務帳戶」頁面中，找到剛建立的服務帳戶
2. 點擊該服務帳戶
3. 進入「金鑰」標籤
4. 點擊「新增金鑰」→「建立新金鑰」
5. 選擇「JSON」
6. 點擊「建立」
7. JSON 檔案會自動下載，**妥善保管**

#### 步驟 5：建立 Google Sheet

1. 前往 [Google Drive](https://drive.google.com)
2. 點擊「新增」→「Google 試算表」
3. 輸入名稱：`火險保單資料庫`
4. 建立完成後，複製 URL 中的 Sheet ID
   - URL 格式：`https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
   - 複製 `{SHEET_ID}` 部分

#### 步驟 6：分享 Google Sheet 給 Service Account

1. 打開 Google Sheet
2. 點擊右上角的「分享」
3. 在分享對話框中，輸入 Service Account 的 email
   - 格式：`line-bot-service@{PROJECT_ID}.iam.gserviceaccount.com`
   - 可以在 Google Cloud Console 的服務帳戶頁面找到
4. 選擇權限為「編輯者」
5. 點擊「分享」

#### 步驟 7：設定 Google Sheet 欄位

1. 打開 Google Sheet
2. 在第一列中添加以下欄位標題：
   - A1: `姓名`
   - B1: `身分證字號`
   - C1: `出生年月日`
   - D1: `標的物地址`
   - E1: `手機號碼`
   - F1: `總保費`
   - G1: `保險生效日期`

3. 格式化標題列（可選）：
   - 選擇第一列
   - 設定背景色為深灰色
   - 設定文字顏色為白色
   - 設定為粗體

#### 步驟 8：添加範例資料

在 Google Sheet 中添加以下範例資料：

| 姓名 | 身分證字號 | 出生年月日 | 標的物地址 | 手機號碼 | 總保費 | 保險生效日期 |
|------|----------|----------|---------|---------|--------|-----------|
| 王小明 | A123456789 | 1990-01-15 | 台北市信義區信義路5號 | 0912345678 | 50000 | 2024-01-01 |
| 李小華 | B987654321 | 1985-06-20 | 台中市西屯區台灣大道3號 | 0923456789 | 75000 | 2024-02-15 |
| 陳小美 | C111222333 | 1992-12-10 | 高雄市前金區五福一路1號 | 0934567890 | 60000 | 2024-03-01 |

#### 步驟 9：設定環境變數

1. 打開下載的 JSON 檔案
2. 複製整個 JSON 內容
3. 設定以下環境變數：

```bash
export GOOGLE_SHEET_ID="<你複製的 Sheet ID>"
export GOOGLE_CREDENTIALS_JSON='<JSON 檔案內容>'
```

### 方案 B：OAuth 2.0 設定

#### 步驟 1：建立 OAuth 2.0 認證

1. 前往 [Google Cloud Console](https://console.cloud.google.com)
2. 進入「API 和服務」→「認證」
3. 點擊「建立認證」→「OAuth 用戶端 ID」
4. 選擇「桌面應用程式」
5. 輸入名稱：`LINE Bot 火險查詢系統`
6. 點擊「建立」
7. 下載 JSON 檔案

#### 步驟 2：使用 OAuth 建立 Google Sheet

```python
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive']

# 第一次運行時會打開瀏覽器進行授權
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
```

#### 步驟 3：保存認證信息

```python
import pickle

# 保存 credentials 以供後續使用
with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)
```

## 驗證設定

### 測試 Service Account 連接

```python
import gspread
from google.oauth2.service_account import Credentials
import json

# 讀取 JSON 檔案
with open('service_account.json', 'r') as f:
    creds_dict = json.load(f)

# 建立認證
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# 連接 gspread
gc = gspread.authorize(creds)

# 打開 Google Sheet
sh = gc.open_by_key('YOUR_SHEET_ID')
print(f"✓ 連接成功：{sh.title}")

# 讀取資料
records = sh.sheet1.get_all_records()
print(f"✓ 讀取成功，共 {len(records)} 筆記錄")
```

### 測試查詢功能

```python
# 查詢特定保單
id_number = "A123456789"
birth_date = "1990-01-15"

for record in records:
    if (record['身分證字號'] == id_number and 
        record['出生年月日'] == birth_date):
        print(f"✓ 查詢成功")
        print(f"  姓名：{record['姓名']}")
        print(f"  地址：{record['標的物地址']}")
        print(f"  生效日期：{record['保險生效日期']}")
        break
else:
    print("✗ 查無資料")
```

## 常見問題

### Q: 如何更新 Google Sheet 中的資料？

A: 直接在 Google Sheet 中編輯，系統會自動讀取最新資料。

### Q: 如何新增新的保單？

A: 在 Google Sheet 中新增一列，填入保單資訊即可。

### Q: 如何刪除保單？

A: 在 Google Sheet 中刪除相應的列。

### Q: Service Account 金鑰洩露怎麼辦？

A: 立即在 Google Cloud Console 中刪除該金鑰，並建立新的金鑰。

### Q: 如何限制 Service Account 的權限？

A: 在 Google Cloud Console 中設定 IAM 角色，只授予必要的權限。

## 安全建議

1. **保護 JSON 金鑰**
   - 不要將 JSON 檔案提交到 Git
   - 使用 `.gitignore` 排除敏感檔案
   - 定期輪換金鑰

2. **限制 Google Sheet 分享**
   - 只分享給必要的 Service Account
   - 定期檢查分享設定

3. **監控 API 使用**
   - 在 Google Cloud Console 中監控 API 使用情況
   - 設定配額警告

4. **使用環境變數**
   - 不要在代碼中硬編碼敏感資訊
   - 使用 `.env` 檔案管理環境變數

## 下一步

完成 Google Sheet 設定後，請：

1. 記錄 Sheet ID
2. 記錄 Service Account email（如使用 Service Account）
3. 設定環境變數
4. 部署 LINE Bot 後端服務

詳見 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**最後更新**：2026-06-02
