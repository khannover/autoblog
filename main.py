from nicegui import app, ui, run
import httpx

# Define a function to create the header of the application.
def header():
    """
    Creates a header for the NiceGUI application with the title "Autoblog".

    This function uses NiceGUI's UI elements to create a header section
    and add a label with the text "Autoblog" to it. The header is set to
    span the full width of the page.
    """
    with ui.header().classes("w-full"):
        # Create a label with the text "Autoblog" and set its font size to 2xl.
        ui.label("Autoblog").classes("text-2xl")


# Define the main page (index) of the application.
@ui.page("/")
async def index():
    """
    The main index page of the application.

    This function is decorated with @ui.page("/") which means it will
    be the content displayed when the user visits the root URL ("/")
    of the application.

    currently, this is an empty page. We can add content here.
    """
    header()

    with ui.row().classes("w-full items-center"):
        prompt = ui.textarea("Prompt").classes("w-full border-re").props("outlined")
        ui.button("Send", icon="send", on_click=lambda: send_prompt(prompt.value, response_label))
    ui.separator()
    response_label = ui.markdown().bind_content(app.storage.general, "prompt_response")


async def send_prompt(prompt: str, response_label: ui.label):
    """
    Sends a prompt to the Ollama API and updates the UI with the streaming response.
    """
    app.storage.general["prompt_response"] = ""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://ollama:11434/api/generate",
            json={"model": "tulu3:8b", "prompt": prompt, "stream": True},
            timeout=None,
        ) as response:
            async for chunk in response.aiter_lines():
                try:
                    import json
                    data = json.loads(chunk)
                    app.storage.general["prompt_response"] += data["response"]
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON chunk: {chunk}")






# Start the NiceGUI application.
ui.run(
    port=8001,  # Specify the port the application should run on.
    show=False,  # Disable automatically opening the application in a browser.
    storage_secret="s3cr3t",  # Set a secret key for secure storage.
    dark=True  # Enable dark mode for the UI.
)
from nicegui import app, ui, run
import httpx

# Define a function to create the header of the application.
def header():
    """
    Creates a header for the NiceGUI application with the title "Autoblog".

    This function uses NiceGUI's UI elements to create a header section
    and add a label with the text "Autoblog" to it. The header is set to
    span the full width of the page.
    """
    with ui.header().classes("w-full"):
        # Create a label with the text "Autoblog" and set its font size to 2xl.
        ui.label("Autoblog").classes("text-2xl")


# Define the main page (index) of the application.
@ui.page("/")
async def index():
    """
    The main index page of the application.

    This function is decorated with @ui.page("/") which means it will
    be the content displayed when the user visits the root URL ("/")
    of the application.

    currently, this is an empty page. We can add content here.
    """
    header()

    with ui.row().classes("w-full items-center"):
        prompt = ui.textarea("Prompt").classes("w-full border-re").props("outlined")
        ui.button("Send", icon="send", on_click=lambda: send_prompt(prompt.value, response_label))
    ui.separator()
    response_label = ui.markdown().bind_content(app.storage.general, "prompt_response")


async def send_prompt(prompt: str, response_label: ui.label):
    """
    Sends a prompt to the Ollama API and updates the UI with the streaming response.
    """
    app.storage.general["prompt_response"] = ""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://ollama:11434/api/generate",
            json={"model": "tulu3:8b", "prompt": prompt, "stream": True},
            timeout=None,
        ) as response:
            async for chunk in response.aiter_lines():
                try:
                    import json
                    data = json.loads(chunk)
                    app.storage.general["prompt_response"] += data["response"]
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON chunk: {chunk}")






# Start the NiceGUI application.
ui.run(
    port=8001,  # Specify the port the application should run on.
    show=False,  # Disable automatically opening the application in a browser.
    storage_secret="s3cr3t",  # Set a secret key for secure storage.
    dark=True  # Enable dark mode for the UI.
)
