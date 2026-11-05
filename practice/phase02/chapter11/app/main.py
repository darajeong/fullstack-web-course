from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Member

app = FastAPI()


@app.get("/members/{member_id}")
def get_member(member_id: int):
    with SessionLocal() as session:
        stmt = select(Member).where(Member.member_id == member_id)
        member = session.scalar(stmt)

        if member is None:
            raise HTTPException(
                status_code=404,
                detail="해당 회원이 존재하지 않습니다.",
            )

        return {
            "member_id": member.member_id,
            "name": member.name,
            "email": member.email,
            "age": member.age,
        }