from app import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_read_user_auth():
    response = client.get("/users/649809d0ce8d854e70f30a91", headers={"bearer": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJtYXJpYW5AZ21haWwuY29tIiwiaWF0IjoxNjg3Njg2NzcwLCJuYmYiOjE2ODc2ODY3NzAsImp0aSI6IjVkZWVkZDExLWI4M2QtNDdjOS05OGE1LWViNTg0M2YwZGY3MiIsImV4cCI6MTY4NzY4NzY3MCwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.jbNdTA79bB0B1gBeR-m5V1LGHkB2RQTeyX8CjllUdnBrpRzHMS8ZIPpTwpapEmJmuRchVe2iSTaUxq5SubbbKA"})
    assert response.status_code == 200
    # assert response.json() == {
    #     "id": "foo",
    #     "title": "Foo",
    #     "description": "There goes my hero",
    # }

