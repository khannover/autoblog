# main.py

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Post
import asyncio
from pydantic import BaseModel
import aiohttp
import json

app = FastAPI()

# Database setup
engine = create_engine('sqlite:///blog.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

# Data model for creating posts
class PostCreate(BaseModel):
    title: str
    prompt: str

# Asynchronous function to generate content using Ollama
async def generate_content(prompt_text: str) -> str:
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:11434/generate'  # Default Ollama server URL
        headers = {'Content-Type': 'application/json'}
        payload = {
            'model': 'llama2',  # Replace with the model you have installed
            'prompt': prompt_text
        }
        async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                async for line in response.content:
                    data = json.loads(line.decode('utf-8'))
                    if 'done' in data and data['done']:
                        break
                    content = data.get('response', '').strip()
                return content
            else:
                raise HTTPException(status_code=500, detail="Content generation failed")

# Endpoint to create a new post
@app.post("/posts/")
def create_post(post: PostCreate):
    session = SessionLocal()
    db_post = Post(title=post.title, prompt=post.prompt)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    session.close()
    return {"id": db_post.id, "title": db_post.title}

# Endpoint to get a list of all posts
@app.get("/posts/")
def read_posts():
    session = SessionLocal()
    posts = session.query(Post).all()
    session.close()
    return [{"id": post.id, "title": post.title} for post in posts]

# Endpoint to get a specific post
@app.get("/posts/{post_id}")
async def read_post(post_id: int):
    session = SessionLocal()
    post = session.query(Post).filter(Post.id == post_id).first()
    session.close()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        content = await generate_content(post.prompt)
    except HTTPException as e:
        raise e
    return {"title": post.title, "content": content}
