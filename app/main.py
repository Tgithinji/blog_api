from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from .database import init_db
from .routes import blog, user

app = FastAPI()

# initialize database tables
init_db()


# Continue only when database is connected
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='blog_api',user='postgres',
            password='password', cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(2)


app.include_router(blog.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}