# Learnings & Patterns

## Tech Stack
- **Framework**: Textual (Async TUI)
- **Data**: SQLModel (Async SQLite via aiosqlite)
- **Testing**: pytest-asyncio + textual.pilot

## Architecture
- **Layer 1: Data**: `src/models/` (SQLModel). Shared schema for YAML validation and DB persistence.
- **Layer 2: Engine**: `src/engine/` (Pure Python). Business logic, decoupled from UI.
- **Layer 3: UI**: `src/tui/` (Textual). Presentation layer, communicates with Engine/Data.

## Conventions
- **Async**: DB operations must be async to prevent UI freezing.
- **Verification**: TDD is mandatory. Write tests before implementation.
- **Config**: Configuration via `pyproject.toml`.
## Project Setup (2026-02-11)
- Established core directory structure (src/, tests/, data/content/).
- Configured pytest-asyncio with asyncio_mode = auto for transparent async test support.
- Added asyncio_default_fixture_loop_scope = 'function' to pyproject.toml to suppress warnings and ensure consistent test behavior.

## Data Models (2026-02-12)
- **SQLModel & JSON Columns**: Using `sa_column=Column(JSON)` allows `SQLModel` to store complex types (List, Dict) in SQLite while maintaining Pydantic validation during instantiation/ingestion.
- **TDD for Models**: Unit tests using `pytest` and `pydantic.ValidationError` are effective for verifying schema constraints (e.g., `ge`, `le` on `StatBlock`).
- **Embedded Models**: `StatBlock` is embedded within `Ingredient` as a JSON column, rather than a separate table, to simplify the schema for this vertical slice.
- **Enums**: Renamed `TextureProfile` to `Texture` for brevity.
- **SQLite JSON Retrieval**: When retrieving models with `Column(JSON)` from SQLite, the fields are returned as `dict` objects (or `list`), not Pydantic models. Engine logic must handle this (e.g., re-instantiating `StatBlock(**ing.stats)` if needed).

## Cooking Engine (2026-02-11)
- Implemented `CookingEngine` with `cook` function.
- Tag Inheritance: Uses `data/config/tags.yaml` to define policies (preserve, overwrite, mix).
- Stat Calculation: Implements weighted averages for all `StatBlock` fields and flavor intensities.
- Transformation Logic: Ingredients can transform into new IDs based on the `CookingMethod`.
- Gotcha: `Ingredient.stats` returns a `dict` at runtime when loaded from SQLite/SQLModel via JSON column. The engine now explicitly converts these to `StatBlock` objects for consistent processing.

## Cooking Engine (2026-02-12)
- Stat calculation (pH, elasticity, etc.) uses uniform averaging over ingredients that actually possess the stat (ignoring None values). This prevents "dilution" of stats by ingredients that don't have them (e.g., adding salt shouldn't halve the pH of the water if salt has no pH defined).
- Flavor intensity, however, is diluted by the total number of ingredients (sum / total_inputs) to reflect volume/mass dilution.
- Tag inheritance supports PRESERVE, MIX, OVERWRITE, and REMOVE policies.
- specific_tags in tags.yaml can override category-level prefix policies.

## Decree System Logic (2026-02-12)
- Implemented `check_compliance` to support various requirement types: `has_tag`, `has_no_tag`, `stat_gt`, `stat_lt`, and `texture_is`.
- Implemented `generate_question` using `text_template` and `token_keys` for procedural trivia generation.
- Procedural distractors are created by mutating requirement values or using generic bureaucratic failure messages.

## TUI Application Shell (2026-02-12)
- **Screen Navigation**: Textual's `push_screen` and `pop_screen` work seamlessly for standard menu navigation.
- **Testing**:
    - **Querying**: `app.query_one` often targets the default screen or fails to find elements on pushed screens. **Solution**: Use `app.screen.query_one(...)` to reliably target elements on the *active* screen.
    - **Timing**: `await pilot.pause()` is critical after `push_screen` or `pop_screen` to ensure the DOM has updated before assertions.
    - **Types**: `Button.label` returns a `rich.text.Text` object. Tests must cast to `str` for comparison (`str(button.label)`).

## Bakery Shift Screen (2026-02-12)
- **Real-time Updates**: `set_interval(1.0, ...)` in `on_mount` allows periodic logic (customer spawning) without blocking the UI.
- **Reactive UI**: Using `reactive` attributes on widgets (`queue_count = reactive(0)`) combined with `watch_queue_count` allows the UI to automatically update when state changes.
- **Testing**: Integration tests need to handle timing. `await pilot.pause(1.5)` was sufficient to let `set_interval(1.0)` fire.

## Crisis Screen Implementation (2026-02-12)
- **Decree Token Keys**: The `Decree` model's `token_keys` dictionary must map the *raw* placeholder name (e.g., "val") to the requirement field key, NOT the placeholder with braces (e.g., "{val}"), because `str.format` uses kwargs matching the raw name.
- **Testing UI Logic**: `pilot.pause(1.1)` was necessary to test time-based rage accumulation effectively.

## Map & Meta-Progression (2026-02-12)
- **Textual Testing**: `Label` widgets store their content in an internal structure. `label.render()` is a reliable way to get the displayed content for assertions in tests, returning a `RenderResult` that can be stringified.
- **Screen Navigation in Tests**: `pilot.app.screen.query_one(...)` is more reliable than `pilot.app.query_one(...)` when multiple screens are involved, as it targets the currently active screen specifically.
- **State Persistence**: Using `dataclasses.asdict` with `json` provides a simple and effective way to save/load game state for early prototypes without the overhead of a database.
- Textual's screen stack (/) effectively manages the game loop (Menu -> Map -> Shift -> Settlement -> Map).
-  property is useful for conditionally available menu options like "Resume Shift".
- Textual's screen stack (`push_screen`/`pop_screen`) effectively manages the game loop (Menu -> Map -> Shift -> Settlement -> Map).
- `Button.disabled` property is useful for conditionally available menu options like "Resume Shift".
## Regression Management - Feb 12 2026
- Fixed UI tests failing due to MainMenu refactor.
- Renamed #start_shift to #new_shift in tests/ui/test_shell.py and tests/ui/test_shift.py.
- Updated tests/ui/test_shift.py to handle the new MapScreen navigation step between MainMenu and ShiftScreen.
- All 29 tests now passing.
