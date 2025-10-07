install:
	uv sync

lint:
	uv run ruff check

fix:
	uv run ruff check --fix

dev:
	uv run manage.py runserver

start:
	uv run gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh
#uv sync --frozen && uv cache prune --ci
