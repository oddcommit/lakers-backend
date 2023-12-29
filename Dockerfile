# ベースとなるDockerイメージ
FROM python:3.10

# 必要なファイルをコピー
COPY . /app
COPY ./pyproject.toml /app/pyproject.toml

# 作業ディレクトリを設定
WORKDIR /app

# ログを出力
ENV PYTHONUNBUFFERED=1

# 環境変数
ENV ALLOWED_HOST=''
ENV SECRET_KEY=''
ENV CORS_ALLOWED_ORIGINS=''
ENV DB_NAME=''
ENV DB_USER=''
ENV DB_PASSWORD=''
ENV DB_HOST=''

# poetryのインストール
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    PYSETUP_PATH="/opt/pysetup"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl && \
    apt-get clean
RUN curl -sSL https://install.python-poetry.org/ | python -

# パッケージのインストール
RUN poetry install --without dev

# ポート番号を指定
EXPOSE 8000

# アプリケーションの起動コマンド
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
