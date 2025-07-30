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

## Getting Started
```python
# Please declare it like this.
from zylo_docs.integration import add_zylo_docs

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"
    
# You need to add the following code at the bottom of your entry point file
add_zylo_docs(app)
```


## Running the FastAPI Server (http:\/\/localhost\:8000\/zylo-docs)
```python
uvicorn main:app --reload
```
You need to start the server using **Uvicorn**.

**After launching the server, navigate to http:\/\/localhost\:8000\/zylo-docs in your browser.** </br>
(If the development server port changes, the port number in the execution command must also change)

<img width="100%" alt="Screenshot 2025-07-30 at 9 01 27 AM" src="https://github.com/user-attachments/assets/5d88e0ca-d5f4-4227-9c2b-aaa7dda65f78" />

## Sign up and sign in zylo


<p align="center">
  <img width="50%" alt="Screenshot 2025-07-30 at 9 04 09 AM" src="https://github.com/user-attachments/assets/9097918a-4e02-4ea8-b6de-de58f6f36bf9" />

</p>
To use the Zylo ai service, please sign in.

## Use zylo-docs ai function
<img width="100%" alt="zylo-docs-magic-wand" src="https://github.com/user-attachments/assets/249146b4-9e46-423d-90c1-c2f4c4aa3f09" />


By clicking the magic wand icon in the blue square, you can use Zylo AI to generate descriptions and test cases for your API documentation.

## Sharing API docs
<img width="100%" alt="Screenshot 2025-07-30 at 9 10 47 AM" src="https://github.com/user-attachments/assets/d9d261af-1157-4f55-bc0c-e85b8885f104" />

Click the `Publish button`  to share your API documentation with anyone you want.

## Development
- Python 3.10+
- FastAPI, Uvicorn

## License

MIT License
