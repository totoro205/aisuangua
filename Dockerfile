# 使用 Python 3.10 slim 映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案
COPY . .

# 設定 Streamlit 監聽的埠號為 8080（Cloud Run 要求）
ENV STREAMLIT_SERVER_PORT=8080

# 開放 8080 埠
EXPOSE 8080

# 啟動 Streamlit 應用
CMD ["streamlit", "run", "ai算卦.py", "--server.port=8080", "--server.address=0.0.0.0"]
