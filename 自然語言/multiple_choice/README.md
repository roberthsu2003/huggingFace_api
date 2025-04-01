## 多項選擇(Multiple Choice)
> [!NOTE]
> 模型:roberthsu2003/for_multiple_choice  
> [資料集來源](https://huggingface.co/datasets/roberthsu2003/for_Multiple_Choice)  
> [官方說明書](https://huggingface.co/docs/transformers/tasks/multiple_choice#inference)  
- [簡體版說明書](https://blog.csdn.net/LLMUZI123456789/article/details/136478140?utm_source=chatgpt.com)  
> [實作ipynb](./demo1.ipynb)  

```python
from transformers import AutoTokenizer, AutoModelForMultipleChoice
from typing import Any
import torch

tokenizer = AutoTokenizer.from_pretrained('roberthsu2003/for_multiple_choice')
model = AutoModelForMultipleChoice.from_pretrained('roberthsu2003/for_multiple_choice')

from typing import Any
import torch

class MultipleChoicePipeline:
    def __init__(self, model, tokenizer) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.device = model.device

    def preprocess(self, context, question, choices):
        cs, qcs = [], []
        for choice in choices:
            cs.append(context)
            qcs.append(question + " " + choice)
        return tokenizer(cs, qcs, truncation="only_first", max_length=256, return_tensors="pt")

    def predict(self, inputs):
        inputs = {k: v.unsqueeze(0).to(self.device) for k, v in inputs.items()}
        return self.model(**inputs).logits

    def postprocess(self, logits, choices):
        predition = torch.argmax(logits, dim=-1).cpu().item()
        return choices[predition]

    def __call__(self, context, question, choices) -> Any:
        inputs = self.preprocess(context,question,choices)
        logits = self.predict(inputs)
        result = self.postprocess(logits, choices)
        return result

if __name__ == "__main__":
  pipe = MultipleChoicePipeline(model, tokenizer)
  result1 = pipe("男：你今天晚上有時間嗎?我們一起去看電影吧? 女：你喜歡恐怖片和愛情片，但是我喜歡喜劇片","女的最喜歡哪種電影?",["恐怖片","愛情片","喜劇片","科幻片"])
  print(result1)

```