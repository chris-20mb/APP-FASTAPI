from typing import Union

from fastapi import Response, Cookie, FastAPI, status, Header
from pydantic import BaseModel
from datetime import UTC, datetime
from typing import Annotated

app = FastAPI()

fake_db = [
    {'title': 'Criando uma aplicação com Django', 'date': datetime.now(UTC), 'published': True}, 
    {'title': 'Criando uma aplicação com FastAPI', 'date': datetime.now(UTC), 'published': False},
    {'title': 'Criando uma aplicação com Flask', 'date': datetime.now(UTC), 'published': True}, 
    {'title': 'Criando uma aplicação com Pandas', 'date': datetime.now(UTC), 'published': False},
]


class Post(BaseModel):
    title: str
    date: datetime = datetime.now(UTC)
    published: bool = False
    author: str

@app.post('/posts/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    fake_db.append(post.model_dump())
    return post


@app.get('/posts')
def read_posts(response: Response, published: bool, limit: int, skip: int = 0, ads_id: Annotated[str | None, Cookie()] = None, user_agent: Annotated[str | None, Header()] = None):
    response.set_cookie(key='user', value='chris@gmail.com')
    print(f'Cookie: {ads_id}')
    print(f'User-agent: {user_agent}')
    posts = []
    for post in fake_db:
        if len(posts) == limit:
            break
        if post["published"] is published:
            posts.append(post)

    return posts        

@app.get("/posts/{framework}")
def read_framework_posts(framework: str):
    return {
        "posts": [
            {'title': f'Criando uma aplicação com {framework}', 'date': datetime.now(UTC)}, 
            {'title': f'Internacionalizando uma app {framework}', 'date': datetime.now(UTC)},
        ]
    }


