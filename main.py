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
            'model': 'tulu3',  # Replace with the model you have installed
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


# gui.py

from nicegui import ui

API_URL = 'http://localhost:8000'

@ui.page('/')
# Index page displaying the list of posts
async def index():
    async def fetch_posts():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/posts/') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return []

    posts = await fetch_posts()

    with ui.header():
        ui.label('Dynamic Blog').classes('text-4xl font-bold mx-auto')
        ui.button('Create Post', on_click=lambda: ui.open('/create'))
        ui.label('Dynamic Blog').classes('text-4xl font-bold mx-auto')


    with ui.column().classes('items-center'):
        for post in posts:
            post_card(post)

# Function to create a post card
def post_card(post):
    with ui.card().classes('w-1/2 m-4'):
        ui.label(post['title']).classes('text-2xl font-semibold')
        ui.button('Read More', on_click=lambda e, post_id=post['id']: ui.open(f'/posts/{post_id}'))

# Post detail page
@ui.page('/posts/{post_id}')
async def post_detail(post_id: int):
    with ui.header():
        ui.button('Back', on_click=lambda e: ui.open('/'))
        ui.label('Dynamic Blog').classes('text-4xl font-bold mx-auto')

    loading = ui.label('Loading...').classes('text-xl mx-auto my-4')

    async def fetch_post():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/posts/{post_id}') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    post = await fetch_post()
    loading.visible = False

    if post:
        with ui.column().classes('items-center'):
            ui.label(post['title']).classes('text-3xl font-bold my-4')
            ui.markdown(post['content']).classes('prose lg:prose-xl m-4')
    else:
        ui.label('Post not found').classes('text-red-500 text-xl')

@ui.page('/create')
def create_post():
    with ui.form():
        title = ui.input('Title').classes('w-full')
        prompt = ui.textarea('Prompt').classes('w-full h-40')
        ui.button('Submit', on_click=lambda: submit_post(title.value, prompt.value))

def submit_post(title, prompt):
    async def post_data():
        async with aiohttp.ClientSession() as session:
            payload = {'title': title, 'prompt': prompt}
            async with session.post(f'{API_URL}/posts/', json=payload) as response:
                if response.status == 200:
                    ui.notify('Post created successfully!')
                    ui.open('/')
                else:
                    ui.notify('Failed to create post.', color='negative')
    asyncio.ensure_future(post_data())

ui.run(title='Dynamic Blog', port=8000,show=False )


