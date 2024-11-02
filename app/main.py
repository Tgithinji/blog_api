from fastapi import FastAPI
from .database import init_db
from .routes import blog, user, auth, comments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']


# CORS function that runs before every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize database tables
init_db()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comments.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
