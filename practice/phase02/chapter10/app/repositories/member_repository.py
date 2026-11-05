from psycopg.rows import dict_row

from ..db import get_connection


def find_all():
    """전체 회원을 조회합니다."""
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, name, email, age
                FROM members
                ORDER BY id;
                """
            )

            return cur.fetchall()


def find_by_id(id: int):
    """id로 회원 한 명을 조회합니다."""
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, name, email, age
                FROM members
                WHERE id = %s;
                """,
                (id,),
            )

            return cur.fetchone()


def exists_by_email(
    email: str,
    exclude_member_id: int | None = None,
):
    """같은 이메일의 회원이 있는지 확인합니다."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            if exclude_member_id is None:
                cur.execute(
                    """
                    SELECT 1
                    FROM members
                    WHERE email = %s;
                    """,
                    (email,),
                )
            else:
                cur.execute(
                    """
                    SELECT 1
                    FROM members
                    WHERE email = %s AND id <> %s;
                    """,
                    (email, exclude_member_id),
                )

            return cur.fetchone() is not None


def create(data):
    """회원을 생성하고 저장된 정보를 반환합니다."""
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, age;
                """,
                (data.name, str(data.email), data.age),
            )

            created = cur.fetchone()
            conn.commit()

            return created