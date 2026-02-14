import os
import yaml
from pathlib import Path
from typing import List, Dict, Type
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from src.models.content import Ingredient, Decree, Recipe


class IngestEngine:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        self.models: Dict[str, Type[SQLModel]] = {
            "ingredient": Ingredient,
            "decree": Decree,
            "recipe": Recipe,
        }

    async def ingest_directory(self, directory: Path) -> int:
        count = 0
        objects = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    file_path = Path(root) / file
                    obj = self._load_file(file_path)
                    objects.append(obj)
                    count += 1

        if objects:
            await self._bulk_insert(objects)

        return count

    def _load_file(self, file_path: Path) -> SQLModel:
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Malformed YAML in {file_path}: {e}") from e

        if not isinstance(data, dict):
            raise ValueError(f"YAML in {file_path} must be a dictionary")

        kind = data.get("kind")
        if not kind:
            raise ValueError(f"Missing 'kind' in {file_path}")

        model_cls = self.models.get(kind)
        if not model_cls:
            raise ValueError(f"Unknown kind: {kind}")

        try:
            return model_cls(**data)
        except Exception as e:
            raise ValueError(f"Validation failed for {file_path}: {e}") from e

    async def _bulk_insert(self, objects: List[SQLModel]):
        async with AsyncSession(self.engine) as session:
            session.add_all(objects)
            await session.commit()
