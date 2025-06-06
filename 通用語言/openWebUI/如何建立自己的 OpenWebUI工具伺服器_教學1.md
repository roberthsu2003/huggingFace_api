
# 如何建立自己的 OpenWebUI 工具伺服器 (教學)

本教學將引導您從零開始，使用 Python、FastAPI 和 Docker 建立一個與 OpenWebUI 相容的 OpenAPI 工具伺服器。

## 專案目標

我們將建立一個名為 `my-tool-server` 的新工具伺服器，它將包含以下功能：

1. 一個基本的 "Hello World" 端點。
2. 一個自訂的 "加法計算機" 工具。
3. 使用 Docker 進行容器化，方便部署與管理。

## 專案結構

首先，我們需要建立一個新的專案資料夾。您可以選擇一個您喜歡的位置，並建立如下的資料夾結構：

```other
my-tool-server/
├── compose.yaml
├── Dockerfile
├── main.py
└── requirements.txt
```

---

## 第一步：建立 `main.py` (應用程式核心)

這是我們的 FastAPI 應用程式主體。它定義了 API 的所有行為。

**檔案路徑**: `my-tool-server/main.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

# 1. 建立 FastAPI 應用程式實例
#    title 和 description 會顯示在 OpenAPI 文件中
app = FastAPI(
    title="我的自訂工具伺服器",
    version="1.0.0",
    description="這是一個包含自訂工具的 FastAPI 伺服器範例。",
)

# 2. 建立一個基本的根端點 (Root Endpoint)
#    這有助於我們快速測試伺服器是否正常運行
@app.get("/", summary="伺服器狀態檢查")
def read_root():
    """
    訪問此端點以確認伺服器正在運行。
    """
    return {"status": "ok", "message": "歡迎來到我的工具伺服器！"}


# 3. 建立自訂工具的資料模型 (Pydantic Model)
#    這定義了 "加法計算機" 工具需要接收的輸入資料格式
class AddNumbersInput(BaseModel):
    number_a: float = Field(..., description="第一個數字")
    number_b: float = Field(..., description="第二個數字")


# 4. 建立自訂工具的 API 端點
#    這就是 OpenWebUI 將會呼叫的 "工具"
@app.post("/add_numbers", summary="加法計算機")
def add_numbers(data: AddNumbersInput):
    """
    接收兩個數字並回傳它們的和。
    """
    result = data.number_a + data.number_b
    return {"sum": result}
```

---

## 第二步：建立 `requirements.txt` (Python 依賴項目)

這個檔案列出了我們的專案需要安裝的所有 Python 套件。

**檔案路徑**: `my-tool-server/requirements.txt`

```other
# FastAPI 核心框架
fastapi

# 運行 FastAPI 所需的 ASGI 伺服器
uvicorn

# Pydantic 已包含在 FastAPI 中，但明確列出是個好習慣
pydantic
```

---

## 第三步：建立 `Dockerfile` (容器化藍圖)

這個檔案定義了如何將我們的 Python 應用程式打包成一個獨立的 Docker 映像檔。

**檔案路徑**: `my-tool-server/Dockerfile`

```other
# 使用官方的 Python 輕量級映像檔作為基礎
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# 設定環境變數，防止 Python 產生 .pyc 檔案並禁用輸出緩衝
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /app

# 安裝依賴項目
# 複製 requirements.txt 並安裝
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 複製應用程式原始碼
COPY main.py .

# 暴露應用程式運行的連接埠
EXPOSE 8000

# 容器啟動時運行的命令
# 使用 uvicorn 啟動 main.py 中的 app
# --host 0.0.0.0 讓容器可以從外部被訪問
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 第四步：建立 `compose.yaml` (服務編排)

這個檔案讓您可以使用 `docker-compose` 指令輕鬆地啟動、停止和管理您的服務。

**檔案路徑**: `my-tool-server/compose.yaml`

```yaml
services:
  my-tool-server:
    # 使用當前目錄下的 Dockerfile 進行建置
    build: .
    # 為容器命名，方便管理
    container_name: my-custom-tool-server
    # 將主機的 8001 連接埠映射到容器的 8000 連接埠
    # 注意：我們使用 8001 是為了避免與 time 伺服器範例的 8000 衝突
    ports:
      - "8001:8000"
    # 當 Docker 重新啟動時，自動重啟此容器
    restart: unless-stopped
```

---

## 第五步：如何運行您的工具伺服器

現在所有檔案都已準備就緒，您可以啟動您的伺服器了。

1. **開啟終端機 (Terminal)**。
2. **切換到 `my-tool-server` 資料夾**。

```Bash
cd path/to/your/my-tool-server
```

1. **執行 Docker Compose 指令**。
`--build` 參數會強制 Docker 根據您的 `Dockerfile` 重新建置映像檔。

```Bash
docker-compose up --build
```

當您看到類似以下的輸出時，代表您的伺服器已經成功啟動：

```other
...
my-custom-tool-server | INFO:     Started server process [1]
my-custom-tool-server | INFO:     Waiting for application startup.
my-custom-tool-server | INFO:     Application startup complete.
my-custom-tool-server | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 第六步：測試您的伺服器

您的伺服器現在運行在 `http://localhost:8001` 上。

1. **自動產生的 API 文件**:
在您的瀏覽器中打開 [http://localhost:8001/docs](http://localhost:8001/docs)。您會看到 FastAPI 為您自動產生的互動式 API 文件 (由 Swagger UI 提供)。您可以在這裡直接測試您的 `add_numbers` 工具！
2. **在 OpenWebUI 中使用**:
    - 進入 OpenWebUI 的設定。
    - 在 "工具 (Tools)" 或 "OpenAPI" 相關設定中，新增一個 OpenAPI 端點。
    - URL 輸入 `http://<您的電腦IP>:8001/openapi.json`。
        - **重要**: 不能使用 `localhost`，因為 OpenWebUI 的容器需要透過網路 IP 位址才能找到您的工具伺服器容器。您需要填寫您電腦在區域網路中的 IP 位址 (例如 `192.168.1.100`)。
    - 儲存後，您就可以在與模型的對話中，讓它使用您的 "加法計算機" 工具了。

---

恭喜您！您已經成功建立並運行了您的第一個自訂工具伺服器。您可以基於這個範本，在 `main.py` 中添加更多、更複雜的工具。