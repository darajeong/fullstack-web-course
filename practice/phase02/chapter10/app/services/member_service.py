from fastapi import HTTPException

from ..repositories import member_repository


def get_members():
    """전체 회원을 조회합니다."""
    return member_repository.find_all()


def get_member(id: int):
    """회원을 조회하고, 없으면 404로 처리합니다."""
    member = member_repository.find_by_id(id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member


def create_member(data):
    """이메일 중복을 확인한 뒤 회원을 생성합니다."""
    if member_repository.exists_by_email(str(data.email)):
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    return member_repository.create(data)