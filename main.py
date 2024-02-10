from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    author: str
    keywords: list | None = None


blog = {
    1: {
        "title": "Пишем API на Python",
        "author": "artur123",
        "keywords": ["API", "блог",  "FastAPI"],
    },
    2: {
        "title": "Используем словари для храниения данных",
        "author": "roma321",
        "keywords": ["Python", "словарь", "данные"],
    },
    3: {
        "title": "Операции со множествами",
        "author": "artur123",
        "keywords": ["множество", "Python", "данные"],
    },
}

@app.get("/")
def home():
    return {"Data":"test"}


@app.get("/about")
def about():
    return {"Data": "about the project"}


@app.get("/post/{post_id}")
def get_post(post_id: int):
    if post_id not in blog:
        return {"Error": "Пост с таким ID не существует"}
    return blog[post_id]

# параметры
@app.get("/query/")
def get_post(keyword: str | None = None, author: str | None = None):
    posts = []
    for post_id in blog:
        if keyword:
            keywords = [w.lower() for w in blog[post_id]["keywords"]]
            if keyword in keywords:
                posts.append(blog[post_id])
        if author:
            if author == blog[post_id]["author"]:
                posts.append(blog[post_id])
        
    return posts



@app.post("/create-post/{post_id}")
def create_post(post_id: int, post: Post):
    if post_id in blog:
        return {"Error": "Пост с таким ID уже существует"}
    blog[post_id] = {
        "title": post.title,
        "author": post.author,
        "keywords": post.keywords
    }

    return blog[post_id]


@app.put("/update-post/{post_id}")
def update_post(post_id: int, post: Post):
    if post_id not in blog:
        return {"Error": "Пост с таким ID не существует"}
    blog[post_id].update(post)
    return blog[post_id]

@app.delete("/delete-post/{post_id}")
def delete_post(post_id: int, post: Post):
    if post_id not in blog:
        return {"Error": "Пост с таким ID не существует"}
    del blog[post_id]
    return {"Success": "Пост успешно удален"}


