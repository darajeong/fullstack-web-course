from fastapi.testclient import TestClient

from app.main import app
from uuid import uuid4

# 회원 목록 조회: 200과 목록 형태 확인
def test_get_members_returns_200():
    with TestClient(app) as client:
        response = client.get("/members")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 없는 회원 조회: 404와 오류 메시지 확인
def test_get_unknown_member_returns_404():
    with TestClient(app) as client:
        response = client.get("/members/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"

    # 회원 번호에 문자를 입력하면 422 반환
def test_member_id_validation_returns_422():
    with TestClient(app) as client:
        response = client.get("/members/not-a-number")

    assert response.status_code == 422

    # 회원 등록: 201과 응답 내용 확인
def test_create_member_returns_201():
    email = f"test-{uuid4()}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/members",
            json={
                "name": "Test User",
                "email": email,
                "age": 30,
            },
        )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Test User"
    assert body["email"] == email

    # 같은 이메일로 다시 등록하면 409 반환
def test_duplicate_email_returns_409():
    email = f"duplicate-{uuid4()}@example.com"

    with TestClient(app) as client:
        # 첫 번째 등록은 성공
        first = client.post(
            "/members",
            json={
                "name": "First",
                "email": email,
                "age": 30,
            },
        )

        assert first.status_code == 201

        # 같은 이메일로 두 번째 등록
        second = client.post(
            "/members",
            json={
                "name": "Second",
                "email": email,
                "age": 31,
            },
        )

        assert second.status_code == 409
        assert second.json()["detail"] == "Email already exists"