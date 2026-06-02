# LINE Bot 火險保單查詢系統 - 部署指南

## 系統架構

```
┌─────────────────────────────────────────────────────────┐
│                    LINE 用戶                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ 訊息
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LINE Official Account                       │
│              (Channel ID: 2010271976)                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Webhook
                     ▼
┌─────────────────────────────────────────────────────────┐
│           LINE Bot 後端服務 (Flask)                      │
│        - 接收 Webhook 訊息                               │
│        - 處理查詢邏輯                                    │
│        - 與 Google Sheet 互動                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API 查詢
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Google Sheet 資料庫                           │
│        (火險保單資料庫)                                  │
│        - 姓名                                            │
│        - 身分證字號                                      │
│        - 出生年月日                                      │
│        - 標的物地址                                      │
│        - 手機號碼                                        │
│        - 總保費                                          │
│        - 保險生效日期                                    │
└─────────────────────────────────────────────────────────┘
```

## 部署步驟

### 第一步：建立 Google Sheet 資料庫

#### 方案 A：使用 Service Account（推薦）

1. **建立 Google Cloud Project**
   - 前往 https://console.cloud.google.com
   - 建立新的 Project（名稱：LINE Bot 火險查詢系統）

2. **啟用 API**
   - 在 API 庫中搜尋並啟用：
     - Google Sheets API
     - Google Drive API

3. **建立 Service Account**
   - 進入「服務帳戶」頁面
   - 建立新的服務帳戶（名稱：line-bot-service）
   - 建立 JSON 金鑰
   - 下載 JSON 檔案並保存

4. **建立 Google Sheet**
   - 在 Google Drive 建立新的試算表
   - 名稱：「火險保單資料庫」
   - 複製 Sheet 的 ID（URL 中的長字符串）
   - 在 Sheet 中分享給 Service Account 的 email
     - 格式：`xxx@xxx.iam.gserviceaccount.com`
     - 權限：編輯者

5. **設定欄位**
   - 第一列添加以下欄位：
     - A: 姓名
     - B: 身分證字號
     - C: 出生年月日
     - D: 標的物地址
     - E: 手機號碼
     - F: 總保費
     - G: 保險生效日期

#### 方案 B：使用 OAuth（如果無法使用 Service Account）

```bash
# 安裝必要套件
pip install google-auth-oauthlib

# 執行設定腳本
python3 setup_google_sheet.py
```

### 第二步：設定 LINE Bot

1. **登入 LINE Official Account Manager**
   - 前往 https://manager.line.biz
   - 選擇你的 LINE@ 帳號

2. **進入開發者設定**
   - 進入「設定」→「開發者」
   - 記錄以下資訊：
     - Channel ID: 2010271976
     - Channel Access Token: 6c4909665e97fddee29ac2f9843eb67c

3. **設定 Webhook**
   - 在「Messaging API 設定」中找到「Webhook 設定」
   - 啟用「使用 Webhook」
   - 設定 Webhook URL（部署後會提供）

### 第三步：部署 LINE Bot 後端服務

#### 方案 A：部署到 Heroku（免費）

1. **安裝 Heroku CLI**
   ```bash
   curl https://cli.heroku.com/install.sh | sh
   ```

2. **登入 Heroku**
   ```bash
   heroku login
   ```

3. **建立 Procfile**
   ```
   web: python3 line_bot_server.py
   ```

4. **建立 requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```

5. **部署**
   ```bash
   heroku create your-app-name
   heroku config:set LINE_CHANNEL_ACCESS_TOKEN="6c4909665e97fddee29ac2f9843eb67c"
   heroku config:set LINE_CHANNEL_SECRET="<你的 Channel Secret>"
   heroku config:set GOOGLE_SHEET_ID="<你的 Sheet ID>"
   heroku config:set GOOGLE_CREDENTIALS_JSON='<JSON 檔案內容>'
   git push heroku main
   ```

6. **取得 Webhook URL**
   ```bash
   heroku apps:info your-app-name
   ```
   Webhook URL 為：`https://your-app-name.herokuapp.com/callback`

#### 方案 B：部署到 Render（推薦）

1. **建立 Render 帳號**
   - 前往 https://render.com

2. **連接 GitHub Repository**
   - 將代碼推送到 GitHub
   - 在 Render 中連接 Repository

3. **建立 Web Service**
   - 選擇 Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python3 line_bot_server.py`

4. **設定環境變數**
   - LINE_CHANNEL_ACCESS_TOKEN
   - LINE_CHANNEL_SECRET
   - GOOGLE_SHEET_ID
   - GOOGLE_CREDENTIALS_JSON

5. **取得 Webhook URL**
   - Render 會提供服務 URL
   - Webhook URL 為：`https://your-service.onrender.com/callback`

#### 方案 C：本地部署（開發用）

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**
   ```bash
   export LINE_CHANNEL_ACCESS_TOKEN="6c4909665e97fddee29ac2f9843eb67c"
   export LINE_CHANNEL_SECRET="<你的 Channel Secret>"
   export GOOGLE_SHEET_ID="<你的 Sheet ID>"
   export GOOGLE_CREDENTIALS_JSON='<JSON 檔案內容>'
   ```

