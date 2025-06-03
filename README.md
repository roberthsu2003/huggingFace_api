# huggingFace的應用
## [Transformer快速入門](https://transformers.run)
## [gradio介面](https://github.com/roberthsu2003/gradio)
## 開放模型
### 1. [ollama 和 openWebUI](./通用語言/ollama)

### 2. [openWebUI應用](./通用語言/openWebUI)

### 2. 通用(多模態)語言模型:
2.1 [llama使用huggingface api](./通用語言/llama)
- 缺點:要12GB以上記憶體
- 優點:速度較快

2.2 [llama使用huggingface api](./通用語言/llama/demo2.ipynb)
- 缺點:回答比較慢
- 優點: CPU可以執行,大約9GB的記憶體

2.3 [圖轉文字描述-使用meta-llama/Llama-3.2-11B-Vision-Instruct](./通用語言/llama/demo3.ipynb)

- 模型大約要22GB,下載時間較久(本機不適合,適合使用colab的GPU使用)
	- 缺點:使用CPU回答速度慢(6核心CPU,大約28分鐘)
	- 不適合使用CPU執行

 
### 2. 自然語言(Natural Language Processing)
[情感分析](./自然語言/text-classification)

[命名實體識別(NER)](./自然語言/ner)

[Question_answering](./自然語言/qa)

[多項選擇](./自然語言/multiple_choice)

[文本相似](./自然語言/multiple_choice/demo1.ipynb)

[RAG_檢索增強生成](./自然語言/RAG)

### 3. HuggingFace上可以使用的資源

[**Hugging Face資源**](./source_hugging_face)

[**專門為繁體中文優化過的開源模型**](./source_for_tw)




