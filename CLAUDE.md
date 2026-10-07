# CLAUDE.md

本檔案為 Claude Code 在此子資料夾工作時的指引。此資料夾**本身是獨立 git 儲存庫**，不受根目錄工作區規則約束（除語言等全域偏好）。

## 這是什麼

**企業數位轉型分析**（公司版），單檔前端、無後端、無序號授權。2026-10-07 依使用者要求「現在的版本是針對個人，把目標對象改成公司，製作一個新的版本，不要跟原來版本混在一起」建置。

- 個人版是 `資料儀表板/personal-digital-workplace-analyzer/`（已上線），**兩者完全獨立**：不同資料夾、repo、port、localStorage 前綴（本版 `companyDigital*`，個人版 `digitalWorkplace*`）、圖示（本版深藍「企」）、測試 hook（本版 `window.__coDigital`，個人版 `__digiWork`）。改其中一個不要順手改另一個，除非使用者要求兩邊同步。
- 程式骨架與個人版相同（範例卡＋我的公司、設定說明框、部門＝categories、流程＝tasks、組織評估＝skills、驗算、優先矩陣、BYOK AI＋規則式、PDF、CSV、跑馬燈、PWA、長說明預設收合）。內部變數名沿用 tasks／categories／skills，語意改為流程／部門／組織構面。

### 與個人版的差異

| 個人版 | 公司版 |
|---|---|
| 月薪＋工時 → 時薪 | 平均每月人事成本／人（含雇主負擔）＋每月工時 → **平均人時成本**；新增 `employees` 員工總數 |
| 任務：次數 × 分鐘 | 流程：**`people` 參與人數** × 每人每週次數 × 分鐘 → 週人時 |
| 工具月費、學習時數 | 系統月費 `toolCost`、**一次性導入費 `setupCost`**、每人訓練時數 `learnHours` |
| 每月釋放價值／月淨效益／學習回本 | **年度節省人力成本**、系統年費、**年度淨效益**、一次性投入（導入費＋訓練人時 × 人時成本）、**投資回收期**、**三年淨效益**、**相當全職人力 FTE**（可釋放人時 ÷ 每週標準工時）、占員工總數 % |
| 工具月預算 | **年度數位化預算** vs 首年支出（導入費＋系統年費；訓練時間不算現金） |
| 回本 ≤3 月 good、≤6 warn | 回收期 ≤12 月 good、≤24 warn、其餘 bad |
| 盤點涵蓋率（任務工時 ÷ 個人標準工時） | 流程人時 ÷（員工 × 標準工時），只在 >100% 時提醒；「每週標準工時」卡改講 FTE 換算 |
| 數位職能自評 8 項 | 組織數位成熟度評估 8 構面：數位策略與領導、流程標準化、雲端與協作基礎、資料管理與分析、自動化程度、資安與治理、員工數位技能、客戶數位體驗 |
| 我的職位 | 我的公司（JSON 匯出 app 欄位為 `company-digital-transformation-analyzer`） |

規則式健檢以 0–3 個月速贏／3–12 個月重點投資排序；速贏流程若系統月費高於省下成本，會改提示「先改用現有工具或較低方案」。驗算 20 項檢查（含 FTE、年度數字、一次性投入、首年支出、計算步驟與 KPI 一致）。

## 10 組產業範例（全虛構，已用 `scripts/preset_model.py` 與 Playwright 核對一致）

| # | 範例 | 週人時 | 可釋放 | 年淨效益 | 回收期 | 成熟度 | 示範狀態 |
|---|---|---|---|---|---|---|---|
| 0 | 會計師事務所 | 50.0 | 10.6 | 120,650 | 3.4 月 | 63.9 | 健康基準，無警示、無資料提醒 |
| 1 | 貿易公司 | 59.7 | 27.8 | 406,517 | 3.0 月 | 29.3 | Excel／Email 作業多，速贏 2 |
| 2 | 製造業工廠 | 78.5 | 44.6 | 471,620 | 15.2 月 | 17.2 | 3＋2 手工警示，重點投資 ERP／條碼 |
| 3 | 連鎖零售 | 85.2 | 34.9 | 341,567 | 11.1 月 | 39.9 | 門市盤點最耗人力 |
| 4 | 餐飲連鎖 | 49.3 | 28.2 | 260,830 | 5.4 月 | 17.1 | 2＋1 手工警示 |
| 5 | 物流倉儲 | 93.9 | 53.0 | 465,423 | 19.3 月 | 10.6 | 成熟度最低、FTE 最多 1.32 |
| 6 | 診所 | 35.7 | 13.5 | 126,355 | 8.0 月 | 36.4 | 預約提醒衛教為速贏 |
| 7 | 補習班 | 43.7 | 19.8 | 172,800 | 2.6 月 | 25.2 | 點名通知、批改為速贏 |
| 8 | 電商品牌 | 45.7 | 9.8 | −83,556 | 無法回收 | 69.3 | 系統年費 > 節省成本、首年支出超預算 |
| 9 | 營建工程 | 52.4 | 26.4 | 219,542 | 40.6 月 | 18.9 | 投資大、回收期最長 |

改範例：`index.html` 的 `PRESETS` 與 `scripts/preset_model.py` 同步改，跑 `python scripts/preset_model.py`，再在 console 執行 `__coDigital.applyPreset(i)` 確認 `#verifyTitle` 為 ✅。

## 踩坑（沿用個人版經驗）

- 驗算不可拿獨立驗算值比 `toFixed()` 文字（浮點跨四捨五入邊界會誤報）；數值用容差比對、文字比對 `calculate()` 的同一個值。
- 說明框與「更多說明」是 `<details>`，預設收合，但裡面的即時內容仍會渲染，驗算照常讀取。
- PDF 驗證用 Playwright `emulateMedia({media:'print'})`＋`page.pdf()`，不要真的點列印按鈕。

## localStorage

`companyDigitalState`、`companyDigitalApiConfig`、`companyDigitalActivePreset`、`companyDigitalCustomPresets`、`companyDigitalCustomDirty`、`companyDigitalMarquee`。

## 指令

無建置步驟（index.html 直接編輯）。預覽：port `8827`（根目錄 `.claude/launch.json` 的 `company-digital-transformation-analyzer`），或 `python -m http.server 8827 --directory 資料儀表板/company-digital-transformation-analyzer`。

## 部署

2026-10-07 依使用者指示推公開 repo <https://github.com/M255525/company-digital-transformation-analyzer>，GitHub Pages（Actions workflow 模式，push 到 master 自動部署）：<https://m255525.github.io/company-digital-transformation-analyzer/>。

踩坑：這次先開 Pages 再推第一個 commit，`github-pages` environment 的部署分支規則只預設允許 `main`，push 觸發的部署被拒（"Branch master is not allowed to deploy"）。已用 `gh api -X POST repos/<repo>/environments/github-pages/deployment-branch-policies -f name=master -f type=branch` 補上 master。
