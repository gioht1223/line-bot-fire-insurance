# 部署檢查清單

## 部署前準備

### 第一步：收集必要資訊

- [ ] **LINE Channel ID**：2010271976
- [ ] **LINE Channel Access Token**：6c4909665e97fddee29ac2f9843eb67c
- [ ] **LINE Channel Secret**：從 LINE Official Account Manager 取得
- [ ] **Google Sheet ID**：建立 Google Sheet 後取得
- [ ] **Google Service Account JSON**：建立 Service Account 後下載

### 第二步：建立 Google Sheet

- [ ] 前往 Google Drive 建立新試算表
- [ ] 命名為「火險保單資料庫」
- [ ] 複製 Sheet ID
- [ ] 添加欄位：
  - [ ] A: 姓名
  - [ ] B: 身分證字號
  - [ ] C: 出生年月日
  - [ ] D: 標的物地址
  - [ ] E: 手機號碼
  - [ ] F: 總保費
  - [ ] G: 保險生效日期
- [ ] 添加至少一筆範例資料
- [ ] 分享給 Service Account

### 第三步：設定環境變數

- [ ] 複製 `.env.example` 為 `.env`
- [ ] 填入 `LINE_CHANNEL_ACCESS_TOKEN`
- [ ] 填入 `LINE_CHANNEL_SECRET`
- [ ] 填入 `GOOGLE_SHEET_ID`
- [ ] 填入 `GOOGLE_CREDENTIALS_JSON`

### 第四步：本地測試

- [ ] 安裝依賴：`pip install -r requirements.txt`
- [ ] 執行測試：`python3 test_system.py`
- [ ] 確認所有測試通過
- [ ] 本地啟動伺服器：`python3 line_bot_server.py`
- [ ] 確認伺服器正常運行

## 部署方式選擇

### 選項 A：本地開發（使用 ngrok）

- [ ] 安裝 ngrok
- [ ] 啟動 ngrok：`ngrok http 5000`
- [ ] 複製 ngrok URL
- [ ] 在 LINE Official Account Manager 中設定 Webhook URL
- [ ] 驗證 Webhook 連接
- [ ] 在 LINE 中測試

### 選項 B：部署到 Render（推薦）

- [ ] 建立 GitHub Repository
- [ ] 推送代碼到 GitHub
- [ ] 在 Render 中建立 Web Service
- [ ] 選擇 Python 環境
- [ ] 設定 Build Command：`pip install -r requirements.txt`
- [ ] 設定 Start Command：`python3 line_bot_server.py`
- [ ] 設定環境變數：
  - [ ] LINE_CHANNEL_ACCESS_TOKEN
  - [ ] LINE_CHANNEL_SECRET
  - [ ] GOOGLE_SHEET_ID
  - [ ] GOOGLE_CREDENTIALS_JSON
- [ ] 部署服務
- [ ] 複製服務 URL
- [ ] 在 LINE Official Account Manager 中設定 Webhook URL
- [ ] 驗證 Webhook 連接
- [ ] 在 LINE 中測試

### 選項 C：部署到 Heroku

- [ ] 建立 Heroku 帳號
- [ ] 安裝 Heroku CLI
- [ ] 登入 Heroku：`heroku login`
- [ ] 建立應用：`heroku create your-app-name`
- [ ] 設定環境變數：
  - [ ] `heroku config:set LINE_CHANNEL_ACCESS_TOKEN="..."`
  - [ ] `heroku config:set LINE_CHANNEL_SECRET="..."`
  - [ ] `heroku config:set GOOGLE_SHEET_ID="..."`
  - [ ] `heroku config:set GOOGLE_CREDENTIALS_JSON='...'`
- [ ] 部署：`git push heroku main`
- [ ] 取得 Webhook URL：`heroku apps:info your-app-name`
- [ ] 在 LINE Official Account Manager 中設定 Webhook URL
- [ ] 驗證 Webhook 連接
- [ ] 在 LINE 中測試

### 選項 D：使用 Docker

- [ ] 安裝 Docker
- [ ] 建立 `.env` 檔案
- [ ] 啟動容器：`docker-compose up -d`
- [ ] 確認容器正常運行：`docker-compose logs`
- [ ] 設定 Webhook URL（根據你的域名）
- [ ] 驗證 Webhook 連接
- [ ] 在 LINE 中測試

## 部署後驗證

### Webhook 驗證

- [ ] 在 LINE Official Account Manager 中點擊「驗證」
- [ ] 確認顯示「成功」
- [ ] 檢查伺服器日誌

### 功能測試

- [ ] 在 LINE 中新增 LINE@ 帳號為好友
- [ ] 輸入「火險保單查詢」
- [ ] 確認系統回覆「請輸入您的身分證字號」
- [ ] 輸入測試身分證號碼（例如：A123456789）
- [ ] 確認系統回覆「請輸入您的出生年月日」
- [ ] 輸入測試出生年月日（例如：1990-01-15）
- [ ] 確認系統返回保單資訊
- [ ] 測試「查無資料」情況
- [ ] 測試「專人」轉接功能
- [ ] 測試「說明」幫助功能

### 性能測試

- [ ] 測試查詢響應時間（應 < 2 秒）
- [ ] 測試多個用戶同時查詢
- [ ] 檢查伺服器日誌中是否有錯誤

### 安全檢查

- [ ] 確認敏感資訊未在代碼中硬編碼
- [ ] 確認使用 HTTPS（生產環境）
- [ ] 確認 Webhook 簽名驗證已啟用
- [ ] 檢查 Google Sheet 分享設定
- [ ] 確認 Service Account 權限受限

## 部署後維護

### 日常維護

- [ ] 定期檢查伺服器日誌
- [ ] 監控 API 使用情況
- [ ] 檢查 Google Sheet 資料完整性
- [ ] 確認 Webhook 連接正常

### 定期更新

- [ ] 每月檢查一次依賴更新
- [ ] 定期輪換 API 金鑰
- [ ] 備份 Google Sheet 資料
- [ ] 檢查系統性能指標

### 故障排查

- [ ] 如果 Webhook 無法連接，檢查：
  - [ ] Webhook URL 是否正確
  - [ ] 伺服器是否正常運行
  - [ ] 防火牆設定是否允許
  - [ ] 伺服器日誌中的錯誤

- [ ] 如果查詢無法返回結果，檢查：
  - [ ] Google Sheet 中是否有資料
  - [ ] 身分證字號和出生年月日格式是否正確
  - [ ] Google Sheet 連接是否正常
  - [ ] Service Account 權限是否足夠

- [ ] 如果伺服器性能下降，檢查：
  - [ ] 是否有大量並發請求
  - [ ] Google Sheet API 配額是否超限
  - [ ] 伺服器資源使用情況
  - [ ] 是否需要實施快取

## 部署完成

- [ ] 所有測試通過
- [ ] Webhook 連接正常
- [ ] 功能測試成功
- [ ] 性能測試通過
- [ ] 安全檢查完成
- [ ] 文檔更新完成
- [ ] 團隊培訓完成
- [ ] 上線公告發布

## 部署日期

- **計劃部署日期**：_______________
- **實際部署日期**：_______________
- **部署人員**：_______________
- **驗證人員**：_______________

## 備註

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

**部署檢查清單版本**：1.0.0
**最後更新**：2026-06-02
