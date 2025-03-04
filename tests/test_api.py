import pytest
from models import Recipe
from sqlalchemy import select


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", ["/recipes", "/recipes/1"])
async def test_api_get_routes(async_client, endpoint):
    response = await async_client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_recipe(async_client):
    data_recipe = {
        "title": "New recipe",
        "cooking_time": 2.2,
        "ingredients": "Any",
        "description": "New recipe",
    }
    response = await async_client.post("/recipes", json=data_recipe)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_api_with_params(async_db):
    recipe = Recipe(title="Any", cooking_time=2.4, ingredients="Any", description="Wow")
    async_db.add(recipe)
    await async_db.commit()
    result = await async_db.execute(select(Recipe).filter_by(title="Any"))
    added_recipe = result.scalars().first()

    assert added_recipe.title == "Any"
    assert added_recipe.views == 0
