# DevTrack API

Minimal Django backend for tracking engineering issues.

## What it does
- Tracker for `Reporter` and `Issue` entities using JSON persistence
- REST endpoints to create and query reporters/issues
- Validation through OOP classes (`BaseEntity`, `Reporter`, `Issue`, `CriticalIssue`, `LowPriorityIssue`)
- Priority-specific issue `describe()` message implemented

## Project structure
- `devtrack/` (Django project folder)
- `issues/` (app folder)
  - `models.py`: OOP model classes
  - `views.py`: API logic and persistence to JSON
  - `urls.py`: routing
- `issues.json`, `reporters.json`: data files

## Setup
1. Open terminal in project root: `c:\Users\mansu\OneDrive\Documents\Airtribe Project`
2. Create virtual env (if not already):
   - `python -m venv .venv`
3. Activate:
   - ` .venv\Scripts\activate`
4. Install requirements:
   - `python -m pip install Django==5.2`
5. Apply migrations:
   - `python manage.py migrate`
6. Run server:
   - `python manage.py runserver`

## Endpoints
### Reporter endpoints
- `POST /api/reporters/` - create reporter
- `GET /api/reporters/` - list all reporters
- `GET /api/reporters/?id=<id>` - get reporter by id

### Issue endpoints
- `POST /api/issues/` - create issue
- `GET /api/issues/` - list all issues
- `GET /api/issues/?id=<id>` - get issue by id
- `GET /api/issues/?status=<status>` - filter by status

## Example: create reporter
`curl -X POST http://127.0.0.1:8000/api/reporters/ -H "Content-Type: application/json" -d "{\"id\":1,\"name\":\"Alice\",\"email\":\"alice@example.com\",\"team\":\"backend\"}"`

## Example: create critical issue
`curl -X POST http://127.0.0.1:8000/api/issues/ -H "Content-Type: application/json" -d "{\"id\":1,\"title\":\"Login button not working\",\"description\":\"...\",\"status\":\"open\",\"priority\":\"critical\",\"reporter_id\":1}"`

## Validation rules
- Reporter: name required, email must contain `@`
- Issue: title required, status in `open,in_progress,resolved,closed`, priority in `low,medium,high,critical`
- Duplicate `id` rejected, unknown reporter id on issue creation returns 404

## Design decision
Used `JSON` file persistence in root for simplicity and to match prompt requirements. This avoids DB migration complexity and keeps data readable by Postman tests.

## How to run tests manually
1. `GET http://127.0.0.1:8000/api/reporters/`
2. `GET http://127.0.0.1:8000/api/issues/`
3. Fill in payloads with IDs and verify response codes:
   - 201 for success
   - 400 for validation errors
   - 404 for missing-resource lookup
