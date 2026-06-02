# 快速開始指南

## 5 分鐘快速設定

### 第一步：準備資訊（1 分鐘）

收集以下資訊：
- ✅ LINE Channel ID：`2010271976`
- ✅ LINE Channel Access Token：`6c4909665e97fddee29ac2f9843eb67c`
- ⏳ LINE Channel Secret：（需要從 LINE Official Account Manager 取得）
- ⏳ Google Sheet ID：（建立 Google Sheet 後取得）
- ⏳ Google Service Account JSON：（建立 Service Account 後取得）

### 第二步：建立 Google Sheet（2 分鐘）

**快速方式：**

1. 前往 [Google Drive](https://drive.google.com)
2. 新增 → Google 試算表
3. 命名為「火險保單資料庫」
4. 在第一列添加欄位：
   - A1: 姓名
   - B1: 身分證字號
   - C1: 出生年月日
   - D1: 標的物地址
   - E1: 手機號碼
   - F1: 總保費
   - G1: 保險生效日期

5. 複製 Sheet ID（URL 中的長字符串）

### 第三步：設定環境變數（1 分鐘）

```bash
# 建立 .env 檔案
cp .env.example .env

# 編輯 .env 檔案，填入以下資訊：
# LINE_CHANNEL_ACCESS_TOKEN=6c4909665e97fddee29ac2f9843eb67c
# LINE_CHANNEL_SECRET=<你的 Channel Secret>
# GOOGLE_SHEET_ID=<你的 Sheet ID>
# GOOGLE_CREDENTIALS_JSON=<Google Service Account JSON>
```

### 第四步：部署（1 分鐘）

**選擇一種部署方式：**

#### 方式 A：本地開發（使用 ngrok）

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 啟動伺服器
python3 line_bot_server.py

# 3. 在另一個終端中啟動 ngrok
ngrok http 5000

# 4. 複製 ngrok URL（例如：https://xxxx-xx-xxx-xxx.ngrok.io）

# 5. 在 LINE Official Account Manager 中設定 Webhook URL
# Webhook URL: https://xxxx-xx-xxx-xxx.ngrok.io/callback
```

#### 方式 B：部署到 Render（推薦）

```bash
# 1. 推送代碼到 GitHub
git push origin main

# 2. 在 Render 中建立 Web Service
# - 選擇 Python
# - Build Command: pip install -r requirements.txt
# - Start Command: python3 line_bot_server.py

# 3. 設定環境變數
# - LINE_CHANNEL_ACCESS_TOKEN
# - LINE_CHANNEL_SECRET
# - GOOGLE_SHEET_ID
# - GOOGLE_CREDENTIALS_JSON

# 4. 複製 Render 服務 URL
# Webhook URL: https://your-service.onrender.com/callback
```

#### 方式 C：部署到 Heroku

```bash
# 1. 登入 Heroku
heroku login

# 2. 建立應用
heroku create your-app-name

# 3. 設定環境變數
heroku config:set LINE_CHANNEL_ACCESS_TOKEN="6c4909665e97fddee29ac2f9843eb67c"
heroku config:set LINE_CHANNEL_SECRET="<你的 Channel Secret>"
heroku config:set GOOGLE_SHEET_ID="<你的 Sheet ID>"
heroku config:set GOOGLE_CREDENTIALS_JSON='<JSON>'

# 4. 部署
git push heroku main

# 5. 取得 Webhook URL
heroku apps:info your-app-name
# Webhook URL: https://your-app-name.herokuapp.com/callback
```

### 第五步：測試（1 分鐘）

1. 在 LINE 中新增你的 LINE@ 帳號為好友
2. 輸入：「火險保單查詢」
3. 輸入身分證字號：「A123456789」
4. 輸入出生年月日：「1990-01-15」
5. 確認系統返回保單資訊

## 常見問題

### Q: 我沒有 Google Service Account，怎麼辦？

A: 參考 [GOOGLE_SHEET_SETUP.md](GOOGLE_SHEET_SETUP.md) 中的「方案 B：使用 OAuth 2.0」

### Q: Webhook 無法連接？

A: 
1. 確認伺服器正常運行
2. 確認 Webhook URL 正確
3. 在 LINE Official Account Manager 中點擊「驗證」

### Q: 查詢無法返回結果？

A:
1. 確認 Google Sheet 中有資料
2. 確認身分證字號和出生年月日格式正確
3. 檢查伺服器日誌

## 下一步

- 📖 閱讀 [README.md](README.md) 了解完整功能
- 🔧 參考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 了解詳細部署
- 📊 參考 [GOOGLE_SHEET_SETUP.md](GOOGLE_SHEET_SETUP.md) 了解 Google Sheet 設定
- 💬 參考 [LINE_BOT_SETUP.md](LINE_BOT_SETUP.md) 了解 LINE Bot 設定

## 需要幫助？

如有任何問題，請查看相應的詳細指南或聯絡開發團隊。

---

**最後更新**：2026-06-02
