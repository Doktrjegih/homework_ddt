from typing import List, Literal

import pytest
import requests
from pydantic import BaseModel, ValidationError, StrictStr, parse_obj_as, StrictInt


class AllPosts(BaseModel):
    userId: StrictInt
    id: StrictInt
    title: StrictStr
    body: StrictStr


class SingleBrewerie(BaseModel):
    id: Literal["madtree-brewing-cincinnati"]


@pytest.mark.parametrize("count_posts", (100, 101))
def test_only_one_hundred_posts(count_posts):
    url = f"https://jsonplaceholder.typicode.com/posts/{count_posts}"
    response = requests.get(url)
    if count_posts == 100:
        assert response.status_code == 200
    else:
        assert response.status_code == 404


def test_validate_all_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    try:
        parse_obj_as(List[AllPosts], response.json())
    except ValidationError:
        pytest.fail()


def test_create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    data = '{"userId":1,"title":"foo","body":"bar"}'
    response = requests.post(
        url=url, data=data, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201, "Пост не добавлен"


def test_patch_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    data = '{"title":"foo","body":"bar"}'
    response = requests.patch(
        url=url, data=data, headers={"Content-Type": "application/json"}
    )
    print(response.json())
    assert (
        response.json()["title"] == "foo" and response.json()["body"] == "bar"
    ), "Пост не обновлен"


@pytest.mark.parametrize("user", (1, 5, 10))
@pytest.mark.parametrize("page", ("albums", "todos", "posts"))
def test_check_data_from_users(user, page):
    url = f"https://jsonplaceholder.typicode.com/users/{user}/{page}"
    response = requests.get(url)
    assert response.json() != [], f"Нет данных да странице {page} у пользователя {user}"
