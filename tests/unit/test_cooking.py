import pytest
from src.engine.cooking import cook
from src.models.content import Ingredient, StatBlock
from src.models.enums import CookingMethod, FlavorProfile


def test_cook_stat_calculation_averages():
    ing1 = Ingredient(
        id="ing1",
        name="Ing 1",
        description="test",
        stats=StatBlock(
            elasticity=50, ph_level=7.0, flavor_intensity={FlavorProfile.SALTY: 100}
        ),
    )
    ing2 = Ingredient(
        id="ing2",
        name="Ing 2",
        description="test",
        stats=StatBlock(
            elasticity=0,
            ph_level=3.0,
            flavor_intensity={FlavorProfile.SALTY: 0, FlavorProfile.SOUR: 50},
        ),
    )

    result = cook([ing1, ing2], CookingMethod.AERATE)

    assert result.stats.elasticity == 25
    assert result.stats.ph_level == 5.0
    assert result.stats.flavor_intensity[FlavorProfile.SALTY] == 50
    assert result.stats.flavor_intensity[FlavorProfile.SOUR] == 25


def test_cook_tag_inheritance_policies():
    ing1 = Ingredient(
        id="ing1",
        name="Ing 1",
        description="test",
        state_tags=["state_raw", "sacred_morgoth", "texture_hard"],
        stats=StatBlock(),
    )
    ing2 = Ingredient(
        id="ing2",
        name="Ing 2",
        description="test",
        state_tags=["texture_soft", "flavor_bitter", "state_cooked"],
        stats=StatBlock(),
    )

    result = cook([ing1, ing2], CookingMethod.SPHERIFY)

    assert "sacred_morgoth" in result.state_tags
    assert "flavor_bitter" in result.state_tags
    assert "state_raw" not in result.state_tags
    assert "state_cooked" in result.state_tags
    assert "texture_hard" not in result.state_tags
    assert "texture_soft" in result.state_tags


def test_cook_ingredient_transformation():
    raw_liver = Ingredient(
        id="raw_liver",
        name="Raw Liver",
        description="test",
        state_tags=["state_raw"],
        stats=StatBlock(ph_level=5.0),
        transforms={CookingMethod.NIXTAMALIZE: "cured_liver"},
    )

    cured_liver_def = Ingredient(
        id="cured_liver",
        name="Cured Liver",
        description="The result of nixtamalization",
        state_tags=["state_cured"],
        stats=StatBlock(ph_level=8.0),
    )

    registry = {"cured_liver": cured_liver_def}

    result = cook([raw_liver], CookingMethod.NIXTAMALIZE, registry=registry)

    assert result.id == "cured_liver_result"
    assert "state_cured" in result.state_tags
    assert "state_raw" not in result.state_tags
    assert result.stats.ph_level == 8.0


def test_cook_stat_ph_averaging_ignores_none():
    ing1 = Ingredient(
        id="ing1",
        name="Ing 1",
        description="test",
        stats=StatBlock(ph_level=4.0),
    )
    ing2 = Ingredient(
        id="ing2",
        name="Ing 2",
        description="test",
        stats=StatBlock(ph_level=None),
    )

    result = cook([ing1, ing2], CookingMethod.AERATE)

    assert result.stats.ph_level == 4.0


def test_cook_tag_remove_policy():
    ing1 = Ingredient(
        id="ing1",
        name="Ing 1",
        description="test",
        state_tags=["state_raw", "sacred_morgoth"],
        stats=StatBlock(),
    )

    result = cook([ing1], CookingMethod.AERATE)

    assert "sacred_morgoth" in result.state_tags
    assert "state_raw" not in result.state_tags
