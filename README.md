# autoblog

# Dynamic Blog Engine

A Python blog engine using FastAPI, NiceGUI, and Ollama to generate dynamic content based on LLM prompts.

## Features

- **Dynamic Content Generation**: Store prompts instead of static content, generating fresh content on each request.
- **FastAPI Backend**: Serves API endpoints for creating and retrieving posts.
- **NiceGUI Frontend**: Provides a user-friendly interface for interacting with the blog.
- **Ollama Integration**: Runs language models locally, eliminating external API dependencies.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Adding Blog Posts](#adding-blog-posts)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/dynamic-blog-engine.git
cd dynamic-blog-engine
```

### Build the Docker Image

```bash
docker build -t dynamic-blog .
```

## Usage

### Run the Docker Container

```bash
docker run -p 8000:8000 -p 8001:8001 dynamic-blog
```

### Run with Docker Compose

```bash
docker-compose up -d --build
```
**Note:** The first time you run the container, Ollama may take some time to set up.

## Access the Application

  - Frontend (NiceGUI): Open your browser and navigate to http://localhost:8001.
  - Backend (FastAPI): API endpoints are available at http://localhost:8000.






