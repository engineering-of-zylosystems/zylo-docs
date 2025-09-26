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

## [1/10] Get Started (Add boilerplate code)

```python
from fastapi import FastAPI
# 👇 [1/2] Add this import at the top
from zylo_docs import zylo_docs

app = FastAPI()
# 👇 [2/2] Add this your entry point file (e.g., main.py)
zylo_docs(app)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

...
...
...


```

## [2/10] Run the FastAPI Server

```python
uvicorn main:app --reload
```

You need to start the server using **Uvicorn**.

> ⚡️ **If your server is already running, you can skip this step.**

**Once the server is running, open your browser and go to: 👉 [http://localhost:8000/zylo-docs](http://localhost:8000/zylo-docs)** </br>
(⚠️ If your development server runs on a different port, update the URL accordingly!)

## [3/10] Tada! You can now view beautifully structured API specs with zylo-docs.
<img width="100%" alt="Screenshot 2025-09-26 at 11 09 16 AM" src="https://github.com/user-attachments/assets/653463d6-b6a6-4ed9-8173-9cdea508ffad" />

## [4/10] To use Zylo AI, sign up and sign in to zylo.

<p align="center">
  <img width="50%" alt="u-4" src="https://github.com/user-attachments/assets/e7a82d4e-ae17-49e5-bea5-302867fbd58d" />
</p>
To enhance your documentation with AI, please sign in to zylo-docs.

## [5/10] Provide context to the zylo-docs AI
Context example
```
Our pet store is called "Patricia", and the pet_id represents the registered number of the pet. This should be reflected in the API specs.
```
<img width="100%" alt="Screenshot 2025-09-26 at 11 11 00 AM" src="https://github.com/user-attachments/assets/f0252159-e72a-4f24-8d9b-a8ae5fc58478" />

Describe how you would like zylo-docs to enrich the document.

## [6/10] Use the Zylo AI function to upgrade your docs

<img width="100%" alt="Screenshot 2025-09-26 at 11 12 18 AM" src="https://github.com/user-attachments/assets/c0e3d730-dc58-4317-b28c-754090212797" />

## [7/10] Tada! Look at the red dot in the top-left corner! It is completed. Let's check this out!

<img width="100%" alt="Screenshot 2025-09-26 at 12 02 33 PM" src="https://github.com/user-attachments/assets/57093d56-15e8-4f3e-a86a-37c32af058c0" />

After you find the red dot on the version selector, it means that our API specs are now upgraded and more user-friendly with zylo-docs. you can find the lastest one. Once you click it, you can check the new one filled with rich content.

## [8/10] Compare the generated docs with the previous version

<img width="100%" src="https://github.com/user-attachments/assets/8b168555-f5fc-4117-b4c4-4ebf4979b8d7"/>


## [9/10] Regenerate specific parts, such as test cases

<img width="100%" src="https://github.com/user-attachments/assets/18780cb7-c513-4acf-9d31-80900c585a52" />


## [10/10] Share your API docs with your team

<img width="100%" alt="Screenshot 2025-09-26 at 12 58 58 PM" src="https://github.com/user-attachments/assets/da7b21d2-5f52-4b66-9772-3774f0cf135c" />

Click the `Publish button` to share your API documentation via email.
- Note : Use authentication to test the token.
  -  Use x-api by entering the key name and key value
  -  Use HTTP Bearer by entering the Bearer token value.
  <img width="100%" src="https://github.com/user-attachments/assets/99d547c9-d3fe-44d5-9a6d-258801e68991" />


## Development

- Python 3.10+
- FastAPI, Uvicorn

## License

MIT License


