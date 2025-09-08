# LLM 大模型專案報告

本文件旨在說明大型語言模型（LLM）專案的結構、目標與實作細節。專案涵蓋了從自然語言處理（NLP）核心技術到通用語言模型應用的多個面向，並針對特定場景進行了客製化開發。

## 專案結構

- **source_for_tw/**: 台灣特定資源。
- **source_hugging_face/**: Hugging Face 相關資源與模型評測。
- **法務部/**: 針對法務部應用的客製化模型與解決方案。
- **自然語言/**: 自然語言處理（NLP）核心技術的實作與展示。
- **通用語言/**: 通用語言模型的應用與介面。

---

## 第一部分：自然語言處理核心技術

自然語言處理（NLP）是本專案的基石，我們實作了多項關鍵技術，包含命名實體辨識（NER）、檢索增強生成（RAG）等。

### 1.1 命名實體辨識 (Named Entity Recognition, NER)

命名實體辨識旨在從文本中識別出具有特定意義的實體，例如人名、地名、組織名等。我們使用了 `ckiplab/bert-base-chinese-ner` 和自行微調的 `roberthsu2003/models_for_ner` 模型進行實作。

#### 模型介紹

- **模型 (中央研究院)**: `ckiplab/bert-base-chinese-ner`
- **模型 (roberthsu2003)**: `roberthsu2003/models_for_ner`

#### 程式碼範例：使用 `ckiplab/bert-base-chinese-ner`

```python
from transformers import pipeline
import numpy as np

ner_pipe = pipeline("token-classification", model='ckiplab/bert-base-chinese-ner', aggregation_strategy="simple")

inputs = "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。"
res = ner_pipe(inputs)

grouped_entities = []
current_group = None

for entity in res:
    if current_group is None:
        current_group = {
            'entity_group': entity['entity_group'],
            'word': entity['word'].replace(' ', ''),  # Remove spaces here
            'start': entity['start'],
            'end': entity['end'],
            'scores': [entity['score'].item()]
        }
    elif entity['entity_group'] == current_group['entity_group'] and entity['start'] == current_group['end']:
        current_group['word'] += entity['word'].replace(' ', '')  # Remove spaces here
        current_group['end'] = entity['end']
        current_group['scores'].append(entity['score'].item())
    else:
        grouped_entities.append(current_group)
        current_group = {
            'entity_group': entity['entity_group'],
            'word': entity['word'].replace(' ', ''),  # Remove spaces here
            'start': entity['start'],
            'end': entity['end'],
            'scores': [entity['score'].item()]
        }

if current_group:
    grouped_entities.append(current_group)

for entity in grouped_entities:
    print(f"Entity: {entity['word']}, Type: {entity['entity_group']}, Scores: {entity['scores']}")
```

### 1.2 檢索增強生成 (Retrieval-Augmented Generation, RAG)

RAG 技術結合了檢索系統與生成模型，使其能從大量文本中尋找相關資訊，並基於這些資訊生成更準確、更豐富的回答。我們使用 Faiss 向量資料庫和 Gradio 建立了一個問答系統介面。

#### 程式碼範例：Faiss 與 Gradio 整合

```python
import gradio as gr
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd

# 載入模型和tokenizer
tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# 載入dataset
dataset = load_dataset('roberthsu2003/data_for_RAG', split='train')
dataset = dataset.map(lambda x: {
    'text': 'passage:' + x['question'] + '\n' + x['answering']
})

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt", max_length=512
    )
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    with torch.no_grad():
        model_output = model(**encoded_input)
        embeddings = model_output.last_hidden_state[:, 0, :]
    return embeddings

# 建立embedding dataset
embedding_dataset = dataset.map(
    lambda x: {"embeddings": get_embeddings(x['text']).detach().cpu().numpy()[0]}
)
embedding_dataset.add_faiss_index(column="embeddings")

def search_similar_questions(question):
    # 處理輸入問題
    question = "query:" + question
    question_embedding = get_embeddings([question]).cpu().detach().numpy()
    
    # 搜尋相似問題
    scores, samples = embedding_dataset.get_nearest_examples(
        "embeddings", question_embedding, k=3
    )
    
    # 格式化輸出結果
    result = ""
    for score, q, a in zip(scores, samples['question'], samples['answering']):
        result += f"問題: {q}\n"
        result += f"答案: {a}\n"
        result += f"相似度分數: {score:.4f}\n"
        result += "="*50 + "\n\n"
    
    return result

# 建立Gradio介面
iface = gr.Interface(
    fn=search_similar_questions,
    inputs=gr.Textbox(lines=2, placeholder="請輸入您的問題..."),
    outputs=gr.Textbox(lines=10),
    title="Tesla Model 3問答系統",
    description="輸入問題，系統會搜尋最相關的答案"
)

if __name__ == "__main__":
    iface.launch()
```

---

## 第二部分：通用語言模型應用

本部分專注於通用大型語言模型的應用，包括 Meta 的 Llama 系列模型、Ollama 框架以及 OpenWebUI 的客製化。

### 2.1 Llama 系列模型應用

我們使用了 `meta-llama/Llama-3.2-3B-Instruct` 模型進行實驗。此模型需要在 Hugging Face 平台申請權限，並建議在具備足夠記憶體（超過 12GB）及 GPU 的環境（如 Google Colab）中執行。

#### 使用流程
1. 於 Hugging Face 平台申請 `meta-llama/Llama-3.2-3B-Instruct` 模型存取權限。
2. 取得並設定 Hugging Face Access Token。
3. 在 Colab 等環境中設定環境變數或 Secret，以保護 Token。
4. 載入模型並進行推論。

### 2.2 Ollama 框架應用

Ollama 是一個輕量級的框架，可以方便地在本機端運行大型語言模型。我們建立了一個 Gradio 介面，透過 API 呼叫在本機運行的 Llama 3.2 模型。

#### 程式碼範例：Ollama Gradio 介面

```python
import requests
import json
import gradio as gr

# 呼叫 Ollama 的函式
def ask_ollama(prompt):
    #url = "http://localhost:11344/api/generate"
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

### 2.3 OpenWebUI 工具伺服器

為了擴充 OpenWebUI 的功能，我們建立了自定義的工具伺服器。此伺服器可以讓 LLM 執行特定的後端任務。

#### 程式碼範例：My Tool Server (main.py)

由於 `main.py` 內容為空，此處僅提供概念性說明。一個基本的工具伺服器通常會使用 FastAPI 或 Flask 框架，定義數個 API 端點。每個端點對應一個工具，接收 LLM 傳來的參數，執行特定功能（如資料查詢、檔案操作等），並將結果回傳。

```python
# 概念性範例 (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ToolInput(BaseModel):
    parameter: str

@app.post("/my_tool")
async def use_my_tool(tool_input: ToolInput):
    try:
        # 在此執行工具的邏輯
        result = f"工具已成功執行，參數為: {tool_input.parameter}"
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 執行伺服器: uvicorn main:app --reload
```