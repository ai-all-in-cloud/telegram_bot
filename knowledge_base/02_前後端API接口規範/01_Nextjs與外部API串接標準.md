# 🔌 Next.js 與外部 API 跨領域協作標準規範

> **協作對象**：001 柚木 (前端/規劃)、002 柚水 (後端/核心)、004 柚土 (測試驗證)

---

## 📦 標準 API 響應結構 (JSON Envelope)

所有 API 端點（無論成功或異常）均應統一遵循下列標準結構：

### 成功回應範例 (HTTP 200)
```json
{
  "success": true,
  "data": {
    "orderId": "ORD-20261005-001",
    "amount": 1580,
    "status": "PAID"
  },
  "timestamp": "2026-10-05T22:00:00.000Z"
}
```

### 錯誤回應範例 (HTTP 400 / 401 / 500)
```json
{
  "success": false,
  "error": {
    "code": "STOCK_INSUFFICIENT",
    "message": "門市庫存不足，無法完成扣減"
  },
  "timestamp": "2026-10-05T22:00:00.000Z"
}
```

---

## 🛡️ 安全防護與 Header 驗證準則
1. **多租戶辨識**：所有請求需帶入或由中間件注入 `x-store-id` 與 `x-store-vip-id`。
2. **防爬蟲保護**：內部或非公開路由需帶有 `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet`。
3. **錯誤攔截 (Error Boundary)**：前端需具備標準 Try-Catch 與 Toast 提示，不可直接噴出空白或未捕獲的 Promise 錯誤。
