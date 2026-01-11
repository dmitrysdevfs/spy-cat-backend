# Spy Cat Agency Backend

Backend implementation for managing spy cats, missions, and targets for the Spy Cat Agency (SCA).

## Tech Stack
- **Framework**: Django + Django REST Framework
- **Database**: SQLite
- **Environment**: uv (Virtual Environment)
- **Security**: python-dotenv (for environment variables)
- **Formatting/Linting**: ruff

## Quick Start

1. **Install Dependencies**:
   ```bash
   uv install
   ```

2. **Environment Setup**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Set your `DJANGO_SECRET_KEY` and `CAT_API_URL` (default: `https://api.thecatapi.com/v1/breeds`).

3. **Database Migrations**:
   ```bash
   uv run python manage.py migrate
   ```

4. **Create Superuser** (optional, for Admin panel):
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Run Server**:
   ```bash
   uv run python manage.py runserver
   ```

## Running Tests
To run the automated tests, use:
```bash
uv run pytest
```

## API Documentation

### Root
- `GET /` — Welcome message and API status.

### Cats
- `GET /api/cats/` — List all spy cats.
- `POST /api/cats/` — Add a new spy cat (breed validation via TheCatAPI).
- `GET /api/cats/<id>/` — Get single cat details.
- `PATCH /api/cats/<id>/` — Update a cat's salary (only `salary` updates allowed).
- `DELETE /api/cats/<id>/` — Remove a spy cat.

### Missions
- `GET /api/missions/` — List all missions.
- `POST /api/missions/` — Create a mission with targets (1-3 targets required).
- `GET /api/missions/<id>/` — Get mission details.
- `DELETE /api/missions/<id>/` — Delete a mission (forbidden if assigned to a cat).

### Actions
- `PATCH /api/missions/<id>/assign-cat/` — Assign a cat to a mission (cat must be available).
- `PATCH /api/missions/<id>/targets/<target_id>/` — Update target notes or status.
  - *Note: Notes cannot be updated if the target or mission is completed.*

## Formatting and Quality
The project uses `ruff` for code linting and formatting:
```bash
uv run ruff check .
uv run ruff format .
```

## Postman Collection
The Postman collection is located in `/postman/SpyCatAgency.postman_collection.json`.
