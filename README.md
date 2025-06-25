# Zylo Docs

The world's best API docs for developers.

## Installation

### From PyPI (when published)
```bash
pip install zylo-docs
```

### From source
```bash
git clone https://github.com/yourusername/zylo-docs.git
cd zylo-docs
pip install -e .
```

## Usage

### Integrate with your FastAPI app

Zylo Docs is a FastAPI plugin that adds a custom HTML-based API documentation UI at the `/zylo` route.

**Example:**
```python
from fastapi import FastAPI
from zylo_docs.integration import mount_zylo_docs

app = FastAPI(title="My API")

@app.get("/users")
async def get_users():
    return {"users": ["user1", "user2"]}

# Integrate Zylo Docs UI with a single line
mount_zylo_docs(app)
```

### Run the Zylo Docs server (for development/testing)

You can run the Zylo Docs server in two ways:

**1. Using the CLI (recommended for quick start):**
```bash
zylo-docs --reload
```

**2. Using uvicorn directly:**
```bash
uvicorn zylo_docs.main:app --reload
```

### Access Zylo Docs
- Zylo UI: [http://localhost:8000/zylo](http://localhost:8000/zylo)
- OpenAPI Spec: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- Your API: [http://localhost:8000/users](http://localhost:8000/users)

### How it works
- The UI served at `/zylo` is located at `zylo_docs/static/zylo-docs.html`.
- Zylo Docs automatically loads your FastAPI OpenAPI spec from `/openapi.json` and displays it in the UI.
- You can integrate Zylo Docs into any FastAPI app with a single line.

## Development
- Python 3.8+
- FastAPI, Uvicorn

## License

MIT License
