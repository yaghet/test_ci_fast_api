from contextlib import asynccontextmanager
from typing import List, Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_engine, get_db
from models import Base, Recipe
from schemas import IdOfRecipe, InRecipe, RecipeFromTop


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    path="/recipes",
    response_model=IdOfRecipe,
    status_code=status.HTTP_201_CREATED,
    tags=["Recipes 🍔"],
    summary="Add a recipe to database",
)
async def add_recipe(
    recipe: InRecipe, session: Annotated[AsyncSession, Depends(get_db)]
) -> IdOfRecipe:
    """Добавляет новый рецепт в базу данных."""
    new_recipe = Recipe(**recipe.model_dump())

    async with session.begin():
        session.add(new_recipe)
        await session.commit()

    return new_recipe


@app.get(
    path="/recipes",
    response_model=List[RecipeFromTop],
    tags=["Recipes 🍔"],
    summary="List all recipes from database sorted by views and cooking time",
)
async def get_list_recipes(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> List[RecipeFromTop]:
    """Возвращает список рецептов, отсортированных по просмотрам и времени приготовления."""
    async with session.begin():
        res = await session.execute(
            select(Recipe.title, Recipe.views, Recipe.cooking_time).order_by(
                Recipe.views.desc(), Recipe.cooking_time
            )
        )
        results = res.all()

        return [
            RecipeFromTop(title=title, views=views, cooking_time=cooking_time)
            for title, views, cooking_time in results
        ]


@app.get(
    path="/recipes/{recipe_id}",
    response_model=IdOfRecipe,
    tags=["Recipes 🍔"],
    summary="Get a specific recipe from database by ID",
)
async def get_recipe(
    recipe_id: int, session: Annotated[AsyncSession, Depends(get_db)]
) -> IdOfRecipe:
    """Возвращает рецепт по его ID и увеличивает количество просмотров."""
    async with session.begin():
        res = await session.execute(select(Recipe).where(Recipe.recipe_id == recipe_id))

        result = res.scalars().first()
        if result:
            try:
                result.views += 1
                session.add(result)
                await session.commit()
                return result
            except Exception:
                raise HTTPException(status_code=500, detail="Failed to update recipe.")
        raise HTTPException(status_code=404, detail="Recipe not found.")
