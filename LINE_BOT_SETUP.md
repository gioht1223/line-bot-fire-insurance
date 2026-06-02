# LINE Bot 設定完整指南

## 概述

本指南將幫助你完成 LINE@ 帳號的開發者設定，並將其與 LINE Bot 後端服務整合。

## 前置要求

- 已建立的 LINE@ 帳號
- LINE Official Account Manager 的存取權限
- 已建立的 Google Sheet 資料庫

## 設定步驟

### 步驟 1：確認 LINE@ 帳號資訊

1. 登入 [LINE Official Account Manager](https://manager.line.biz)
2. 選擇你的 LINE@ 帳號
3. 記錄以下資訊：
   - **Channel ID**：2010271976（已提供）
   - **帳號名稱**：（用於識別）

### 步驟 2：啟用 Messaging API

1. 在 LINE Official Account Manager 中，進入「設定」
2. 找到「開發者」或「Messaging API」選項
3. 如果還未啟用，點擊「啟用 Messaging API」
4. 系統會提示建立 Channel

### 步驟 3：取得 Channel Access Token

1. 在 LINE Official Account Manager 中，進入「設定」→「開發者」
2. 在「Messaging API 設定」區域，找到「Channel access token」
3. 如果還沒有，點擊「發行」按鈕
4. 複製 Channel Access Token
   - 格式：`6c4909665e97fddee29ac2f9843eb67c`
5. **妥善保管**，不要分享給他人

### 步驟 4：取得 Channel Secret

1. 在同一頁面中，找到「Channel Secret」
2. 複製 Channel Secret
3. **妥善保管**

### 步驟 5：設定 Webhook

#### 5.1 啟用 Webhook

1. 在「Messaging API 設定」中，找到「Webhook 設定」
2. 點擊「編輯」
3. 在「Webhook URL」欄位中，輸入你的 Webhook URL
   - 本地開發：`https://your-ngrok-url.ngrok.io/callback`
   - 生產環境：`https://your-domain.com/callback`
4. 點擊「驗證」確認 URL 有效
5. 啟用「使用 Webhook」開關
6. 啟用「Webhook 重新傳遞」開關（可選但推薦）

#### 5.2 設定 Webhook 事件

1. 在「Messaging API 設定」中，找到「Webhook 事件設定」
2. 確保以下事件已啟用：
   - ✅ 訊息事件（Message Event）
   - ✅ 追蹤事件（Follow Event）
   - ✅ 取消追蹤事件（Unfollow Event）

### 步驟 6：設定自動回覆

1. 在 LINE Official Account Manager 中，進入「設定」→「自動回覆」
2. 根據需要設定自動回覆訊息
3. 建議設定：
   - **歡迎訊息**：「歡迎使用火險保單查詢系統，請輸入『火險保單查詢』開始查詢」
   - **預設回覆**：「感謝您的訊息，我們會盡快回覆」

### 步驟 7：設定快速選單（Rich Menu）

1. 在 LINE Official Account Manager 中，進入「設定」→「快速選單」
2. 點擊「建立」
3. 設定以下按鈕：
   - **按鈕 1**：「火險保單查詢」
   - **按鈕 2**：「使用說明」
   - **按鈕 3**：「聯絡業務」
4. 設定每個按鈕的動作為「傳送文字」
5. 點擊「發佈」

### 步驟 8：設定環境變數

在部署 LINE Bot 後端服務時，設定以下環境變數：

```bash
export LINE_CHANNEL_ACCESS_TOKEN="6c4909665e97fddee29ac2f9843eb67c"
export LINE_CHANNEL_SECRET="<你的 Channel Secret>"
export GOOGLE_SHEET_ID="<你的 Google Sheet ID>"
export GOOGLE_CREDENTIALS_JSON='<Google Service Account JSON>'
```

## 驗證設定

### 測試 Webhook 連接

1. 在 LINE Official Account Manager 中，進入「設定」→「開發者」
2. 在「Messaging API 設定」中，找到「Webhook 設定」
3. 點擊「驗證」按鈕
4. 如果顯示「成功」，表示連接正常

### 測試 LINE Bot

1. 在 LINE 中新增你的 LINE@ 帳號為好友
2. 輸入測試訊息：「火險保單查詢」
3. 確認 Bot 有正確回覆

## 常見問題

### Q: Webhook 驗證失敗怎麼辦？

A: 
1. 確認 Webhook URL 正確
2. 確認伺服器正常運行（可訪問 `/health` 端點）
3. 檢查防火牆設定
4. 查看伺服器日誌以獲取更多信息

### Q: 無法取得 Channel Access Token？

A:
1. 確認已啟用 Messaging API
2. 確認帳號有足夠的權限
3. 嘗試重新登入 LINE Official Account Manager

### Q: 如何更新 Channel Access Token？

A:
1. 在「Messaging API 設定」中，找到「Channel access token」
2. 點擊「重新發行」
3. 舊的 Token 會失效，新的 Token 會立即生效
4. 更新環境變數並重新部署

### Q: 如何撤銷 Webhook 設定？

A:
1. 在「Webhook 設定」中，清空 Webhook URL
2. 禁用「使用 Webhook」開關
3. 系統會停止發送 Webhook 請求

## 安全建議

1. **保護 Channel Secret**
   - 不要在代碼中硬編碼
   - 使用環境變數管理
   - 定期輪換

2. **驗證 Webhook 簽名**
   - 系統已實現簽名驗證
   - 確保只接受來自 LINE 的請求

3. **監控 API 使用**
   - 定期檢查 LINE Official Account Manager 的統計數據
   - 監控異常的訊息活動

4. **限制 API 調用**
   - 實現速率限制
   - 防止濫用

## 進階設定

### 設定 Rich Menu（快速選單）

Rich Menu 提供更好的用戶體驗，允許用戶通過按鈕快速執行操作。

```python
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, PostbackAction, MessageAction

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 建立 Rich Menu
rich_menu = RichMenu(
    size=RichMenuBounds(width=2800, height=1686),
    selected=True,
    name="主選單",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1400, height=1686),
            action=MessageAction(label="火險保單查詢", text="火險保單查詢")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1400, y=0, width=1400, height=1686),
            action=MessageAction(label="使用說明", text="說明")
        )
    ]
)

# 建立 Rich Menu
rich_menu_id = line_bot_api.create_rich_menu(rich_menu)
print(f"Rich Menu ID: {rich_menu_id}")

# 設定為預設 Rich Menu
line_bot_api.set_default_rich_menu(rich_menu_id)
```

### 設定 Flex Message（卡片訊息）

Flex Message 提供更豐富的訊息格式。

```python
from linebot.models import FlexMessage, FlexContainer

flex_message = FlexMessage(
    alt_text="保單資訊",
    contents=FlexContainer(
        type="bubble",
        body={
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "保單資訊",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "地址",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "台北市信義區信義路5號",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    )
)
```

## 下一步

完成 LINE Bot 設定後，請：

1. 部署 LINE Bot 後端服務
2. 設定 Webhook URL
3. 測試系統功能
4. 監控性能和錯誤

詳見 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 參考資源

- [LINE Messaging API 官方文件](https://developers.line.biz/en/docs/messaging-api/)
- [LINE Official Account Manager](https://manager.line.biz)
- [LINE Developers](https://developers.line.biz)

---

**最後更新**：2026-06-02
