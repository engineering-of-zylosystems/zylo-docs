# project description

<div align="center"> 
   <img width="772" height="280" alt="zylo-docs" src="https://github.com/user-attachments/assets/3c4c24ac-708a-42d5-b673-90c8b3cd0816" />
   <br />
   <b><em>build the world’s best API docs highly integrated with FastAPI for developers</em></b>
</div>
<p align="center">

<a href="" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/zylo-docs?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---
**zylo-docs is built on FastAPI and automatically generates APIs written by users, adds descriptions using AI, and even supports API testing**

## A Simple Example
```python
# zylo-docs boilerplate
from zylo_docs.integration import add_zylo_docs

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"

# Add at the bottom
add_zylo_docs(app)
```

## Running the FastAPI Server
```python
uvicorn main:app --reload
```
After starting the server, open your browser and visit the root URL followed by **/zylo-docs**.

<img width="1497" height="802" alt="스크린샷 2025-07-29 오후 4 58 33" src="https://github.com/user-attachments/assets/1a4712ea-7fc0-40cb-8da0-0997d2159676" />

## sign up and sign in zylo


<p align="center">
  <img src="https://github.com/user-attachments/assets/11dc4408-a772-4783-886a-f65881654673" height="500px" />
  <img src="https://github.com/user-attachments/assets/3ce01104-c784-43e3-a0e0-6dcb54a4d128" height="500px" />
</p>
To use the Zylo service, please sign up or sign in.

## use zylo-AI function
<img width="1186" height="896" alt="Frame 9" src="https://github.com/user-attachments/assets/7719a629-18af-4f46-9581-b1b54deb3a0d" />

By clicking the magic wand icon, you can use Zylo AI to generate descriptions and test cases for your API documentation.

## Development

- Python 3.10+
- FastAPI, Uvicorn

## License

MIT License
