from fastapi import APIRouter, status

from ..schemas import MemberCreate, MemberResponse
from ..services import member_service


router = APIRouter(
    prefix="/members",
    tags=["members"],
)


@router.get("", response_model=list[MemberResponse])
def get_members():
    return member_service.get_members()


@router.get("/{id}", response_model=MemberResponse)
def get_member(id: int):
    return member_service.get_member(id)


@router.post(
    "",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(member: MemberCreate):
    return member_service.create_member(member)