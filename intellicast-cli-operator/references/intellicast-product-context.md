# IntelliCast Product Context

Use this file as the shared product and CLI context for `intellicast-cli-operator`.

If the IntelliCast source repository is available, treat its implementation as the ultimate authority. If it is not available in context, use this file as the working baseline.

## What IntelliCast Is

IntelliCast is a macOS screen recording and editing product built around a project bundle format:

- `.intellicast`

The product supports:

- recording screen capture projects
- reopening and editing saved projects
- applying persisted editor settings
- exporting final videos
- capturing screenshots from projects
- traversing undo and redo history

The agent-facing automation surface is the CLI:

- `intellicast-cli`

The preferred automation model is project-level editing, not UI automation.

Source baseline for command definitions:

- `Sources/IntelliCastCLI/main.swift`
- `Sources/IntelliCast/Models/Commands/AgentCommandModels.swift`
- `Sources/IntelliCast/Services/Commands/AgentCommandService.swift`
- `Sources/IntelliCast/Services/Commands/AgentHostControlService.swift`

## Project Model

An IntelliCast project persists as a `.intellicast` bundle.

Key files:

- `project.json`
  - committed `ProjectMetadata`
- `project.autosave.json`
  - autosaved draft `EditingMetadata`
- `history.json`
  - persisted undo/redo stacks
- `media/raw_capture.mp4`
  - primary captured video

Key model split:

- `RecordingMetadata`
  - factual capture data such as duration, resolution, and media availability
- `EditingMetadata`
  - persisted editor choices such as background, frame, zoom, cursor, camera, audio, and segments

## Persistence Boundary

Persistent edits are expected to follow the same path as the editor:

1. `VideoEditorDocument`
2. `ProjectEditingService`
3. `VideoEditConfig`
4. `ProjectHistoryService`
5. commit final `EditingMetadata` back to `project.json`

Do not:

- mutate SwiftUI view state directly
- invent alternate persistence files
- treat render-only overrides as committed project edits

## Current CLI Categories

### Read

- `help`
- `status`
- `inspect`

Purpose:

- read host or project state without modifying persisted editing metadata

### Persistent Edit

- `editor style`
- `editor background`
- `editor cursor`
- `editor camera`
- `editor zoom`
- `editor frame`
- `editor audio`
- `split`
- `undo`
- `redo`

Purpose:

- change what the editor will show next time the project is opened

### Render-only

- `export`
- `screenshot`

Purpose:

- render output from current persisted project state
- may apply temporary render settings
- must not commit edits back to `project.json`

### Project Lifecycle / Host Control

- `record`
- `stop`
- `status`
- `del`

Purpose:

- create, stop, inspect, or remove projects

## Current Editor Command Surface

Prefer narrow commands over composite commands.

Preferred persistent editor commands:

- `editor background`
  - background mode
  - gradient or wallpaper selection
  - solid color
  - blur
  - padding via `screenScale`
  - corner radius
  - shadow intensity
- `editor cursor`
  - auto zoom flag
  - zoom visibility
  - selected zoom level
  - cursor visibility
  - cursor scale
  - cursor style
- `editor camera`
  - camera visibility
  - position
  - size
  - roundedness
  - mirrored
  - shape
  - effect
- `editor zoom`
  - add, update, remove, clear zoom regions
  - region range
  - zoom level
  - focus point
  - enabled state
- `editor frame`
  - resolution
  - aspect ratio
  - frame scale
  - corner radius
- `editor audio`
  - system audio mute
  - microphone mute
  - microphone enhancement

Legacy compatibility command:

- `editor style`

Treat `editor style` as a composite compatibility surface. Prefer the narrower command set above for new automation and future skill improvements.

## Current Top-Level CLI Commands

- `help`
- `record`
- `stop`
- `status`
- `editor style`
- `editor background`
- `editor cursor`
- `editor camera`
- `editor zoom`
- `editor frame`
- `editor audio`
- `inspect`
- `export`
- `screenshot`
- `split`
- `del`
- `undo`
- `redo`

## Inspect Workflow

Agents should default to this sequence:

1. `inspect`
2. choose the smallest matching `editor ...` command
3. `inspect` again to validate persisted state
4. optionally `screenshot` or `export` when visual confirmation is required

Useful inspect sections:

- `summary`
- `editing`
- `history`
- `zoom`

## Safety Guidance For Agents

- Prefer absolute project paths.
- Inspect before making ambiguous edits.
- Modify one semantic category at a time when possible.
- Use `history` or `undo` / `redo` when validating new edit commands.
- Do not promise capabilities that are not present in the current CLI.

## Source Of Truth Files In The IntelliCast Repo

When the main IntelliCast repository is available, these files are the recommended starting point:

- `Sources/IntelliCastCLI/main.swift`
- `Sources/IntelliCast/Services/Commands/AgentCommandService.swift`
- `Sources/IntelliCast/Models/Commands/AgentCommandModels.swift`
- `Sources/IntelliCast/Services/Commands/AgentHostControlService.swift`
- `Sources/IntelliCast/Services/Commands/ProjectCommandLock.swift`
- `docs/cli-editor-consistency.md`
