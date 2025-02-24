from app.database import engine, Base
from app.models import UploadFile, Record

Base.metadata.create_all(bind=engine)