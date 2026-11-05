import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# phase02/.env 파일 읽기
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)


def get_connection():
    """PostgreSQL 연결을 만들어 반환합니다."""
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )