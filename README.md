<div align="center"> 
   <img width="772" height="280" alt="zylo-docs" src="https://github.com/user-attachments/assets/3c4c24ac-708a-42d5-b673-90c8b3cd0816" />
   <br />
   <b><em>Build the world’s best API docs highly integrated with FastAPI for developers</em></b>
</div>
<p align="center">

<a href="" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/zylo-docs?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---
**Writing technical documentation like API specs is often a burden for software engineers — it’s not their expertise, and rarely a top priority. That’s where Zylo-docs comes in. Zylo-docs seamlessly integrates with FastAPI and automatically generates OpenAPI-compliant specs. With powerful AI assistance, it helps developers create clear, user-friendly, and rich documentation with minimal effort. Think of it as a more intuitive, AI-powered alternative to Swagger.**

## [1/7] Get Started (Add boilerplate code)
```python
from fastapi import FastAPI
# 👇 [1/2] Add this import at the top
from zylo_docs.integration import add_zylo_docs

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# ...
# ...
# ...

# 👇 [2/2] Add this at the bottom of your entry point file (e.g., main.py)
add_zylo_docs(app)
```


## [2/7] Run the FastAPI Server
```python
uvicorn main:app --reload
```
You need to start the server using **Uvicorn**.

> ⚡️ **If your server is already running, you can skip this step.**

**Once the server is running, open your browser and go to: 👉 [http://localhost:8000/zylo-docs](http://localhost:8000/zylo-docs)** </br>
(⚠️ If your development server runs on a different port, update the URL accordingly!)

## [3/7] Tada! You can now view beautifully structured API specs with zylo-docs.
<img width="100%" alt="Screenshot 2025-07-30 at 9 01 27 AM" src="https://github.com/user-attachments/assets/5d88e0ca-d5f4-4227-9c2b-aaa7dda65f78" />

## [4/7] To use Zylo AI, sign up and sign in to zylo.
<p align="center">
  <img width="50%" alt="Screenshot 2025-07-30 at 9 04 09 AM" src="https://github.com/user-attachments/assets/9097918a-4e02-4ea8-b6de-de58f6f36bf9" />
</p>
To enhance your documentation with AI, please sign in to zylo-docs.

## [5/7] Use the Zylo AI function to upgrade your docs
<img width="100%" alt="zylo-docs-magic-wand" src="https://github.com/user-attachments/assets/249146b4-9e46-423d-90c1-c2f4c4aa3f09" />
Click the `magic wand icon` in the top-right corner to activate Zylo AI, which will generate detailed descriptions and test cases for each of your API endpoints.

## [6/7] Tada! Look at the red dot in the top-left corner! It is completed. Let's check this out!
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/ab1e6402-6bdc-43bc-971e-a44afac1786e" />
After you find the red dot on the version selector, it means that our API specs are now upgraded and more user-friendly with zylo-docs. you can find the lastest one. Once you click it, you can check the new one filled with rich content.


## [7/7] Share your API docs with your team
<img width="100%" alt="Screenshot 2025-07-30 at 9 10 47 AM" src="https://github.com/user-attachments/assets/d9d261af-1157-4f55-bc0c-e85b8885f104" />

Click the `Publish button`  to share your API documentation via email.

## Development
- Python 3.10+
- FastAPI, Uvicorn

## License

MIT License
