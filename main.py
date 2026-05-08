from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import users
from routes import products
from routes import categories
from routes import tags
from routes import auth

from config import UPLOAD_FOLDER


app = FastAPI(
    title="Ecommerce API"
)


app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(auth.router)


app.mount(
    "/static",
    StaticFiles(directory=UPLOAD_FOLDER),
    name="static"
)
