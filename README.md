# Back-End-Development-Pictures

Flask REST service for the IBM Back-end Application Development Capstone Project. Created from the official IBM template; all supplied API tests are retained.

## Environment setup

Run `bash bin/setup.sh`, then `source .venv/bin/activate`. The setup script creates an isolated `.venv` using the installed Python 3.10+ interpreter (the container uses Python 3.11). The original template's unrelated PostgreSQL setup and unused dependencies have been removed.

Start locally with `flask --app app run --port 5001`. Run `pytest` for the course tests.

## API

- `GET /health`: service status.
- `GET /count`: picture count, including zero for an empty collection.
- `GET /picture` and `GET /picture/<id>`: list and retrieve.
- `POST /picture`: create (201), duplicate ID (302, as required by the course contract).
- `PUT /picture/<id>`: replace an existing picture (200).
- `DELETE /picture/<id>`: remove (204); missing IDs return 404.

A picture has an integer `id`, HTTP(S) `pic_url`, and string fields `event_country`, `event_state`, `event_city`, `event_date`. Invalid input returns 400/415. IDs cannot change during update.

The course uses an in-memory list seeded from `backend/data/pictures.json`; changes reset when the process restarts and are not shared across replicas. Use a single replica/worker for this exercise. This unauthenticated educational API must not contain private data.

## Container

`docker build -t pictures .`

`docker run --rm -p 3000:3000 pictures`

The container uses Gunicorn on port 3000 and runs as an unprivileged user. Deploy to the course-provided IBM Code Engine project.

## Setup verification

This repository was created from the [official course template](https://github.com/ibm-developer-skills-network/luggb-Back-End-Development-Pictures). On 2026-10-30, `bash bin/setup.sh` completed successfully (exit status 0) with Python 3.12, installed all requirements, and produced the activation instructions for `.venv`.

The original course lab refers to Python 3.9 and a named virtual environment. This implementation uses Python 3.10+ and the repository-local `.venv` to support its current Flask dependencies; the deployed container uses Python 3.11.
