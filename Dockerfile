FROM zauberzeug/nicegui:latest

COPY main.py /app/main.py

CMD ["python", "/app/main.py"]