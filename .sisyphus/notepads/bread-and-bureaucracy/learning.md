# Learnings & Patterns

## TUI Testing
- Using `app.screen.query_one` with `await pilot.pause()` is effective for simulating user interactions in Textual.
- Testing screen transitions requires ensuring the screen stack is properly managed (`push_screen`, `pop_screen`).

## Meta-Progression
- Implementing a closed loop (Map -> Shift -> Settlement -> Map) simplifies the game flow and allows for easier integration testing.
- Keeping `GLOBAL_STATE` mutable but serializable via `dataclasses.asdict` works well for simple game states.
