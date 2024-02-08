from fastapi import FastAPI

app = FastAPI()

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


@app.get("/keyword/{keyword}")
def get_post(keyword: str):
    posts = []
    for post in blog:
        keywords = [w.lower() for w in blog[post]["keywords"]]
        if keyword in keywords:
            posts.append(blog[post])
    return posts
