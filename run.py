import subprocess
import sys
import time

print("Starting FastAPI...")

api_process = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "app.api.main:app",
        "--port",
        "8000"
    ]
)

time.sleep(3)

print("Starting Gradio...")

from app.ui.gradio_app import create_gradio_app

app = create_gradio_app()

app.launch(
    server_name="0.0.0.0",
    server_port=7890
)