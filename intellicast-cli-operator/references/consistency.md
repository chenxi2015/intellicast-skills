# IntelliCast CLI Persistence Model

Use the IntelliCast CLI against the same persisted project model as the editor.

Project storage:

- `project.json`
  - committed `ProjectMetadata`
- `project.autosave.json`
  - autosaved draft editing state
- `history.json`
  - undo/redo stacks for `EditingMetadata`

Persistent edit path:

1. `VideoEditorDocument`
2. `ProjectEditingService`
3. `VideoEditConfig`
4. `ProjectHistoryService`
5. commit back to `project.json`

Rules:

- Persistent edit commands must mutate `VideoEditConfig` and commit `EditingMetadata`.
- Do not mutate SwiftUI view state directly.
- `export` and `screenshot` are render-only.
- `undo` and `redo` operate on persisted history.
- `editor style` is legacy compatibility; prefer narrow editor commands.

Current persistent editor commands:

- `editor background`
- `editor cursor`
- `editor camera`
- `editor zoom`
- `editor frame`
- `editor audio`
- `split`

Current read commands:

- `status`
- `inspect`
