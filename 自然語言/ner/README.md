# 命名實體識別(named entity recognition)
- 模型:(中央研究院)  
ckiplab/bert-base-chinese-ner

- 模型:roberthsu2003  
roberthsu2003/models_for_ner

## 使用ckiplab/bert-base-chinese-ner

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

## 使用:roberthsu2003/models_for_ner



```python
#使用方法(pipeline的方法)

from transformers import pipeline

ner_pipe = pipeline('token-classification', model='roberthsu2003/models_for_ner',aggregation_strategy='simple')
inputs = '徐國堂在台北上班'
res = ner_pipe(inputs)
print(res)
res_result = {}
for r in res:
    entity_name = r['entity_group']
    start = r['start']
    end = r['end']
    if entity_name not in res_result:
        res_result[entity_name] = []
    res_result[entity_name].append(inputs[start:end])

res_result
#==output==
{'PER': ['徐國堂'], 'LOC': ['台北']}

```


```python
#使用方法(model,tokenizer)
from transformers import AutoModelForTokenClassification, AutoTokenizer
import numpy as np

# Load the pre-trained model and tokenizer
model = AutoModelForTokenClassification.from_pretrained('roberthsu2003/models_for_ner')
tokenizer = AutoTokenizer.from_pretrained('roberthsu2003/models_for_ner')

# The label mapping (you might need to adjust this based on your training)
#['O', 'B-PER', 'I-PER', 'B-ORG', 'I-ORG', 'B-LOC', 'I-LOC']
label_list = list(model.config.id2label.values())


def predict_ner(text):
    """Predicts NER tags for a given text using the loaded model."""
    # Encode the text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    
    # Get model predictions
    outputs = model(**inputs)
    predictions = np.argmax(outputs.logits.detach().numpy(), axis=-1)
    
    # Get the word IDs from the encoded inputs
    # This is the key change - word_ids() is a method on the encoding result, not the tokenizer itself
    word_ids = inputs.word_ids(batch_index=0)
    
    pred_tags = []
    for word_id, pred in zip(word_ids, predictions[0]):
        if word_id is None:
            continue  # Skip special tokens
        pred_tags.append(label_list[pred])

    return pred_tags

#To get the entities, you'll need to group consecutive non-O tags:

def get_entities(tags):
    """Groups consecutive NER tags to extract entities."""
    entities = []
    start_index = -1
    current_entity_type = None
    for i, tag in enumerate(tags):
        if tag != 'O':
            if start_index == -1:
                start_index = i
                current_entity_type = tag[2:] # Extract entity type (e.g., PER, LOC, ORG)
        else: #tag == 'O'
            if start_index != -1:
                entities.append((start_index, i, current_entity_type))
                start_index = -1
                current_entity_type = None
    if start_index != -1:
        entities.append((start_index, len(tags), current_entity_type))
    return entities

# Example usage:
text = "徐國堂在台北上班"
ner_tags = predict_ner(text)
print(f"Text: {text}")
#==output==
#Text: 徐國堂在台北上班


print(f"NER Tags: {ner_tags}")
#===output==
#NER Tags: ['B-PER', 'I-PER', 'I-PER', 'O', 'B-LOC', 'I-LOC', 'O', 'O']


entities = get_entities(ner_tags)
word_tokens = tokenizer.tokenize(text)  # Tokenize to get individual words
print(f"Entities:")
for start, end, entity_type in entities:
    entity_text = "".join(word_tokens[start:end])
    print(f"- {entity_text}: {entity_type}")

#==output==
#Entities:
#- 徐國堂: PER
#- 台北: LOC

```



