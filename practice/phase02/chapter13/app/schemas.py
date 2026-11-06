from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


# 회원 등록 요청
class MemberCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=0)


# 회원 전체 수정 요청
class MemberUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=0)


# 회원 일부 수정 요청
class MemberPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0)

    @model_validator(mode="before")
    @classmethod
    def reject_explicit_null(cls, data):
        if isinstance(data, dict):
            for field in ("name", "email", "age"):
                if field in data and data[field] is None:
                    raise ValueError(
                        f"{field}에는 null을 입력할 수 없습니다."
                    )

        return data


# 회원 정보 응답
class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    name: str
    email: EmailStr
    age: int