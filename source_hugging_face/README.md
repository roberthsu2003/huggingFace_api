## Hugging Face的一些資源

## HuggingFace 免費資源
- 支援繁體中文(triditional chinese)
### **1. text-embedding生成**
**支援繁體中文**

### [**. 適合繁體中文的embedding模型評估表**](./Embeddings模型評測.xlsx)

> 資料來源:[使用繁體中文評測各家 Embedding 模型的檢索能力](https://ihower.tw/blog/archives/12167)


- intfloat/multilingual-e5-large

### **2. text-generation**
**支援繁體中文**

- mistralai/Mistral-Nemo-Instruct-2407 (serverless)

- [huggingface網址](./https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407)

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
	api_key="xxxxxxxxxxx"
)

messages = [
	{
		"role": "user",
		"content": "法國的首都是何處?"
	}
]

completion = client.chat.completions.create(
    model="mistralai/Mistral-Nemo-Instruct-2407", 
	messages=messages, 
	max_tokens=500
)

print(completion.choices[0].message)
```

### **3. automatic speech recognition**
**僅支援英文**
- facebook/wav2vec2-base-960h

**支援多種語言(自動判斷)**
- openai/whisper-large-v3-turbo (serverless)

### **4. text-classification**
- **multilingual-sentiments**
- **支援中文**

- lxyuan/distilbert-base-multilingual-cased-sentiments-student

### **5. question-answering**
- timpal0l/mdeberta-v3-base-squad2 (模型比較大)
- uer/roberta-base-chinese-extractive-qa (模型比較小)


