from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
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



@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in blog:
        return {"Error": "Пост с таким ID уже существует"}
    blog[item_id] = {
        "title": item.title,
        "author": item.author,
        "keywords": item.keywords
    }

    return blog[item_id]