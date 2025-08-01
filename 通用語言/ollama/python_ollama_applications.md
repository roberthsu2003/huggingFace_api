# Python + Ollama 應用程式想法集

基於 `ollama.md` 中的基礎範例，以下是一些實用的 Python + Ollama 應用程式想法，適合教學和實際應用。

## 🎯 教學導向應用

### 1. 程式碼解釋器
讓學生貼上程式碼，AI 解釋每一行在做什麼

```python
import requests

def generate_response(prompt: str, model: str = "gemma:2b") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()["response"]
    except Exception as e:
        return f"錯誤：{e}"

def explain_code(code_snippet):
    prompt = f"請逐行解釋這段 Python 程式碼：\n{code_snippet}"
    return generate_response(prompt)

# 使用範例
code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
print(explain_code(code))
```

### 2. 程式碼除錯助手
學生遇到錯誤時，AI 幫忙找問題

```python
def debug_helper(error_message, code):
    prompt = f"這段程式碼出現錯誤：{error_message}\n程式碼：\n{code}\n請幫我找出問題並提供解決方案"
    return generate_response(prompt)

# 使用範例
error_code = """
def greet(name)
    print(f"Hello, {name}!")
"""
error_msg = "SyntaxError: invalid syntax"
print(debug_helper(error_msg, error_code))
```

### 3. 練習題產生器
根據主題自動產生程式練習題

```python
def generate_exercise(topic, difficulty="初級"):
    prompt = f"請產生一個關於 {topic} 的 {difficulty} Python 練習題，包含題目描述和範例解答"
    return generate_response(prompt)

# 使用範例
print(generate_exercise("迴圈", "中級"))
```

## 🚀 實用工具應用

### 4. 智能筆記整理
將課堂筆記轉換成結構化內容

```python
def organize_notes(raw_notes):
    prompt = f"請將以下筆記整理成清楚的重點摘要，使用條列式格式：\n{raw_notes}"
    return generate_response(prompt)

# 使用範例
notes = """
今天學了變數 變數可以存資料 有不同類型 int str float bool
還有list和dict 可以用來存多個資料
"""
print(organize_notes(notes))
```

### 5. 程式碼風格檢查器
檢查程式碼是否符合 PEP 8 規範

```python
def style_checker(code):
    prompt = f"請檢查這段程式碼的風格，並提供 PEP 8 規範的改善建議：\n{code}"
    return generate_response(prompt)

# 使用範例
messy_code = """
def calculate_area(length,width):
    result=length*width
    return result
"""
print(style_checker(messy_code))
```

### 6. 文件字串產生器
自動為函式產生說明文件

```python
def generate_docstring(function_code):
    prompt = f"請為這個函式產生完整的 Google 風格 docstring：\n{function_code}"
    return generate_response(prompt)

# 使用範例
func_code = """
def calculate_bmi(weight, height):
    return weight / (height ** 2)
"""
print(generate_docstring(func_code))
```

## 🎮 互動式學習工具

### 7. Python 問答遊戲

```python
def python_quiz():
    prompt = "請出一題 Python 基礎概念的選擇題，包含 4 個選項和正確答案"
    return generate_response(prompt)

def quiz_game():
    print("🎯 Python 知識問答遊戲")
    while True:
        print("\n" + "="*50)
        print(python_quiz())
        
        continue_game = input("\n繼續下一題？(y/n): ")
        if continue_game.lower() != 'y':
            break
    print("感謝參與！")

# 啟動遊戲
# quiz_game()
```

### 8. 程式碼翻譯器
將自然語言轉換成 Python 程式碼

```python
def natural_to_code(description):
    prompt = f"請將以下描述轉換成 Python 程式碼，並加上註解說明：{description}"
    return generate_response(prompt)

# 使用範例
description = "建立一個函式，計算一個數字列表的平均值"
print(natural_to_code(description))
```

## 📊 進階應用

### 9. 學習進度追蹤

