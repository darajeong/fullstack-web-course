from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

from common.db import get_connection

app = FastAPI()


# 회원 등록 요청 데이터
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# 회원 등록 응답 데이터
class MemberResponse(MemberCreate):
    id: int


# 중복 이메일 확인
def check_duplicate_email(email: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM public.members WHERE email = %s",
                (email,)
            )
            return cursor.fetchone()


# 회원 저장 및 rollback 테스트
def insert_member(member: MemberCreate):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, age
                """,
                (member.name, str(member.email), member.age)
            )

            row = cursor.fetchone()

            # 조회 결과를 응답용 딕셔너리로 변환
            columns = [column[0] for column in cursor.description]
            if hasattr(row, "keys"):
                created_member = dict(row)
            else:
                created_member = dict(zip(columns, row))

            # 터미널에서 INSERT 성공 여부 확인
            print("INSERT 성공, commit 전 데이터:", created_member)

            # 테스트용: 오류가 with 밖으로 전달되면서 자동 rollback
            # raise Exception("Rollback 테스트용 오류")

    # 테스트용 오류를 삭제하면 with 정상 종료 후 자동 commit
    return created_member


# 회원 등록 API
@app.post(
    "/members",
    response_model=MemberResponse,
    status_code=201
)
def create_member(member: MemberCreate):
    if check_duplicate_email(str(member.email)):
        raise HTTPException(
            status_code=409,
            detail="이미 등록된 이메일입니다."
        )

    return insert_member(member)