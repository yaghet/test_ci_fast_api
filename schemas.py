from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseRecipe(BaseModel):
    title: str = Field(title="Recipe Title", description="The name of the recipe.")
    cooking_time: float = Field(
        title="Cooking Time",
        description="Cooking time in minutes.",
    )

    @field_validator("cooking_time")
    def validate_cooking_time(cls, value):
        if value <= 0:
            raise ValueError("Cooking time must be greater than 0.")
        return value


class RecipeFromTop(BaseRecipe):
    views: int = Field(
        title="Number of Views",
        description="Number of views. The higher the number of views, the higher the recipe in the top.",
    )


class InRecipe(BaseRecipe):
    ingredients: Optional[str] = Field(
        title="List of Ingredients",
        description="List of ingredients as a text.",
        default=None,
    )
    description: Optional[str] = Field(
        title="Description of the Recipe",
        description="Description of the recipe as a text.",
        default=None,
    )


class IdOfRecipe(InRecipe):
    recipe_id: int = Field(
        title="Primary Key",
        description="ID of the recipe in the database (primary key).",
    )

    model_config = ConfigDict(from_attributes=True)
