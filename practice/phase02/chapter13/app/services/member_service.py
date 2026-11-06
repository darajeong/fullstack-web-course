from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import member_repository
from app.schemas import MemberCreate, MemberPatch, MemberUpdate


# 전체 회원 조회
def find_all_service(db: Session):
    return member_repository.find_all(db)


# 회원 번호로 한 명 조회
def find_by_id_service(db: Session, member_id: int):
    member = member_repository.find_by_id(db, member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member


# 새 회원 등록
def create_member_service(db: Session, payload: MemberCreate):
    email = str(payload.email)

    existing = member_repository.find_by_email(db, email)

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        return member_repository.create_member(
            db,
            payload.name,
            email,
            payload.age,
        )

    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# 회원 정보 전체 수정
def update_member_service(
    db: Session,
    member_id: int,
    payload: MemberUpdate,
):
    member = find_by_id_service(db, member_id)

    email = str(payload.email)
    existing = member_repository.find_by_email(db, email)

    if existing is not None and existing.member_id != member_id:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        return member_repository.update_member(
            db,
            member,
            payload,
        )

    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# 회원 정보 일부 수정
def patch_member_service(
    db: Session,
    member_id: int,
    payload: MemberPatch,
):
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required",
        )

    member = find_by_id_service(db, member_id)

    if "email" in changes:
        email = str(changes["email"])
        existing = member_repository.find_by_email(db, email)

        if existing is not None and existing.member_id != member_id:
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            )

    try:
        return member_repository.patch_member(
            db,
            member,
            payload,
        )

    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# 회원 삭제
def delete_member_service(db: Session, member_id: int):
    member = find_by_id_service(db, member_id)
    member_repository.delete_member(db, member)