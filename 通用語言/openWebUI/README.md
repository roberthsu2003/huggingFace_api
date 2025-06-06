# Open WebUI

## 模組 1：基礎認識與安裝

### 1. 什麼是 Open WebUI？
Open WebUI 是一款開源的自託管人工智慧平台，提供類似 ChatGPT 的圖形化使用者介面。使用者可在本地或雲端環境中，與大型語言模型（LLMs）互動。它支援多種模型執行器，如 Ollama 及與 OpenAI API 相容的服務，並設計為可完全離線運作，非常適合對資料隱私與安全性有高度要求的應用場景。

---

## 模組 2：Open WebUI 的主要特色與優勢

- 開源、免費且可自訂
- 資料隱私與安全性高
- 支援多種模型
  - OpenAI GPT-4/3.5
  - Ollama 本地模型
  - OpenRouter（支援 Claude、Gemini、Mixtral 等）

---

### 3. 安裝 Open WebUI（本地端 & 雲端）

#### 3.1 本地安裝

```bash
docker run -d --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

- `docker run`：執行一個 Docker 容器
- `-d`：讓容器在背景執行（detached mode），終端機可繼續操作
- `--network=host`：
  - 使用主機網路模式，將容器網路與主機網路綁定
  - 適用於本機（Host）上有 Ollama 模型執行器（如 http://127.0.0.1:11434）時，容器內的 Open WebUI 可直接存取
  - 注意：在 Mac 或 Windows 的 Docker Desktop 上，`--network=host` 可能有限制
- `-v open-webui:/app/backend/data`：
  - 建立名為 open-webui 的 Docker 卷（volume）
  - 將 `/app/backend/data` 目錄資料持久化，避免容器刪除後資料遺失
- `-e OLLAMA_BASE_URL=http://127.0.0.1:11434`：
  - 設定環境變數，指定 Open WebUI 呼叫 Ollama API 的位置
  - 預設 Ollama 埠為 11434
- `--name open-webui`：為容器命名，方便後續管理
- `ghcr.io/open-webui/open-webui:main`：指定 Docker 映像檔位置，`:main` 代表主分支最新版本

#### 3.2 雲端安裝

3.2.1 選擇雲端平台（如 GCP、AWS、Azure、Vultr 等）  
3.2.2 建立一台 Linux VM（建議 Ubuntu 20.04 以上版本）  
3.2.3 安裝 Docker：

```bash
sudo apt update
sudo apt install docker.io
```

3.2.4 執行 Docker 指令（同本地端）  
3.2.5 設定防火牆或安全群組，開放 3000 埠對外連線

---

#### 4. 初始設定

4.1 帳號註冊與登入（請務必記住帳號與密碼）

4.2 模型提供者設定  
- Ollama 連線設定
- 支援 OpenAI API 格式的連線
  - 例如 OpenRouter 連線格式：`https://openrouter.ai/api/v1`

![](./images/pic1.png)

4.3 測試模型（可同時測試多個模型）

![](./images/pic2.png)

---

## 模組 3：基礎使用與管理

1. **筆記功能（Notes）**  
   讓你在與模型互動時，將特定回答或輸入「標記」並儲存於可管理的區塊，猶如筆記。這對教學、研究或專案紀錄特別有幫助。

2. **臨時對話（Temporary Chat）**  
   此功能強化隱私保護與資料合規性。啟用後，對話內容不會被永久儲存，適合處理敏感資訊或避免留下紀錄的情境。

3. **工作區 → 模型**  
   可建立自訂名稱的模型（如：寫程式、翻譯、寫文章等專用模型）

4. **工作區 → 知識區**  
   可上傳相關文件，讓模型依據文件內容進行搜尋與回答

5. **工作區 → 提示詞**  
   建立預設的 Prompt，方便快速使用

6. **網頁搜尋（Web Search）**  
   - 需啟用網頁搜尋選項
   - 申請 Google Programmable Search Engine
   - 需填入 Google PSE 引擎 ID 與 API 金鑰（申請時請選擇 Programmatic access）
   - 每日 10,000 次免費請求

   ![金鑰申請需選擇 Programmatic access](./images/pic4.png)

   ![](./images/pic3.png)

7. **聲音（Audio）**  
   - 預設畫面可直接使用語音功能
   - 支援 TTS 語音模型：Kokoro TTS（輕量級開源語音模型，支援中文）

     > 深入了解 Kokoro TTS，這款僅 8200 萬參數卻表現優異的文字轉語音模型。特別推薦最新的中文模型 Kokoro-82M-v1.1-zh，以及其安裝與整合方式。[相關介紹](https://www.communeify.com/tw/blog/kokoro-tts-lightweight-open-source-text-to-speech-model-complete-guide)

     > [Kokoro TTS 安裝與整合至 Open WebUI](./kokoro.md)

8. **OpenWebUI 社群**  
   - 需註冊 OpenWebUI 官方網站帳戶

---

## 模組 4：與模型的互動

1. **支援中文模型**：
   - LLaMA
   - Gemma
   - Mistral
   - CodeGemma（專為程式設計）

2. **如何連接及呼叫 LLM（如 GPT、LLaMA）**
   - 以 OpenRouter 為例：`https://openrouter.ai/api/v1`

3. **基本 Prompt 工具及使用方式**

4. **聊天及問答系統的建立**

5. **互動式應用開發**（如：問答、資料摘要、翻譯等）

---

## 模組 5：進階應用開發

1. 整合 API（串接外部資源）
2. 使用 Plugins 擴充功能
3. 客製化回應與 Prompt 工程（Prompt Engineering）
4. 多模態應用（如結合圖片、語音等）

---

## 模組 6：專題與實作

1. 設計完整應用案例（如 AI 客服、文件問答系統）
2. 根據實際需求設計 Prompt 流程
3. 簡易部署與展示

---

## **應用方向建議**

- **教育輔助**：建置問答系統，供學生自學或課堂互動
- **知識管理**：建立文件摘要、搜尋與問答功能
- **客戶服務**：開發簡易客服機器人，協助回答常見問題
- **資料分析**：結合大語言模型進行資料解讀與分析
- **語言學習**：搭配多語言模型，支援翻譯、語法解釋等
- **程式教學**：利用 Prompt 協助解釋程式碼、示範範例

---
