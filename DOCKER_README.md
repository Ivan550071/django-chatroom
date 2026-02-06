# Django Chatroom - Docker Setup

A real-time chat application built with Django, featuring user authentication, profiles, AJAX messaging, and more.

# Django Chatroom — Docker

This file contains Docker-specific setup and troubleshooting notes for the `django-chatroom` project.

## Prerequisites

- Docker & Docker Compose installed

## Build & Run (quick)

```bash
git clone <your-repo-url>
cd django-chatroom
docker compose up --build
```

The `web` service builds the Django image, runs `collectstatic`, applies migrations and starts Gunicorn on port `8000`.

## Common commands

- View logs:

```bash
docker compose logs -f web
```

- Run a management command:

```bash
docker compose exec web python manage.py <command>
```

- Create superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

- Stop and remove containers:

```bash
docker compose down
```

## Environment variables (examples)

- `SECRET_KEY=your-secret-key`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `DATABASE_URL=postgresql://user:pass@db:5432/chatroom`

These are set in `docker-compose.yml`. For production, prefer a `.env` file or CI secrets.

## Volumes

- `postgres_data` persists Postgres data
- `static_volume` stores collected static files (mapped to `/app/staticfiles` inside the container)

## Access from LAN

1. Ensure `ALLOWED_HOSTS` includes your host IP.
2. Run `docker compose up --build` and open `http://<host-ip>:8000` from another device.

## Troubleshooting

- `Not Found: /static/...` after deploy: ensure `whitenoise` is installed and `STATIC_ROOT` is set (project already configured to collect static files).
- Collectstatic errors complaining about `STATIC_ROOT` not set: set `STATIC_ROOT` in `chatroom/settings.py` to a filesystem path (the repo uses `/app/staticfiles`).
- Port conflicts: update `ports` in `docker-compose.yml`.

## Rebuild fully

```bash
docker compose down -v
docker compose up --build --force-recreate
```
