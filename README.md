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
from zylo_docs import zylo_docs

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

...
...
...

# 👇 [2/2] Add this at the bottom of your entry point file (e.g., main.py)
zylo_docs(app)
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
<img width="100%" alt="3:7" src="https://github.com/user-attachments/assets/d71a3115-6106-4881-9af8-e1e0972edec6" />


## [4/7] To use Zylo AI, sign up and sign in to zylo.
<p align="center">
  <img width="50%" alt="u-4" src="https://github.com/user-attachments/assets/e7a82d4e-ae17-49e5-bea5-302867fbd58d" />
</p>
To enhance your documentation with AI, please sign in to zylo-docs.

## [5/7] Use the Zylo AI function to upgrade your docs
<img width="100%" alt="5:7" src="https://github.com/user-attachments/assets/87f7f783-e1c1-4437-b3ef-2eabea99477d" />

## [6/7] Tada! Look at the red dot in the top-left corner! It is completed. Let's check this out!
<img width="100%" alt="6:7" src="https://github.com/user-attachments/assets/45561bb3-a4d5-4216-aa4e-c38408a6f6ab" />
After you find the red dot on the version selector, it means that our API specs are now upgraded and more user-friendly with zylo-docs. you can find the lastest one. Once you click it, you can check the new one filled with rich content.

## [6.2/7] Compare the generated docs with the previous version
<video controls muted playsinline loop style="max-width:100%; height:auto;">
  <source src="https://github.com/user-attachments/assets/58370b53-d98c-4cb5-8cd3-b628dd48c1e9" type="video/mp4" />
  Your browser doesn’t support embedded video. 
  <a href="https://github.com/user-attachments/assets/58370b53-d98c-4cb5-8cd3-b628dd48c1e9">Open the video</a>.
</video>

## [6.5/7] Regenerate specific parts, such as test cases
<video controls muted playsinline loop style="max-width:100%; height:auto;">
  <source src="https://github.com/user-attachments/assets/34a0eee7-364e-4572-9930-440c00db7085" type="video/mp4" />
  Your browser doesn’t support embedded video. 
  <a href="https://github.com/user-attachments/assets/34a0eee7-364e-4572-9930-440c00db7085">Open the video</a>.
</video>

## [7/7] Share your API docs with your team
<img width="100%" alt="7:7" src="https://github.com/user-attachments/assets/85bd8986-617a-4a7c-8141-2098ccb14ebf" />

Click the `Publish button`  to share your API documentation via email.

## Development
- Python 3.10+
- FastAPI, Uvicorn

## License

MIT License
