# 發布紀錄

- 主 repo：`justty32/paper_readings_site`，private。
- Sites project：`appgprj_6aec267962c88191abdb9f7f91d81d1d`，本輪建立，預設 owner-private；未放寬觀眾。
- 預期網址：`https://paper-readings-playground.justty32.chatgpt.site`。此欄僅為目標，成功與版本待本輪發布後記錄。
- 網站來源固定於 paper_readings `1f91be9`；網站程式版本與論文來源版本為不同概念。

發布步驟：重建HTML→靜態檢查→JavaScript語法→瀏覽器驗證→產生dist→Sites helper以stdin接收暫時憑證、提交推送並封裝→儲存版本與private部署→核實成功狀態→推送GitHub main。憑證不可落檔或回顯。
