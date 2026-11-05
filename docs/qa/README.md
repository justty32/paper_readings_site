# 2026-11-05 驗證

- 靜態：41頁、28課、10分類，全部本地連結與錨點、正文引用、45個固定已讀筆記路徑通過。
- 瀏覽器：Windows Chrome headless，獨立使用者資料目錄及CDP連接埠，沒有開啟可見視窗或佔用鍵盤焦點。
- 1440px／390px：41頁逐頁無橫向溢位、互動空白或JavaScript例外，共82個版面檢查。
- 28課：實際點擊每個互動按鈕、調整各旋鈕／選項，確認有效解釋與無執行錯誤。
- 功能：主題搜尋及無結果狀態、閱讀勾選跨頁保存、清除勾選、選答回饋、停用JavaScript的靜態例子。
- 額外：320px KAN抽查、Space鍵開啟原生details。

詳細執行紀錄在 [browser-report.json](browser-report.json)。代表截圖：首頁桌面／手機、I類總覽、ARC手機、符號迴歸首屏及互動區、工具呼叫手機、智能體記憶展開細節。

可重現：先啟動本地靜態伺服器及一個獨立headless瀏覽器，再執行：

```sh
SITE_URL=http://127.0.0.1:8778/ BROWSER_CDP_URL=http://127.0.0.1:9335 node tools/browser_qa.mjs
```

本機沒有Linux Chrome執行所需的libnspr4，因此使用已安裝Windows Chrome的headless模式。未安裝新瀏覽器，未操作使用者原有分頁。

內容驗證依固定快照的已讀筆記，不宣稱重讀45篇全部原PDF。主線已實際覆核子線正文與來源卡，另回讀世界模型定理假設、Ratchet退役與非發散條件、TTT資料邊界等易過度推論處。所有圖與玩具均標示合成／教學，沒有拿玩具結果當論文效能。arXiv原文入口未做45篇批次HTTP壓力檢查；GitHub筆記連結的commit與路徑已用Git物件逐一核實。
