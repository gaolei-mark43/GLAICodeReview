from fastapi import FastAPI
from app.api import review
from app.api import auth

app = FastAPI()
 
app.include_router(review.router, prefix="/api")
app.include_router(auth.router, prefix="/api") 