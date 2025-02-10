# gui.py

from nicegui import ui
import aiohttp
import asyncio

API_URL = 'http://localhost:8000'

def main():
    # Index page displaying the list of posts
    @ui.page('/')
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

    ui.run(title='Dynamic Blog', port=8001)

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


if __name__ == '__main__':
    main()
