# Bread & Bureaucracy Implementation Plan

## TL;DR

> **Quick Summary**: A TUI-based roguelike management simulator where you play an Ogre baker in a corporate dungeon. Built with Python, Textual (TUI), and SQLModel (Data).
>
> **Deliverables**:
> - Playable "Goblin Slums" vertical slice.
> - Data-driven engine (YAML -> SQLite).
> - Real-time "Kitchen" and "Trivia" minigames.
> - "Kafkaesque" UI with stress mechanics.
>
> **Estimated Effort**: Large (Multi-week)
> **Parallel Execution**: YES - 3 Waves
> **Critical Path**: Data Layer -> Core Logic -> TUI Screens

---

## Context

### Original Request
"Review the files in `docs/` and create a high level plan for implementation."

### Interview & Analysis Summary
**Key Decisions**:
- **Tech Stack**: Python 3.11+, Textual (TUI), SQLModel (ORM/Validation), Pytest (Testing).
- **Architecture**: 3-Layer Split (Data/Core/Presentation) to handle Async/Sync mismatch.
- **Data Source**: YAML files are the Source of Truth, ingested into SQLite at runtime.
- **Game Loop**: Real-time (tick-based) for stress mechanics.

**Metis Review Gaps (Addressed)**:
- **Async DB**: Using `SQLModel` with `aiosqlite` to prevent TUI freezing.
- **Testing**: Using `pytest-asyncio` for logic and `Textual Pilot` for UI.
- **Scope**: Limited to "Goblin Slums" content only (5 ingredients, 3 decrees).

---

## Work Objectives

### Core Objective
Build a stable, expandable vertical slice of the "Bread & Bureaucracy" management sim, demonstrating the core loop: Buy -> Bake (Molecular Gastronomy) -> Sell -> Crisis (Trivia).

### Concrete Deliverables
- [ ] `src/models/`: SQLModel definitions sharing schema with YAML.
- [ ] `src/engine/`: Pure Python game logic (Cooking, Decrees).
- [ ] `src/tui/`: Textual application with 5 key screens (Menu, Map, Shift, Crisis, Report).
- [ ] `data/content/`: Initial YAML content for Goblin Slums.

### Definition of Done
- [ ] `pytest` passes with >80% coverage.
- [ ] `python -m src.main` launches the game.
- [ ] Can complete a full shift without crashing.
- [ ] Data persists between runs (SQLite save).

### Must Have
- **Data-Driven Design**: All game content defined in YAML, not hardcoded.
- **Async IO**: Database operations must not block the UI thread.
- **TDD**: Tests written *before* implementation for Core/Data layers.

### Must NOT Have (Guardrails)
- **Custom Scripting Language**: Use Python logic/Enums for Decrees, not a new parser.
- **Multiplayer**: Single-player only.
- **Graphics**: ASCII/TUI only (no images).

---

## Verification Strategy

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
> All verification must be automated via `pytest` and `Textual Pilot`.

### Test Infrastructure
- **Framework**: `pytest` + `pytest-asyncio`
- **UI Testing**: `textual.pilot` (headless browser-like testing for TUI)
- **Data Testing**: `SQLModel` in-memory validation

### Agent-Executed QA Scenarios (Examples)
1. **Ingestion**: Run `python -m src.scripts.ingest --dry-run` -> Exit 0.
2. **Cooking**: Call `cook(ingredients, method)` -> Assert Result Tags match expected.
3. **UI Nav**: Pilot press "Start" -> Assert "Map" screen active.
4. **Trivia**: Pilot selects correct answer -> Assert "Rage" decreases.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation):
├── Task 1: Project Skeleton & CI Setup
├── Task 2: Data Models (SQLModel)
└── Task 3: YAML Ingestion Engine

Wave 2 (Core Logic):
├── Task 4: Molecular Gastronomy Engine (Cooking)
├── Task 5: Decree System (Logic + Trivia Gen)
└── Task 6: Basic TUI Shell (Menu + Layouts)

