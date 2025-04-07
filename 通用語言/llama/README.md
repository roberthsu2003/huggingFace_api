## Meta Llama

- [HuggingFace Meta Llama](https://huggingface.co/meta-llama)

### HuggingFace API

**使用meta-llama/Llama-3.2-3B-Instruct示範**

#### 使用流程
1. 申請huggingface帳號

2. 進入hugging face的meta-llama/Llama-3.2-3B-Instruct填寫左上角同意書`You need to agree to share your contact information to access this model`,並且按下`同意`


3. 將會看到以下訊息:`Your request to access this repository has been submitted and is awaiting a review from the repository authors. You can check the status of all your access requests in **your settings.**`\   
   請點選your settings,將會進入到個人設定頁面`Gated Repos Status`,如下圖:
   
   ![](./images/pic1.png)
   

4. 設定HuggingFace access token:如下圖

	![](./images/pic2.png)

5. 安裝python-dotenv,保護token

6. 程式碼:

```python
%pip install python-dotenv
```

```python
from huggingface_hub import login
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 使用環境變數中的token進行登入
login(token=os.getenv('HF_TOKEN'))
```


```python
from huggingface_hub import login
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 使用環境變數中的token進行登入
login(token=os.getenv('HF_TOKEN'))
```

7.本機端的記憶體不足夠,無法執行,colab上執行
