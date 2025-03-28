# question-answering

- timpal0l/mdeberta-v3-base-squad2 (模型比較大)
- uer/roberta-base-chinese-extractive-qa (模型比較小)

- roberthsu2003/models_for_qa_slide

## 實作

```python
from transformers import pipeline

pipe = pipeline("question-answering", model="roberthsu2003/models_for_qa_slide")
```


```python
answer = pipe(question="蔡英文何時卸任?",context="蔡英文於2024年5月卸任中華民國總統，交棒給時任副總統賴清德。卸任後較少公開露面，直至2024年10月她受邀訪問歐洲。[25]")
answer['answer']
```


```python

context='台積電也承諾未來在台灣的各項投資不變，計劃未來在本國建造九座廠，包括新竹、高雄、台中、嘉義和台南等地，在2035年，台灣仍將生產高達80%的晶片。'
answer = pipe(question='台積電未來要建立幾座廠',context=context)
print(answer['answer'])
answer = pipe(question='2035年在台灣生產的晶片比例?',context=context)
print(answer['answer'])
```