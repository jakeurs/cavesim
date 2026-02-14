import pytest
from pydantic import ValidationError
from src.models.content import Ingredient, StatBlock, Decree, Recipe
from src.models.enums import FlavorProfile, CookingMethod


def test_stat_block_validation():
    # Valid StatBlock
    stats = StatBlock(
        elasticity=50, ph_level=7.0, flavor_intensity={FlavorProfile.SALTY: 10}
    )
    assert stats.elasticity == 50

    # Invalid elasticity (too high)
    with pytest.raises(ValidationError):
        StatBlock(elasticity=101)

    # Invalid ph_level (too low)
    with pytest.raises(ValidationError):
        StatBlock(ph_level=-1)


def test_ingredient_validation():
    # Valid Ingredient
    stats = StatBlock(flavor_intensity={FlavorProfile.BITTER: 80})
    ing = Ingredient(
        id="eel_liver",
        name="Eel Liver",
        description="Bitter organ",
        stats=stats,
        state_tags=["raw", "organ"],
        transforms={CookingMethod.NIXTAMALIZE: "eel_liver_cured"},
    )
    assert ing.id == "eel_liver"
    assert ing.stats.flavor_intensity[FlavorProfile.BITTER] == 80


def test_decree_validation():
    decree = Decree(
        id="decree_rot_01",
        target_tag="sacred_rot",
        operation=CookingMethod.INOCULATE,
        requirements=[{"type": "temperature_below", "value": 20}],
        text_template="Rot-Mother blesses...",
        token_keys={"max_temp": "value"},
        success_effect="add_tag:blessed_by_rot",
        failure_effect="add_tag:cursed_by_rot",
    )
    assert decree.id == "decree_rot_01"


def test_recipe_validation():
    recipe = Recipe(
        id="neon_gut_bomb",
        name_pattern="{Adjective} Sludge-Sphere",
        inputs=[{"slot": "base", "tag_filter": "aerated"}],
        process=CookingMethod.SPHERIFY,
        base_stats={"flavor_intensity": {"chroma": 50}},
    )
    assert recipe.id == "neon_gut_bomb"
