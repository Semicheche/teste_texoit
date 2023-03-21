from fastapi import FastAPI
from v1.api import router
from core.db.db import Base
from core.models import Movie


db_init = Base()
app = FastAPI()

app.include_router(router)
