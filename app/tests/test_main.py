import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine

# Тестовый клиент FastAPI
client = TestClient(app)

# Фикстура для создания и удаления временной базы данных в памяти
@pytest.fixture(scope="module")
def test_db():
    from app.database import SessionLocal, Base

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Пример теста для GET /memes
def test_read_memes(test_db):
    response = client.get("/memes")
    assert response.status_code == 200
    assert response.json() == []

# Добавьте другие тесты для остальных эндпоинтов
