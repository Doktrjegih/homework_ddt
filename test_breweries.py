from typing import List, Union, Literal

import pytest
import requests
from pydantic import BaseModel, ValidationError, StrictStr, parse_obj_as


class AllBreweries(BaseModel):
    country: StrictStr
    phone: Union[StrictStr, None]


class SingleBrewerie(BaseModel):
    id: Literal["madtree-brewing-cincinnati"]


def test_country_and_phone_in_breweries():
    url = "https://api.openbrewerydb.org/breweries"
    response = requests.get(url)
    try:
        parse_obj_as(List[AllBreweries], response.json())
    except ValidationError:
        pytest.fail()


@pytest.mark.parametrize(
    "alias, city",
    (("san_diego", "San Diego"), ("boring", "Boring"), ("new_york", "New York")),
)
def test_breweries_by_city(alias, city):
    url = f"https://api.openbrewerydb.org/breweries?by_city={alias}"
    response = requests.get(url)
    for brewerie in response.json():
        assert brewerie["city"] == city, "Город неправильный"


@pytest.mark.parametrize("search", ("cooper", "dog", "beer"))
def test_breweries_by_name(search):
    url = f"https://api.openbrewerydb.org/breweries?by_name={search}"
    response = requests.get(url)
    for brewerie in response.json():
        assert search in (brewerie["name"]).lower(), f"Имя не содержит {search}"


def test_single_brewerie():
    url = "https://api.openbrewerydb.org/breweries/madtree-brewing-cincinnati"
    response = requests.get(url)
    try:
        SingleBrewerie.validate(response.json())
    except ValidationError:
        pytest.fail()


def test_autocomplete_not_city():
    url = "https://api.openbrewerydb.org/breweries/autocomplete?query=dog"
    response = requests.get(url)
    for brewerie in response.json():
        if "city" in brewerie.keys():
            pytest.fail()
