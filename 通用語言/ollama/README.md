## 使用ollama和openWebUI

1. [安裝Docker](#安裝Docker)
2. [本機安裝Ollama](#本機安裝Ollama)
3. [docker安裝Ollama](#docker安裝Ollama)
4. [docker安裝OpenWebUI](#docker安裝OpenWebUI)
5. [requests連結ollama](#requests連結ollama)
6. [requests連結ollama_generate_mode](#requests連結ollama_generate_mode)
7. [requests連結chat_mode](#requests連結chat_mode)
8. [連接gradio的介面呼叫ollama的api](#連接gradio的介面呼叫ollama的api)

<a name="安裝Docker"></a>
### 1. 安裝Docker
- https://docs.docker.com/get-started/get-docker/
---
<a name="本機安裝Ollama"></a>
### 2. 本機安裝Ollama
- 優點:會直接使用Mac的GPU,無GPU自動使用CPU
- [ollama官網](https://ollama.com)
- ollama支援的模型,請參考ollam的官網

**2.1 Ollama基本指令**

**下載模型**

- mac預設下載的目錄`~/.ollama/models/blobs`  
- windows `C:\Users\<用户名>\.ollama\models`  
- linux `~/.ollama/models`  
- 更改預設目錄要修改環境變數`OLLAMA_MODELS` 來指定新的儲存路徑

**更改下載目錄**

- **windows**

```
Windows
	1.	修改系統環境變數：
	•	右鍵點擊「此電腦」，選擇「屬性」。
	•	點擊「高級系統設定」。
	•	在「系統屬性」窗口中，選擇「高級」選項卡，然後點擊「環境變數」。
	•	在「系統變數」部分，點擊「新建」。
	•	輸入「變量名」為 `OLLAMA_MODELS`，並設定「變量值」為您想要的自定義路徑（例如 `D:\Ollama\Models`）。
	•	點擊「確定」保存變更。
	2.	重啟 Ollama：
	•	退出 Ollama 服務（右鍵點擊 Ollama 圖標，選擇「退出」）。
	•	重新啟動 Ollama 服務。
```

- **mac**

```
	1.	設定環境變數：
	•	打開終端機。
	•	如果您使用 Bash，編輯 `~/.bashrc` 文件：
	nano ~/.bashrc
	
	如果您使用 Zsh，編輯 `~/.zshrc` 文件：
	nano ~/.zshrc
	
	在文件末尾添加以下行：
	export OLLAMA_MODELS=~/ollama_download_models
	
	重新載入配置：
	source ~/.bashrc
	source ~/.zshrc
	
	重新開機
  
```

**檢查是否已經安裝Ollama**

```bash
ollama --version
```

**查詢可以下載的模型**

[查詢Ollama支援的Model](https://ollama.com/search)

**下載模型指令**

```bash
ollama pull llama3.2:3b
```

**檢視目前已經下載的模型**

```bash
ollama list
```

**執行模型**

```bash
ollama run llama3.2
```

**停止執行模型**

```
>>> /bye
```


**目前被載入的模型**
- 可以查看是否是使用GPU

```bash
ollama ps

#=====output===
NAME         ID              SIZE      PROCESSOR    UNTIL              
gemma3:4b    a2af6cc3eb7f    6.3 GB    100% GPU     3 minutes from now
```

**停止模型**

```bash
ollama stop llama3.2
```

**刪除模型**

```bash
ollama rm llama3.2
```

---


<a name="docker安裝Ollama"></a>
### 3. docker安裝Ollama
- 缺點:都是使用CPU
- 如果要支援NVIDIA,請安裝NVIDIA Container Toolkit⁠.

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```


> [!IMPORTANT]
> 安裝完後,可以利用docker desktop內container Exec來執行ollama的指令

---

<a name="docker安裝OpenWebUI"></a>
### 4. docker安裝OpenWebUI

- 可以使用透過網路連線的免費模型(Chatbot Arena有17b的參數量)
- 設定->管理員設定->連線->開啟直接連線(會自動連線Chatbot Arena)

- 由於使用了restart always,docker一被啟動就會自動開啟container(比較秏資源)

```bash
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```


- 手動開啟container的語法

```bash
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui ghcr.io/open-webui/open-webui:main
```

**使用瀏覽器啟動http://localhost:8080**

---
<a name="requests連結ollama"></a>
### 5. requests連結ollama

```python
import requests

def chat_with_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False,
        "options": { #參考說明1
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
        },
        "max_tokens": 100,
        "format": "json",
    }

    response = requests.post(url, json=payload)
    result = response.json()
    print("💬 AI 回應：")
    # Print the whole result for debugging
    print(result)
    # Try to print the 'response' key if it exists, otherwise print possible keys
    if "response" in result:
        print(result["response"])
    elif "message" in result:
        print(result["message"])
    elif "content" in result:
        print(result["content"])
    else:
        print("No expected key found in response. Available keys:", result.keys())

#範例輸入
chat_with_ollama("請用簡單的方式解釋什麼是Python的函式？")
```

### 說明1:

`options` 物件封裝了對於生成模型行為的三個關鍵調整參數：`temperature`、`top_p` 以及 `top_k`。透過這些設定，我們可以更精細地控制模型在產生文字時的隨機程度與多樣性，以達到更符合需求的輸出風格。

`temperature`（溫度）參數設定為 0.7，表示在挑選下一個字元或詞彙時，會根據模型預測機率分佈做溫度縮放。溫度越接近 1，生成結果越隨機、多樣；當溫度降低時，生成更傾向於高機率選擇，輸出結果較為保守且重複性增加。設定為 0.7 能在隨機性與穩定性間取得平衡。

`top_p`（又稱 nucleus sampling）設為 0.9，代表每次生成時僅考慮累積機率前 90% 的候選詞彙。換言之，模型先將所有候選依機率由高到低排序，然後從機率總和達到 0.9 的詞彙子集中進行隨機抽樣。這種方法可避免只關注最高機率而忽略其他合理選項，也能自動調整抽樣範圍以抑制極低機率的「噪音」輸出。

`top_k` 參數設置為 50，表示在抽樣時僅從預測機率最高的前 50 個詞彙中選擇下一步結果。這是在限制搜索空間大小、提高運算效率與品質控制的常見做法。結合 `top_p` 與 `top_k` 使用，能進一步平衡多樣性與穩定性：`top_k` 確保候選集不超過一定規模，`top_p` 則依實際機率分佈動態修剪集內詞彙。

綜合而言，這三項參數共同為生成模型提供了多層次的隨機與篩選機制。依據不同應用場景（如對話系統、文章撰寫或程式碼生成），可微調這些值以獲得更符合需求的結果。

<a name="requests連結ollama_generate_mode"></a>
### 6. requests連結ollama_generate_mode

```python
import requests
def chat_with_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False,
        "options": { #參考說明1
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
        },
        "max_tokens": 100,
        "format": "json",
    }

    response = requests.post(url, json=payload)
    result = response.json()
    print("💬 AI 回應：")
    # Print the whole result for debugging
    #print(result)
    # Try to print the 'response' key if it exists, otherwise print possible keys
    if "response" in result:
        print(result["response"])
    elif "message" in result:
        print(result["message"])
    elif "content" in result:
        print(result["content"])
    else:
        print("No expected key found in response. Available keys:", result.keys())

    
def chat_loop():
    print("歡迎使用本地端 LLM 聊天機器人（輸入 q 離開）")
    while True:
        user_input = input("👤 你說：")
        if user_input.lower() == 'q':
            break
        chat_with_ollama(user_input)

chat_loop()
```

---

<a name="requests連結chat_mode"></a>
### 7. requests連結chat_mode

```python
import requests
import json

def chat_with_ollama(prompt: str):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "gemma3:1b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": True,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
        }
    }

    print("💬 AI 回應：", end="", flush=True)
    
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    
                    # 檢查是否有訊息內容
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        print(content, end="", flush=True)
                    
                    # 檢查是否完成
                    if chunk.get('done', False):
                        print()  # 換行
                        break
                        
                except json.JSONDecodeError:
                    continue
                    
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 請求錯誤: {e}")
    except Exception as e:
        print(f"\n❌ 處理錯誤: {e}")

def chat_loop():
    print("歡迎使用本地端 LLM 聊天機器人（輸入 q 離開）")
    while True:
        user_input = input("👤 你說：")
        if user_input.lower() == 'q':
            break
        chat_with_ollama(user_input)
        print()  # 空行分隔

chat_loop()
```

<a name="連接gradio的介面呼叫ollama的api"></a>
### 8. 連接gradio的介面呼叫ollama的api

![](./images/pic1.png)

- [ollama api官方說明書](https://github.com/ollama/ollama/blob/main/docs/api.md)

> [!IMPORTANT]
> 1. ollama的服數要開啟
> 2. ollama run 模型名稱
> 3. 本地端或docker api網址不一樣

- [**實作py**](./interface.py)


```python
import requests
import json
import gradio as gr

# 呼叫 Ollama 的函式
def ask_ollama(prompt):
    #url = "http://localhost:11434/api/generate"
    url = "http://host.docker.internal:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"⚠️ Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"

# 建立 Gradio 介面
iface = gr.Interface(
    fn=ask_ollama,
    inputs=gr.Textbox(label="輸入你的問題"),
    outputs=gr.Textbox(label="模型的回答"),
    title="🦙 Ollama 聊天介面 (LLaMA3)",
    description="輸入文字，讓本機的 LLaMA3 模型回答你"
)

# 啟動介面
iface.launch()
```
