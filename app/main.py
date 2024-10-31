from fastapi import FastAPI
from .database import init_db
from .routes import blog, user, auth, comments

app = FastAPI()

# initialize database tables
init_db()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}