from enum import Enum
from fastapi import FastAPI, Path, Body, Form, File, Header, Cookie, status, Response, HTTPException
from os import path
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse

from pydantic import BaseModel

app = FastAPI()


class UserType(str, Enum):
 STANDARD = "standard"
 ADMIN = "admin"

class Post(BaseModel):
 title: str

class PublicPost(BaseModel):
 title: str


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# # Path to validate number params
# @app.get("/users/{id}")
# async def get_user(id: int = Path(..., ge=5)): 
#  return {"id": id}

# # @app.get("/users/{type}/{id}/")
# # async def get_user(type: str, id: int):
# #  return {"type": type, "id": id}

# @app.get("/users/{type}/{id}/")
# async def get_user(type: UserType, id: int):
#  return {"type": type, "id": id}


# @app.get("/license-plates/{license}")
# async def get_license_plate(license: str = Path(..., min_length=5, max_length=9)):
#  return {"license": license}

# # This is for body post request
# # @app.post("/users")
# # async def create_user(name: str = Body(...), age: int = 
# # Body(...)):
# #  return {"name": name, "age": age}


# @app.post("/users")
# async def create_user(name: str = Form(...), age: int = Form(...)):
#  return {"name": name, "age": age}


# @app.post("/files")
# async def upload_file(file: bytes = File(...)):
#  return {"file_size": len(file)}


# # @app.post("/files")
# # async def upload_multiple_files(files: List[UploadFile] = File(...)):
# #  return [
# #  {"file_name": file.filename, "content_type": file.content_type}
# #  for file in files
# #  ]


# @app.get("/")
# async def get_header(hello: str = Header(...)):
#  return {"hello": hello}


# # @app.get("/")
# # async def get_cookie(hello: Optional[str] = Cookie(None)):
# #  return {"hello": hello}




# # Dummy database
# posts = {
#  1: Post(title="Hello", nb_views=100),
# }

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#  posts.pop(id, None)
#  return None


# # Dummy database
# posts = {
#  1: Post(title="Hello", nb_views=100),
# }

# @app.get("/posts/{id}", response_model=PublicPost)
# async def get_post(id: int):
#  return posts[id]


# # Custom headers
# @app.get("/")
# async def custom_header(response: Response):
#  response.headers["Custom-Header"] = "Custom-Header-Value"
#  return {"hello": "world"}


# #Setting cookies
# @app.get("/")
# async def custom_cookie(response: Response):
#  response.set_cookie("cookie-name", "cookie-value", max_age=86400)
#  return {"hello": "world"}


# updating status code and creating a new if an id is not existing
# Dummy database
posts = {
 1: Post(title="Hello", nb_views=100),
}

@app.put("/posts/{id}")
async def update_or_create_post(id: int, post: Post, response: Response):
 if id not in posts:
    response.status_code = status.HTTP_201_CREATED
 posts[id] = post
 return posts[id]


#  HTTPException Password example
@app.post("/password")
#                                        Definition that contains the raw data
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
 if password != password_confirm:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail={
        "message": "Passwords don't match.",
        "hints": [
        "Check the caps lock on your keyboard",
        "Try to make the password visible by clicking on the eye icon to check your typing",
        ],
        },
        )
 return {"message": "Passwords match."}



#-------------------------------------------------------------------------
# Custom content-type
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
        <html>
            <head>
                <title>Hello world!</title>
            </head>
            <body>
                <h1>Hello world!</h1>
            </body>
        </html>
    """
# Custom content-type
@app.get("/text", response_class=PlainTextResponse)
async def text():
 return "Hello world!"


# redirection content-type
@app.get("/redirect")
async def redirect():
 return RedirectResponse("/new-url")

@app.get("/redirect")
async def redirect():
 return RedirectResponse("/new-url", status_code=status.HTTP_301_MOVED_PERMANENTLY)

# fileresponse content-type
@app.get("/cat")
async def get_cat():
 root_directory = path.dirname(path.dirname(__file__))
 picture_path = path.join(root_directory, "assets", "cat.jpg")
 return FileResponse(picture_path)


#custom content-type
@app.get("/xml")
async def get_xml():
 content = """<?xml version="1.0" encoding="UTF-8"?><Hello>World</Hello>"""
 return Response(content=content, media_type="application/xml")