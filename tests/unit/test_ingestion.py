import pytest
import yaml
import os
from pathlib import Path
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.engine.ingest import IngestEngine
from src.models.content import Ingredient, Decree, Recipe
from src.models.enums import FlavorProfile, CookingMethod


@pytest.fixture
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    yield engine
    await engine.dispose()


@pytest.mark.asyncio
async def test_ingest_all_types(tmp_path, async_engine):
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    ing_data = {
        "id": "void_grain",
        "name": "Void Grain",
        "description": "Grain from the gap",
        "kind": "ingredient",
        "stats": {"elasticity": 80, "flavor_intensity": {"hollow": 100}},
    }
    (content_dir / "ingredient.yaml").write_text(yaml.dump(ing_data))

    dec_data = {
        "id": "decree_01",
        "kind": "decree",
        "target_tag": "grain",
        "operation": "laminate",
        "text_template": "Fold the void...",
        "success_effect": "void_bless",
        "failure_effect": "void_curse",
    }
    (content_dir / "decree.yaml").write_text(yaml.dump(dec_data))

    rec_data = {
        "id": "recipe_01",
        "kind": "recipe",
        "name_pattern": "Void Loaf",
        "process": "laminate",
        "inputs": [{"slot": "flour", "tag_filter": "void"}],
    }
    (content_dir / "recipe.yaml").write_text(yaml.dump(rec_data))

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    engine = IngestEngine(async_engine)
    count = await engine.ingest_directory(content_dir)

    assert count == 3

    async with AsyncSession(async_engine) as session:
        res = await session.execute(
            select(Ingredient).where(Ingredient.id == "void_grain")
        )
        ing = res.scalar_one()
        assert ing.name == "Void Grain"
        assert ing.stats["flavor_intensity"]["hollow"] == 100

        res = await session.execute(select(Decree).where(Decree.id == "decree_01"))

        dec = res.scalar_one()
        assert dec.operation == CookingMethod.LAMINATE

        res = await session.execute(select(Recipe).where(Recipe.id == "recipe_01"))
        rec = res.scalar_one()
        assert rec.name_pattern == "Void Loaf"


@pytest.mark.asyncio
async def test_ingest_invalid_kind(tmp_path, async_engine):
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    bad_data = {"id": "bad", "kind": "unknown_type", "name": "Bad"}
    (content_dir / "bad.yaml").write_text(yaml.dump(bad_data))

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    engine = IngestEngine(async_engine)
    with pytest.raises(ValueError, match="Unknown kind: unknown_type"):
        await engine.ingest_directory(content_dir)


@pytest.mark.asyncio
async def test_ingest_malformed_yaml(tmp_path, async_engine):
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    (content_dir / "broken.yaml").write_text("id: : broken")

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    engine = IngestEngine(async_engine)
    with pytest.raises(yaml.YAMLError):
        await engine.ingest_directory(content_dir)
