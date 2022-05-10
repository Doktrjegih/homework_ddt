from typing import Dict, List, Union

import pytest
import requests
from pydantic import BaseModel, ValidationError, StrictStr, conlist


class AllDogs(BaseModel):
    message: Dict[StrictStr, List[StrictStr]]
    status = "success"


class DogsCount(BaseModel):
    message: Union[conlist(StrictStr, min_items=2, max_items=50), StrictStr]
    status = "success"


class DogsBreed(BaseModel):
    message: List[StrictStr]
    status = "success"


class OneSubBreed(BaseModel):
    message: StrictStr
    status = "success"


def test_validate_all_breeds():
    url = "https://dog.ceo/api/breeds/list/all"
    response = requests.get(url)
    try:
        AllDogs.validate(response.json())
    except ValidationError:
        pytest.fail()


@pytest.mark.parametrize("dogs_count", (1, 2, 100))
def test_check_min_max_random_images(dogs_count):
    url = "https://dog.ceo/api/breeds/image/random"
    if dogs_count > 1:
        url += f"/{dogs_count}"
    response = requests.get(url)
    try:
        DogsCount.validate(response.json())
    except ValidationError:
        pytest.fail()


@pytest.mark.parametrize("breed", ("mastiff", "retriever", "terrier"))
def test_validate_certain_breed(breed):
    url = "https://dog.ceo/api/breed/breed-&/images"
    response = requests.get(url.replace("breed-&", breed))
    try:
        DogsBreed.validate(response.json())
    except ValidationError:
        pytest.fail()


def test_success_status_code():
    url = "https://dog.ceo/api/breed/hound/afghan/images/random"
    response = requests.get(url)
    assert response.status_code == 200


def test_validate_certain_sub_breed():
    url = "https://dog.ceo/api/breed/hound/afghan/images/random"
    response = requests.get(url)
    try:
        OneSubBreed.validate(response.json())
    except ValidationError:
        pytest.fail()
