# Decisions & Rationales

## Tech Stack
- **Textual**: Selected for TUI because of its modern, async-first architecture which fits the "real-time" requirement.
- **SQLModel**: Chosen to unify Data Validation (Pydantic) and Persistence (SQLAlchemy/SQLite) in a single definition.
- **aiosqlite**: Essential for keeping the TUI responsive during DB operations.

## Architecture & Project Structure (2026-02-11)
- **Directory Structure**: Using a standard src/ layout for better package isolation.
- **Async Engine**: Settled on sqlmodel + aiosqlite for asynchronous database operations.
- **Testing Strategy**: Mandated TDD; using pytest-asyncio for async test suites.
- **Enum Naming**: Preferred `Texture` over `TextureProfile` as per user prompt, while retaining definitions from `DATA_ARCHITECTURE.md`.
- **Tag Implementation**: `Ingredient.state_tags` implemented as a `List[str]` (JSON column) to simplify YAML ingestion, while still defining a `Tag` model as requested for global tag management.
- **Embedded StatBlock**: `StatBlock` is defined as a `SQLModel` (without `table=True`) and stored as a JSON column within `Ingredient` to satisfy the "single row" nature of static ingredient definitions.

## YAML Ingestion Engine
- Used 'session.add_all()' for bulk insert of 'SQLModel' objects.
- 'IngestEngine' recursively scans directories for '.yaml' or '.yml' files.
- YAML 'kind' field is used to map to the appropriate 'SQLModel' class ('Ingredient', 'Decree', 'Recipe').
- Implemented robust error handling for malformed YAMLs and validation errors.

## Tag Inheritance & Stats (2026-02-12)
- Implemented specific_tags override in CookingEngine to allow fine-grained control over tag survival (e.g., state_raw should always be removed by any cooking process).
- Decided to average stats only over ingredients that have them to prevent accidental dilution of unique properties, while keeping flavor intensity dilution based on total input count.

## Decree System Architecture
- Decided to use `getattr` with `typing.cast` for dynamic stat checking on `StatBlock` to satisfy type checkers while maintaining flexibility.
- Trivia distractors use simple string manipulation (e.g., 'counter-' prefix) for string values and numeric offsets for numeric values to ensure at least 4 options are always available.

## Crisis Navigation
- **Trigger**: Added a temporary 'c' keybinding to `ShiftScreen` to manually trigger the `CrisisScreen`. This allows for independent testing of the screen transition without waiting for random game events.
- **Logic**: Implemented self-contained timer logic within `CrisisScreen` for the rage meter, ensuring it cleans up (implicit in screen dismissal) and doesn't rely on an external clock for this specific minigame loop.

## Map & Meta-Progression (2026-02-12)
- **Save System**: Chose JSON serialization for `GameState` persistence over SQLite for simplicity and because the game state is currently small and self-contained in a dataclass.
- **State Management**: Used a mutable `GLOBAL_STATE` instance for runtime state to allow easy access across screens, with `dataclasses.asdict` for serialization.
- "New Shift" currently bypasses Character Creation and goes directly to MapScreen to satisfy the immediate "Map & Meta-Progression" task scope.
- Reused existing `src/engine/save.py` for persistence instead of implementing new logic in `ingest.py` as it already satisfied requirements.

## Testing Screen
- **Exception**: Added a `Testing` button to `MainMenu` and a `TestingScreen` to allow manual triggering of unit tests/scripts from within the TUI, as requested by the user. This is an explicit deviation from `docs/UI_SPECS.md` for development convenience.
