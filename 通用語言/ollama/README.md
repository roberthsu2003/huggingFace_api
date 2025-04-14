## 使用ollama和openWebUI

1. 安裝Docker
2. 本機安裝Ollama
3. docker安裝Ollama
4. docker安裝OpenWebUI

### 1. 安裝Docker
- https://docs.docker.com/get-started/get-docker/

### 2. 本機安裝Ollama
- 優點:會直接使用Mac的GPU,無GPU自動使用CPU
- [ollama官網](https://ollama.com)
- ollama支援的模型,請參考ollam的官網

**2.1 Ollama基本指令**

**下載模型**

- mac預設下載的目錄`~/.ollama/models/blobs`  
- windows `C:\Users\<用户名>\.ollama\models`  
- linux `~/.ollama/models`  
- 更改預設目錄要修改環境變數`OLLAMA_MODELS` 來指定新的儲存路徑

**更改下載目錄**

- **windows**

```
Windows
	1.	修改系統環境變數：
	•	右鍵點擊「此電腦」，選擇「屬性」。
	•	點擊「高級系統設定」。
	•	在「系統屬性」窗口中，選擇「高級」選項卡，然後點擊「環境變數」。
	•	在「系統變數」部分，點擊「新建」。
	•	輸入「變量名」為 `OLLAMA_MODELS`，並設定「變量值」為您想要的自定義路徑（例如 `D:\Ollama\Models`）。
	•	點擊「確定」保存變更。
	2.	重啟 Ollama：
	•	退出 Ollama 服務（右鍵點擊 Ollama 圖標，選擇「退出」）。
	•	重新啟動 Ollama 服務。
```

- **mac**

```
	1.	設定環境變數：
	•	打開終端機。
	•	如果您使用 Bash，編輯 `~/.bashrc` 文件：
	nano ~/.bashrc
	
	如果您使用 Zsh，編輯 `~/.zshrc` 文件：
	nano ~/.zshrc
	
	在文件末尾添加以下行：
	export OLLAMA_MODELS=~/ollama_download_models
	
	重新載入配置：
	source ~/.bashrc
	source ~/.zshrc
	
	重新開機
  
```

**下載模型指令**

```bash
ollama pull llama3.2:3b
```

**檢視目前已經下載的模型**

```bash
ollama list
```

**執行模型**

```bash
ollama run llama3.2
```

**停止執行模型**

```
>>> /bye
```


**目前被載入的模型**
- 可以查看是否是使用GPU

```bash
ollama ps

#=====output===
NAME         ID              SIZE      PROCESSOR    UNTIL              
gemma3:4b    a2af6cc3eb7f    6.3 GB    100% GPU     3 minutes from now
```

**停止模型**

```bash
ollama stop llama3.2
```

**刪除模型**

```bash
ollama rm llama3.2
```

### 3. docker安裝Ollama
- 缺點:都是使用CPU
- 如果要支援NVIDIA,請安裝NVIDIA Container Toolkit⁠.

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```


> [!IMPORTANT]
> 安裝完後,可以利用docker desktop內container Exec來執行ollama的指令


### 4. docker安裝OpenWebUI

- 可以使用透過網路連線的免費模型(Chatbot Arena有17b的參數量)
- 設定->管理員設定->連線->開啟直接連線(會自動連線Chatbot Arena)

- 由於使用了restart always,docker一被啟動就會自動開啟container(比較秏資源)

```bash
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```


- 手動開啟container的語法

```bash
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui ghcr.io/open-webui/open-webui:main
```

**使用瀏覽器啟動http://localhost:8080**
