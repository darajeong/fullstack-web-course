from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ORM 모델의 공통 부모 클래스
class Base(DeclarativeBase):
    pass


# members 테이블에 연결되는 회원 모델
class Member(Base):
    __tablename__ = "members"

    member_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )