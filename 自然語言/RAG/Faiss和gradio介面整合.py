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
