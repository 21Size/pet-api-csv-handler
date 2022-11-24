from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_item():
    files = {'upload_file': ('bills.csv', open('../bills.csv', 'rb'), 'multipart/form-data')}
    response = client.post("/api/v1/bills/", files=files)
    assert response.status_code == 200
