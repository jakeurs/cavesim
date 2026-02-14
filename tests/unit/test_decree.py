import pytest
from src.models.content import Ingredient, Decree, StatBlock
from src.models.enums import CookingMethod, FlavorProfile
from src.engine.decree import check_compliance, generate_question


def test_check_compliance_tag_requirement():
    decree = Decree(
        id="test_decree",
        target_tag="sacred",
        operation=CookingMethod.AERATE,
        requirements=[{"type": "has_tag", "value": "pure", "token_key": "purity_tag"}],
        text_template="Must have {purity_tag} tag.",
        token_keys={"purity_tag": "value"},
        success_effect="none",
        failure_effect="none",
    )

    item_ok = Ingredient(
        id="item1",
        name="Item OK",
        description="test",
        state_tags=["pure", "sacred"],
        stats=StatBlock(),
    )
    assert check_compliance(item_ok, decree) is True

    item_fail = Ingredient(
        id="item2",
        name="Item Fail",
        description="test",
        state_tags=["sacred"],
        stats=StatBlock(),
    )
    assert check_compliance(item_fail, decree) is False


def test_check_compliance_stat_requirement():
    decree = Decree(
        id="stat_decree",
        target_tag="delicate",
        operation=CookingMethod.EMULSIFY,
        requirements=[
            {"type": "stat_gt", "stat": "ph_level", "value": 5.0, "token_key": "min_ph"}
        ],
        text_template="pH must be above {min_ph}.",
        token_keys={"min_ph": "value"},
        success_effect="none",
        failure_effect="none",
    )

    item_ok = Ingredient(
        id="item1",
        name="Item OK",
        description="test",
        state_tags=["delicate"],
        stats=StatBlock(ph_level=6.0),
    )
    assert check_compliance(item_ok, decree) is True

    item_fail = Ingredient(
        id="item2",
        name="Item Fail",
        description="test",
        state_tags=["delicate"],
        stats=StatBlock(ph_level=4.0),
    )
    assert check_compliance(item_fail, decree) is False


def test_generate_question():
    decree = Decree(
        id="test_decree",
        target_tag="sacred",
        operation=CookingMethod.AERATE,
        requirements=[{"type": "has_tag", "value": "pure", "token_key": "purity_tag"}],
        text_template="Must have {purity_tag} tag.",
        token_keys={"purity_tag": "value"},
        success_effect="none",
        failure_effect="none",
    )

    question_data = generate_question(decree)
    assert "question" in question_data
    assert "options" in question_data
    assert "answer" in question_data

    assert question_data["answer"] == "Must have pure tag."
    assert question_data["answer"] in question_data["options"]
    assert len(question_data["options"]) == 4

    distractors = [o for o in question_data["options"] if o != question_data["answer"]]
    assert len(distractors) == 3
    assert "Must have counter-pure tag." in distractors


def test_check_compliance_has_no_tag():
    decree = Decree(
        id="no_tag_decree",
        target_tag="pure",
        operation=CookingMethod.STERILIZE,
        requirements=[{"type": "has_no_tag", "value": "tainted"}],
        text_template="Must not be tainted.",
        token_keys={},
        success_effect="none",
        failure_effect="none",
    )

    item_ok = Ingredient(
        id="item1",
        name="Item OK",
        description="test",
        state_tags=["pure"],
        stats=StatBlock(),
    )
    assert check_compliance(item_ok, decree) is True

    item_fail = Ingredient(
        id="item2",
        name="Item Fail",
        description="test",
        state_tags=["pure", "tainted"],
        stats=StatBlock(),
    )
    assert check_compliance(item_fail, decree) is False


def test_check_compliance_stat_lt():
    decree = Decree(
        id="stat_lt_decree",
        target_tag="stable",
        operation=CookingMethod.EMULSIFY,
        requirements=[{"type": "stat_lt", "stat": "water_activity", "value": 0.5}],
        text_template="Water activity must be below 0.5.",
        token_keys={},
        success_effect="none",
        failure_effect="none",
    )

    item_ok = Ingredient(
        id="item1",
        name="Item OK",
        description="test",
        state_tags=["stable"],
        stats=StatBlock(water_activity=0.3),
    )
    assert check_compliance(item_ok, decree) is True

    item_fail = Ingredient(
        id="item2",
        name="Item Fail",
        description="test",
        state_tags=["stable"],
        stats=StatBlock(water_activity=0.7),
    )
    assert check_compliance(item_fail, decree) is False
