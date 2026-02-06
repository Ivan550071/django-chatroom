# Django Chatroom

A small chat application built with Django featuring user authentication, chat rooms, AJAX messaging, and user profiles.

## Quick Start (Docker)

Prerequisites: Docker & Docker Compose installed.

1. Clone the repo and enter the folder:

```bash
git clone <your-repo-url>
cd django-chatroom
```

2. Build and start:

```bash
docker compose up --build
```

3. Open your browser to `http://localhost:8000`.

Notes: the compose setup starts a Postgres service, runs migrations and collects static files.

## Quick Start (Local, venv)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies and run migrations:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Environment variables

- `SECRET_KEY` — Django secret key (set in Docker or host env)
- `ALLOWED_HOSTS` — comma-separated hosts (default: `localhost,127.0.0.1`)
- `DATABASE_URL` — optional (Postgres URL when not using default SQLite)

For Docker, these are defined in `docker-compose.yml`.

## Docker-specific notes

- Static files are served via WhiteNoise; the Docker image runs `collectstatic` automatically.
- To create a superuser inside the running container:

```bash
docker compose exec web python manage.py createsuperuser
```

To stop and remove containers:

```bash
docker compose down
```

See [DOCKER_README.md](DOCKER_README.md) for detailed Docker instructions and troubleshooting tips.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Open a pull request

## License

MIT