3. **使用 ngrok 暴露本地服務**
   ```bash
   # 安裝 ngrok
   brew install ngrok  # macOS
   # 或
   choco install ngrok  # Windows

   # 啟動 ngrok
   ngrok http 5000
   ```

4. **啟動 Flask 伺服器**
   ```bash
   python3 line_bot_server.py
   ```

5. **設定 Webhook URL**
   - 在 LINE Official Account Manager 中設定
   - Webhook URL：`https://your-ngrok-url.ngrok.io/callback`

### 第四步：測試系統

1. **在 LINE 中新增 LINE@ 帳號為好友**

2. **測試查詢流程**
   - 輸入：「火險保單查詢」
   - 系統應回覆：「請輸入您的身分證字號」
   - 輸入：「A123456789」
   - 系統應回覆：「請輸入您的出生年月日（格式：YYYY-MM-DD，例如：1990-01-15）」
   - 輸入：「1990-01-15」
   - 系統應回覆保單資訊或「查無資料」

3. **測試其他功能**
   - 輸入：「說明」- 查看使用說明
   - 輸入：「專人」- 轉接業務

## 環境變數設定

### 必需的環境變數

```bash
# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN="6c4909665e97fddee29ac2f9843eb67c"
LINE_CHANNEL_SECRET="<你的 Channel Secret>"

# Google Sheet 設定
GOOGLE_SHEET_ID="<你的 Google Sheet ID>"
GOOGLE_CREDENTIALS_JSON='{"type": "service_account", ...}'
```

### 如何取得 Channel Secret

1. 登入 LINE Official Account Manager
2. 進入「設定」→「開發者」
3. 在「Messaging API 設定」中找到「Channel Secret」
4. 複製並設定為環境變數

## 資料庫管理

### 新增保單資料

1. **直接在 Google Sheet 中新增**
   - 打開 Google Sheet
   - 在新的一列中填入保單資訊
   - 系統會自動讀取最新資料

2. **使用 Python 腳本新增**
   ```python
   from google_sheet_setup import GoogleSheetManager
   
   manager = GoogleSheetManager(credentials_dict)
   manager.add_policy(
       name="王小明",
       id_number="A123456789",
       birth_date="1990-01-15",
       address="台北市信義區信義路5號",
       phone="0912345678",
       premium="50000",
       effective_date="2024-01-01"
   )
   ```

### 更新保單資料

- 直接在 Google Sheet 中編輯相應的儲存格
- 系統會自動讀取更新後的資料

### 刪除保單資料

- 在 Google Sheet 中刪除相應的列
- 系統會自動跳過已刪除的資料

## 故障排查

### 問題 1：Webhook 無法連接

**症狀**：LINE 訊息無法觸發 Bot 回覆

**解決方案**：
1. 確認 Webhook URL 正確
2. 確認伺服器正常運行（訪問 `/health` 端點）
3. 檢查 LINE Official Account Manager 中的 Webhook 設定
4. 查看伺服器日誌以獲取更多信息

### 問題 2：Google Sheet 連接失敗

**症狀**：查詢時顯示「系統暫時無法連接資料庫」

**解決方案**：
1. 確認 GOOGLE_SHEET_ID 正確
2. 確認 GOOGLE_CREDENTIALS_JSON 有效
3. 確認 Service Account 有權限訪問 Google Sheet
4. 檢查網絡連接

### 問題 3：查詢結果不正確

**症狀**：輸入正確的身分證字號和出生年月日，但查無資料

**解決方案**：
1. 確認 Google Sheet 中的資料格式正確
2. 檢查身分證字號是否有空格或大小寫問題
3. 確認出生年月日格式為 YYYY-MM-DD
4. 檢查 Google Sheet 中是否真的有該筆資料

## 安全建議

1. **保護敏感資訊**
   - 不要在代碼中硬編碼 Channel Access Token 或 Google 認證資訊
   - 使用環境變數或密鑰管理服務

2. **驗證 Webhook 簽名**
   - 系統已實現簽名驗證
   - 確保只接受來自 LINE 的請求

3. **限制 API 訪問**
   - 定期檢查 Google Sheet 的分享設定
   - 只授予必要的權限

4. **監控日誌**
   - 定期檢查伺服器日誌
   - 監控異常的查詢活動

## 後續改進

1. **新增功能**
   - 保單續期提醒
   - 理賠申請表單
   - 保單修改功能

2. **性能優化**
   - 實現資料快取
   - 使用資料庫而不是 Google Sheet

3. **用戶體驗**
   - 新增 Rich Menu（快速選單）
   - 新增 Flex Message（卡片訊息）
   - 支持更多查詢方式

## 聯絡支持

如有任何問題，請聯絡開發團隊。

---

**最後更新**：2026-06-02
**版本**：1.0.0
