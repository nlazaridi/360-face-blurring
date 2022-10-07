from config import settings

IP = settings.gunicorn.ip
PORT = settings.gunicorn.port
TIMEOUT = settings.gunicorn.timeout
WORKERS = settings.gunicorn.workers

bind = f"{IP}:{PORT}"
timeout = TIMEOUT
workers = WORKERS
worker_class = settings.gunicorn.worker_class
