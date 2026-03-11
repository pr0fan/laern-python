# Workout Tracker API

## Description

Api for the home workout plan app

## Technologies

Programming language - python
Framework - FastAPI
HTTP server - uvicorn
Database - MongoDb
Db driver - Motor

## Install and run

Install packages:

```bash
pip install fastapi uvicorn motor python-dotenv
```

Run: 
```bash
python -m uvicorn main:app --reload
```

## Endpoints
| Method | URL | Description |
|--------|-----|-------------| 
| GET | /exercises | Get all exercises |
| POST | /exercises | Add new exercise |
| GET | /exercises/summary | Get summary exercises |
| GET | /exercises/heaviest | Get heaviest exercise |
| GET | /exercises/{category} | Get exercises by category |

Example request:

curl -X 'GET' \
  'http://127.0.0.1:8000/exercises' \
  -H 'accept: application/json'

Response: 
```json
[
  {
    "_id": "69b1397d05082799fa56aac8",
    "name": "Тяга",
    "weight": 120,
    "category": "Спина"
  },
  {
    "name": "Приседания",
    "weight": 116,
    "category": "Ноги",
    "_id": "69b14c7b89fb42b4ac1385a1"
  }
]
```

## Env example

MONGODB_URL=mongoServUrl
