from fastapi import FastAPI
from mangum import Mangum

from app.routers import items

app = FastAPI()

app.include_router(items.router)

handler = Mangum(app)
