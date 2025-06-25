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

### Run the FastAPI server locally

After installation, you can run the server using:

```bash
# Using the command line tool
zylo-docs

# Or directly with Python
python -m zylo_docs.main

# Or with uvicorn
uvicorn zylo_docs.main:app --reload
```

The server will start on `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

## License

MIT License
