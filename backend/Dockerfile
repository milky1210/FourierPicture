FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# コンテナ外からアクセスするためにポートを公開
EXPOSE 5000

# 0.0.0.0 でリッスンするように起動
CMD ["python", "app.py"]
