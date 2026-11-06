# practice/phase02/common/db.py

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# phase02/.env 파일 읽기
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "phase02/.env 파일에 DATABASE_URL을 설정해 주세요."
    )


# DB 연결을 관리하는 Engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
)

# 요청 처리에 사용할 Session 생성 설정
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# 요청마다 Session을 만들고, 처리가 끝나면 닫기
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()