Wave 3 (Integration):
├── Task 7: Bakery Shift Screen (Real-time Loop)
├── Task 8: Crisis Screen (Trivia Minigame)
└── Task 9: Map & Meta-Progression
```

---

## TODOs

### Wave 1: Foundation & Data

- [x] 1. **Project Skeleton & Test Config**
  **What to do**:
  - Set up directory structure.
  - Create `pyproject.toml` with dependencies: `textual`, `sqlmodel`, `aiosqlite`, `pyyaml`, `pydantic`.
  - Configure `pytest` with `asyncio_mode = auto`.
  - Create hello-world test.
  **Verification**: `pytest` runs and passes 1 dummy test.

- [x] 2. **Core Data Models (SQLModel)**
  **What to do**:
  - Define `Ingredient`, `Decree`, `Recipe` models in `src/models/`.
  - Ensure models work for both Pydantic validation (YAML import) and SQLite (Table).
  - Use Enums for `FlavorProfile`, `Texture`, `CookingMethod`.
  **References**: `docs/DATA_ARCHITECTURE.md` (Schema definitions).
  **Verification**:
  - `pytest tests/unit/test_models.py`: Instantiate models, validate bad data raises ValidationError.

- [x] 3. **YAML Ingestion Engine**
  **What to do**:
  - Create `src/engine/ingest.py`.
  - Implement recursive loading of YAMLs from `data/content/`.
  - Validate against Models.
  - Bulk insert into SQLite (Async).
  **Verification**:
  - Create sample YAML.
  - Run ingestion.
  - Query SQLite: `select count(*) from ingredient` -> Returns expected count.

### Wave 2: Core Game Logic (Pure Python)

- [x] 4. **Molecular Gastronomy Resolver**
  **What to do**:
  - Implement `cook(inputs: List[Ingredient], method: CookingMethod) -> Ingredient`.
  - Implement Tag Inheritance Logic (`tags.yaml` policies: preserve, overwrite, mix).
  - Implement Stat calculation (weighted averages).
  **References**: `docs/GAME_DESIGN_OVERVIEW.md` (Section 6.1).
  **Verification**:
  - Unit Test: Combine "Raw Sludge" + "Heat" -> "Cooked Sludge" (Check tags change).

- [x] 5. **Decree System Logic**
  **What to do**:
  - Implement `Decree` class with predicate evaluation (`check_compliance(item)`).
  - Implement `TriviaGenerator`: Fill templates with logic variables + generate distractors.
  **References**: `docs/DATA_ARCHITECTURE.md` (Section 6).
  **Verification**:
  - Unit Test: Create Decree "No Red Items". Check "Apple" (Fail), "Banana" (Pass).
  - Unit Test: Generate Question. Assert "Apple" is in options.

- [x] 6. **TUI Application Shell**
  **What to do**:
  - Create `src/tui/app.py` (Textual App).
  - Implement `Screen` switching manager.
  - Create `MainMenu` and `Settings` screens.
  - Implement global `GameState` provider (Context).
  **Verification**:
  - `pytest tests/ui/test_shell.py` (Pilot): Launch app, see Menu, Click Quit, App exits.

### Wave 3: Gameplay Implementation

- [x] 7. **Bakery Shift Screen (Real-time)**
  **What to do**:
  - Create `ShiftScreen`.
  - Implement `Customer` spawner (Tick-based).
  - Implement `Counter` widget (Queue visualization).
  - Implement `Kitchen` widget (Appliance slots).
  **References**: `docs/UI_SPECS.md` (Screen 5).
  **Verification**:
  - Pilot Test: Start shift. Wait 5 ticks. Assert Customer count > 0.

- [x] 8. **Crisis Screen (Trivia Minigame)**
  **What to do**:
  - Create `CrisisScreen`.
  - Implement "Wall of Text" `ListView` (Scrollable).
  - Implement `RageMeter` (ProgressBar with auto-increase).
  - Connect to `DecreeSystem` for question generation.
  **References**: `docs/UI_SPECS.md` (Screen 6).
  **Verification**:
  - Pilot Test: Enter Crisis. Select Wrong Answer -> Rage increases. Select Right -> Rage decreases.

- [x] 9. **Map & Meta-Progression**
  **What to do**:
  - **Refactor Main Menu**: Strictly adhere to `docs/UI_SPECS.md` by removing "Map" and "Settlement" buttons. Rename "Start Shift" to "New Shift".
  - **Add Testing Button**: Add a "Testing" button to `MainMenu` (explicit exception to strict UI adherence).
  - **Implement TestingScreen**: A dedicated screen with buttons to trigger simple unit/integration test scripts.
  - **Implement MapScreen**: Allows node selection. Clicking a node (or "Travel") pushes the `ShiftScreen`.
  - **Implement SettlementScreen**: "End of Run" summary. Clicking "Next Assignment" pushes the `MapScreen`.
  - **Update ShiftScreen**: Ensure finishing a shift pushes the `SettlementScreen` (closing the loop).
  - **Save/Load**: Implement persistence using `src/engine/ingest.py` (or new logic) to persist `GameState`.
  **References**: `docs/UI_SPECS.md` (Screens 1, 4 & 7).
  **Verification**:
  - `pytest tests/ui/test_meta.py` (Pilot): Start New Shift -> Map -> Select Node -> Shift -> Finish -> Settlement -> Next -> Map.

### Final Polish

- [ ] 10. **Vertical Slice Content**
  **What to do**:
  - Write `data/content/goblin_slums/manifest.yaml`.
  - Define 5 Ingredients, 3 Recipes, 3 Decrees.
  **Verification**:
  - Run full game loop with this content.

---

## Success Criteria

### Final Checklist
- [ ] `pytest` suite passes (Unit + UI Pilot).
- [ ] Can launch game and navigate to "Shift".
- [ ] "Goblin Slums" data loads correctly.
- [ ] No TUI freezes during DB operations.
