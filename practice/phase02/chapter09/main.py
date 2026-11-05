from fastapi import FastAPI, HTTPException, Response, status

from common.db import get_connection


app = FastAPI()


@app.delete(
    "/members/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_member(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM members
                WHERE id = %s
                RETURNING id;
                """,
                (id,),
            )

            deleted = cur.fetchone()

            if deleted is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found",
                )

            conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)