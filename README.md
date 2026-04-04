# 🛠️ 自動化評測系統 (Task Automation)

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Category](https://img.shields.io/badge/Task-Automation-orange.svg)

> 🔍 一套用於自動比對 Python 程式輸出、模擬輸入、並進行批改流程自動化的工具

---

## 📌 專案介紹

本專案為一個 **自動化程式評測系統**，專門用於：

* 比對「正解程式」與「學生程式」輸出
* 自動模擬輸入資料
* 判斷 PASS / FAIL
* 自動整理與管理檔案

👉 適合：

* 程式教學批改
* 題庫練習
* 自動化測試流程

---

## 🚀 核心特色

### 🔹 自動輸出比對

* 精準比對兩份程式輸出
* 支援逐行差異顯示（Debug友善）

### 🔹 輸入模擬系統

* 自動記錄使用者輸入
* 重放輸入給學生程式（確保公平測試）

### 🔹 檔案自動管理

* ✅ PASS：

  * 刪除正解檔
  * 學生檔重新命名為 `_checkedOK.py`
* ❌ FAIL：

  * 保留所有檔案並顯示錯誤差異

### 🔹 題型支援

* 一般輸入題（stdin）
* 檔案讀寫題（自動同步 `.txt`）

---

## ⚙️ 技術亮點

* `importlib`：動態載入 Python 檔案
* `StringIO`：模擬輸入/輸出流
* 自動輸出攔截與比對
* CLI 互動式流程設計
* 檔案系統操作（rename / remove / copy）

---

## 🧪 執行流程

```text
1. 選擇題型（是否需讀寫檔案）
2. 選擇正解與學生檔
3. 執行正解（記錄輸入）
4. 套用輸入執行學生程式
5. 比對輸出結果
6. 顯示 PASS / FAIL 並處理檔案
```

---

## 📦 安裝套件

### 主要套件

本專案使用 Python 標準函式庫，無需額外安裝第三方套件

### 套件版本（實際使用）

* Python 3.10+（建議）

### 執行環境

* OS：Windows / macOS / Linux
* 執行方式：CLI（Command Line）

---

## 📂 專案結構

```text
.
├── .venv/               # 虛擬環境
├── .gitignore           # Git 過濾設定
├── README.md            # 本說明文件
├── omni_executor.py     # 核心評測主程式
└── transfer/            # 待測檔案緩衝區
    └── .gitkeep         # 保持目錄結構
```

---

## ▶️ 使用方式

### 1️⃣ 準備測試檔案

將以下檔案放入 `transfer/`：

* 正解程式（answer.py）
* 學生程式（student.py）
* 測試資料（.txt，如需要）

---

### 2️⃣ 執行系統

```bash
python omni_executor.py
```

---

### 3️⃣ 操作流程

* 選擇題型（是否有檔案輸入）
* 指定正解與學生程式
* 系統自動執行並比對

---

## 📊 輸出範例

### ✅ PASS

```
***** 比較結果：完全一致 (PASS) *****
```

### ❌ FAIL

```
第 3 行差異：
  正解: '10'
  學生: '8'
```

---

## 🧠 設計理念

本專案核心目標為：

> **將「人工批改程式」流程轉換為自動化系統（Task Automation）**

透過：

* 輸入模擬
* 自動比對
* 檔案管理

達到：

* 減少人工作業
* 提高批改效率
* 降低錯誤率

---

## 🏷️ 專案標籤

* Task Automation
* CLI Tool
* Python Tooling
* Code Evaluation System

---

## 📈 未來優化方向

* GUI 介面（PyQt / Web）
* 批次多檔評測
* 成績報表輸出（CSV / DB）
* Docker 化部署
* Web API 化

---

## 👨‍💻 作者

> Developed as a portfolio project for automation & system design
> 專注於提升程式批改流程效率 🚀
