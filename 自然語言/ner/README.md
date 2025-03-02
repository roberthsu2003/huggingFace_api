# 命名實體識別(named entity recognition)
- 模型:(中央研究院)
- ckiplab/bert-base-chinese-ner

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


#==output==
Device set to use cpu
Entity: 傅達仁, Type: PERSON, Scores: [0.9999995231628418, 0.9999995231628418]
Entity: 今, Type: DATE, Scores: [0.9991734623908997]
Entity: 20年, Type: DATE, Scores: [0.9999994039535522, 0.9999892711639404]
Entity: 緯來體育台, Type: ORG, Scores: [0.9999988079071045, 0.9999990463256836]
```
