import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any
from src.models.content import Ingredient, StatBlock
from src.models.enums import CookingMethod, TagPolicy, FlavorProfile


class CookingEngine:
    def __init__(self, ingredient_registry: Optional[Dict[str, Ingredient]] = None):
        self.registry = ingredient_registry or {}
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        config_path = Path("data/config/tags.yaml")
        if config_path.exists():
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def cook(self, inputs: List[Ingredient], method: CookingMethod) -> Ingredient:
        if not inputs:
            raise ValueError("Cooking requires at least one input ingredient.")

        transformed_inputs = self._transform_inputs(inputs, method)

        base_ingredient = transformed_inputs[0]
        for i, original in enumerate(inputs):
            if original.id != transformed_inputs[i].id:
                base_ingredient = transformed_inputs[i]
                break

        stats = self._calculate_stats(transformed_inputs)
        tags = self._inherit_tags(transformed_inputs)

        return Ingredient(
            id=f"{base_ingredient.id}_result",
            name=f"{method.value.capitalize()} {base_ingredient.name}",
            description=f"Result of {method.value} operation.",
            stats=stats,
            state_tags=tags,
        )

    def _transform_inputs(
        self, inputs: List[Ingredient], method: CookingMethod
    ) -> List[Ingredient]:
        transformed = []
        for ing in inputs:
            if method in ing.transforms:
                new_id = ing.transforms[method]
                if new_id in self.registry:
                    transformed.append(self.registry[new_id])
                else:
                    transformed.append(ing)
            else:
                transformed.append(ing)
        return transformed

    def _get_tag_policy(self, tag: str) -> TagPolicy:
        specific = self.config.get("specific_tags", {})
        if tag in specific:
            return TagPolicy(specific[tag])

        categories = self.config.get("tag_categories", {})
        for _, data in categories.items():
            prefix = data.get("prefix")
            if prefix and tag.startswith(prefix):
                return TagPolicy(data.get("policy"))
        return TagPolicy(self.config.get("default_policy", "preserve"))

    def _get_category(self, tag: str) -> Optional[str]:
        categories = self.config.get("tag_categories", {})
        for cat, data in categories.items():
            prefix = data.get("prefix")
            if prefix and tag.startswith(prefix):
                return cat
        return None

    def _inherit_tags(self, inputs: List[Ingredient]) -> List[str]:
        output_tags = set()

        for ing in inputs:
            for tag in ing.state_tags:
                policy = self._get_tag_policy(tag)
                if policy in [TagPolicy.PRESERVE, TagPolicy.MIX]:
                    output_tags.add(tag)
                elif policy == TagPolicy.OVERWRITE:
                    category = self._get_category(tag)
                    if category:
                        output_tags = {
                            t for t in output_tags if self._get_category(t) != category
                        }
                    output_tags.add(tag)
                elif policy == TagPolicy.REMOVE:
                    if tag in output_tags:
                        output_tags.remove(tag)

        return sorted(list(output_tags))

    def _calculate_stats(self, inputs: List[Ingredient]) -> StatBlock:
        num = len(inputs)

        def avg(values: List[Optional[float]]) -> Optional[float]:
            present = [v for v in values if v is not None]
            if not present:
                return None
            return sum(present) / len(present)

        def avg_int(values: List[Optional[int]]) -> Optional[int]:
            v = avg([float(x) if x is not None else None for x in values])
            return round(v) if v is not None else None

        flavor_sums: Dict[FlavorProfile, float] = {}
        for ing in inputs:
            stats = self._get_stats_obj(ing)
            for f, intensity in stats.flavor_intensity.items():
                flavor_sums[f] = flavor_sums.get(f, 0.0) + intensity

        return StatBlock(
            elasticity=avg_int([self._get_stats_obj(i).elasticity for i in inputs]),
            plasticity=avg_int([self._get_stats_obj(i).plasticity for i in inputs]),
            friability=avg_int([self._get_stats_obj(i).friability for i in inputs]),
            ph_level=avg([self._get_stats_obj(i).ph_level for i in inputs]),
            water_activity=avg([self._get_stats_obj(i).water_activity for i in inputs]),
            flavor_intensity={f: round(i / num) for f, i in flavor_sums.items()},
        )

    def _get_stats_obj(self, ingredient: Ingredient) -> StatBlock:
        if isinstance(ingredient.stats, dict):
            return StatBlock(**ingredient.stats)
        return ingredient.stats


def cook(
    inputs: List[Ingredient],
    method: CookingMethod,
    registry: Optional[Dict[str, Ingredient]] = None,
) -> Ingredient:
    engine = CookingEngine(registry)
    return engine.cook(inputs, method)