```python
import json
from datetime import datetime

def learning_assessment(student_code, topic):
    prompt = f"評估這段關於 {topic} 的程式碼，給出學習建議和評分(1-10分)：\n{student_code}"
    return generate_response(prompt)

def save_progress(student_name, topic, code, assessment):
    progress_data = {
        "timestamp": datetime.now().isoformat(),
        "student": student_name,
        "topic": topic,
        "code": code,
        "assessment": assessment
    }
    
    # 儲存到檔案 (實際應用中可能使用資料庫)
    with open(f"progress_{student_name}.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(progress_data, ensure_ascii=False) + "\n")

# 使用範例
student_code = """
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
average = total / len(numbers)
print(average)
"""
assessment = learning_assessment(student_code, "迴圈和平均值計算")
save_progress("張同學", "迴圈", student_code, assessment)
```

### 10. 專案想法產生器

```python
def suggest_project(skill_level, interests):
    prompt = f"推薦一個適合 {skill_level} 程度，對 {interests} 有興趣的學生的 Python 專案，包含：\n1. 專案描述\n2. 主要功能\n3. 需要用到的技術\n4. 預估完成時間"
    return generate_response(prompt)

# 使用範例
print(suggest_project("中級", "遊戲開發"))
```

## 🔧 完整應用範例：多功能學習助手

```python
class PythonLearningAssistant:
    def __init__(self, model="gemma:2b"):
        self.model = model
    
    def generate_response(self, prompt):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload)
            return response.json()["response"]
        except Exception as e:
            return f"錯誤：{e}"
    
    def main_menu(self):
        while True:
            print("\n🐍 Python 學習助手")
            print("1. 程式碼解釋")
            print("2. 除錯協助")
            print("3. 產生練習題")
            print("4. 風格檢查")
            print("5. 知識問答")
            print("6. 離開")
            
            choice = input("請選擇功能 (1-6): ")
            
            if choice == "1":
                code = input("請輸入要解釋的程式碼：\n")
                print(self.explain_code(code))
            elif choice == "2":
                code = input("請輸入有問題的程式碼：\n")
                error = input("錯誤訊息：")
                print(self.debug_helper(error, code))
            elif choice == "3":
                topic = input("請輸入主題：")
                level = input("難度 (初級/中級/高級)：")
                print(self.generate_exercise(topic, level))
            elif choice == "4":
                code = input("請輸入要檢查的程式碼：\n")
                print(self.style_checker(code))
            elif choice == "5":
                print(self.python_quiz())
            elif choice == "6":
                print("再見！")
                break
            else:
                print("無效選擇，請重新輸入")
    
    def explain_code(self, code_snippet):
        prompt = f"請逐行解釋這段 Python 程式碼：\n{code_snippet}"
        return self.generate_response(prompt)
    
    def debug_helper(self, error_message, code):
        prompt = f"這段程式碼出現錯誤：{error_message}\n程式碼：\n{code}\n請幫我找出問題並提供解決方案"
        return self.generate_response(prompt)
    
    def generate_exercise(self, topic, difficulty="初級"):
        prompt = f"請產生一個關於 {topic} 的 {difficulty} Python 練習題，包含題目描述和範例解答"
        return self.generate_response(prompt)
    
    def style_checker(self, code):
        prompt = f"請檢查這段程式碼的風格，並提供 PEP 8 規範的改善建議：\n{code}"
        return self.generate_response(prompt)
    
    def python_quiz(self):
        prompt = "請出一題 Python 基礎概念的選擇題，包含 4 個選項和正確答案"
        return self.generate_response(prompt)

# 啟動應用
if __name__ == "__main__":
    assistant = PythonLearningAssistant()
    assistant.main_menu()
```

## 📝 使用說明

1. **前置需求**：
   - 確保 Ollama 正在執行
   - 已下載 gemma:2b 模型 (`ollama run gemma:2b`)
   - 安裝 requests 套件 (`pip install requests`)

2. **基礎設定**：
   - 所有範例都基於 `ollama.md` 中的 `generate_response` 函式
   - API 端點：`http://localhost:11434/api/generate`
   - 預設模型：`gemma:2b`

3. **擴展建議**：
   - 可以整合 Flask 建立 Web 介面
   - 使用 Streamlit 建立互動式應用
   - 加入資料庫儲存學習記錄
   - 整合 Jupyter Notebook 進行教學

## 🚀 下一步

這些應用可以進一步發展為：
- **Web 應用**：使用 Flask 或 FastAPI
- **桌面應用**：使用 Tkinter 或 PyQt
- **聊天機器人**：整合 LINE Bot 或 Discord Bot
- **教學平台**：結合 LMS 系統

每個應用都可以根據實際需求進行客製化調整。