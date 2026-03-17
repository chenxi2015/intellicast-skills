---
name: intellicast-cli-operator
description: Operate IntelliCast projects through the supported `intellicast-cli` command surface. Use when an agent needs to inspect a `.intellicast` project, apply persistent editor changes, export or capture output, manage undo/redo history, or control recording without touching SwiftUI view state.
---

# IntelliCast CLI Operator

Use the IntelliCast CLI as the source of truth for agent-driven project operations.

## Core Rules

- Read project state first with `inspect` before changing anything material.
- Prefer narrow persistent commands:
  - `editor background`
  - `editor cursor`
  - `editor camera`
  - `editor zoom`
  - `editor frame`
  - `editor audio`
- Treat `editor style` as legacy compatibility only.
- Use `undo` and `redo` for persisted history traversal.
- Do not mutate SwiftUI view state or invent alternate project persistence.
- Keep edits aligned with the persisted project model described in [references/consistency.md](references/consistency.md).

## CLI Location

Try these paths in order:

1. `build/DerivedDataCLI/Build/Products/Debug/intellicast-cli`
2. `build/Export/IntelliCast.app/Contents/Resources/intellicast-cli`

If neither exists, build the CLI from the repo root:

```bash
xcodebuild -project IntelliCast.xcodeproj -scheme IntelliCastCLI -configuration Debug -derivedDataPath build/DerivedDataCLI build CODE_SIGNING_ALLOWED=NO
```

## Default Workflow

### 1. Inspect

Use JSON output to decide what to change:

```bash
intellicast-cli inspect -f /path/to/project.intellicast --section summary
intellicast-cli inspect -f /path/to/project.intellicast --section editing
intellicast-cli inspect -f /path/to/project.intellicast --section history
intellicast-cli inspect -f /path/to/project.intellicast --section zoom
```

### 2. Apply persistent edits

Use the smallest command that matches the requested change.

Examples:

```bash
intellicast-cli editor background -f /path/to/project.intellicast --background-mode solid --background-color '#1E7AF0' --background-blur 24
intellicast-cli editor cursor -f /path/to/project.intellicast --show-cursor false --cursor-scale 1.8 --cursor-type glow
intellicast-cli editor camera -f /path/to/project.intellicast --camera-position tm --camera-size 0.31 --camera-effect comic
intellicast-cli editor zoom -f /path/to/project.intellicast --action add --start 1.0 --end 3.5 --zoom-level 2.2 --focus 0.25,0.75
intellicast-cli editor frame -f /path/to/project.intellicast --aspect_ratio 16:9 --screen-scale 0.9
intellicast-cli editor audio -f /path/to/project.intellicast --mute-system-audio true
```

### 3. Validate

After edits, read back the affected section:

```bash
intellicast-cli inspect -f /path/to/project.intellicast --section editing
intellicast-cli inspect -f /path/to/project.intellicast --section zoom
intellicast-cli inspect -f /path/to/project.intellicast --section history
```

When output matters, optionally validate with:

```bash
intellicast-cli screenshot -f /path/to/project.intellicast --time 00:01
intellicast-cli export -f /path/to/project.intellicast
```

## Command Selection

- Use `inspect --section summary` to check recording facts, history counts, and draft presence.
- Use `inspect --section editing` when a caller needs raw persisted `EditingMetadata`.
- Use `inspect --section history` before or after undoable workflows.
- Use `inspect --section zoom` before changing zoom regions.
- Use `split` only for persisted segment edits.
- Use `screenshot` and `export` as render-only commands.
- Use `record`, `stop`, and `status` for host recording control.
- Use `del` only when the user explicitly wants project deletion.

## Safety

- Prefer absolute project paths.
- Assume commands are persistent unless they are clearly render-only.
- If a change is ambiguous, inspect first and modify one category at a time.
- If validating a new command surface, confirm both `project.json` and `history.json` semantics through `inspect`.

## References

- Read [references/consistency.md](references/consistency.md) for the persistence model and command classification.
- Read [references/commands.md](references/commands.md) for the supported command surface and examples.
