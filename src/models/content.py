from typing import List, Dict, Optional, Any, Union
from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, Relationship
from .enums import FlavorProfile, CookingMethod


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


class StatBlock(SQLModel):
    elasticity: Optional[int] = Field(default=None, ge=0, le=100)
    plasticity: Optional[int] = Field(default=None, ge=0, le=100)
    friability: Optional[int] = Field(default=None, ge=0, le=100)
    ph_level: Optional[float] = Field(default=None, ge=0, le=14)
    water_activity: Optional[float] = Field(default=None, ge=0, le=1)
    flavor_intensity: Dict[FlavorProfile, int] = Field(default_factory=dict)


class Ingredient(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    description: str
    kind: str = Field(default="ingredient")
    state_tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    stats: StatBlock = Field(sa_column=Column(JSON))
    transforms: Dict[CookingMethod, str] = Field(
        default_factory=dict, sa_column=Column(JSON)
    )


class Decree(SQLModel, table=True):
    id: str = Field(primary_key=True)
    kind: str = Field(default="decree")
    target_tag: str
    operation: CookingMethod
    requirements: List[Dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSON)
    )
    text_template: str
    token_keys: Dict[str, str] = Field(default_factory=dict, sa_column=Column(JSON))
    success_effect: str
    failure_effect: str


class Recipe(SQLModel, table=True):
    id: str = Field(primary_key=True)
    kind: str = Field(default="recipe")
    name_pattern: str
    inputs: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    process: CookingMethod
    base_stats: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


ContentObject = Union[Ingredient, Decree, Recipe]
