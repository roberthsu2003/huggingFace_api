# text-classification
## 模型:lxyuan/distilbert-base-multilingual-cased-sentiments-student
- multilingqual-sentiments
- 支援中文

```python
from transformers import pipeline

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
)

# english
distilled_student_sentiment_classifier ("I love this movie and i would watch it again and again!")


# malay
distilled_student_sentiment_classifier("Saya suka filem ini dan saya akan menontonnya lagi dan lagi!")


# japanese
distilled_student_sentiment_classifier("私はこの映画が大好きで、何度も見ます！")


```


```python
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
)

label2string = {
    'positive':'正評',
    'negative':'負評'
}

result = distilled_student_sentiment_classifier("飯很不好吃")
print('評比:',label2string[result[0]['label']])
print('分數:',result[0]['score'])

#==output==
評比: 負評
分數: 0.9129632115364075
```