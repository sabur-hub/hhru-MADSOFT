from app.services import media_service, meme_service
from app.database import SessionLocal
from fastapi import UploadFile
import pytest

@pytest.fixture(scope="module")
def test_db():
    from app.database import SessionLocal, Base
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_upload_image():
    with open("test_image.jpg", "rb") as f:
        file = UploadFile(filename="test_image.jpg", file=f, content_type="image/jpeg")
        file_name = media_service.upload_image(file)
        assert file_name.endswith(".jpg")

def test_create_meme(test_db):
    from app.schemas import MemeCreate

    with open("test_image.jpg", "rb") as f:
        file = UploadFile(filename="test_image.jpg", file=f, content_type="image/jpeg")
        meme_data = MemeCreate(text="Test Meme", image_path="")
        new_meme = meme_service.create_meme(test_db, meme_data, file)
        assert new_meme.text == "Test Meme"
        assert new_meme.image_path is not None
