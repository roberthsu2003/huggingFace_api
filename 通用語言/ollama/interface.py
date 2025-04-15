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
