# 本地端 LLM 教學範例

使用 requests 模組與 Ollama 本地 HTTP API 溝通。

---

## 基礎前提

- 確保 Ollama 正在執行，並且模型已經被拉下來（例如：ollama run gemma:1b 已經執行過一次）
- Ollama API 預設會在 `http://localhost:11434` 提供服務。

---

## 安裝必要套件

如果還沒安裝，請執行：

```bash

pip install requests
```

---

## 範例 1：發送基本對話請求給 Gemma 模型

```python

import requests

def chat_with_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:2b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    result = response.json()
    print("💬 AI 回應：")
    print(result["response"])

# 範例輸入
chat_with_ollama("請用簡單的方式解釋什麼是Python的函式？")
```

---

## 範例 2：建立一個簡單的聊天互動（CLI 聊天機器人）

```python

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

## 範例 3：包裝成函式，供 Web 或 GUI 使用

這個結構更容易擴展為 Flask、Streamlit 等應用：

```python
def generate_response(prompt: str, model: str = "gemma3:1b") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()["response"]
    except Exception as e:
        return f"錯誤：{e}"
```


