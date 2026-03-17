---
name: intellicast-cli-operator
description: Inspect, edit, validate, render, delete, and control IntelliCast projects through the supported `intellicast-cli` command surface. Use when a request involves a `.intellicast` bundle, IntelliCast CLI mode, CLI help, persisted editor settings, project.json or history.json state, background or cursor or camera or zoom or frame or audio edits, split changes, undo or redo, screenshots or export, legacy `editor style`, or host commands such as record, stop, status, or explicit project deletion.
---

# IntelliCast CLI Operator

Use the IntelliCast CLI as the source of truth for agent-driven project operations.

## Read Order

1. Read [references/intellicast-product-context.md](references/intellicast-product-context.md) first for product scope and CLI capability boundaries.
2. Read [references/commands.md](references/commands.md) when selecting the exact command form, supported options, enums, or aliases.
3. Read [references/consistency.md](references/consistency.md) when validating persistence, history, or render-only behavior.

## CLI Location

Try these paths in order:

1. `build/DerivedDataCLI/Build/Products/Debug/intellicast-cli`
2. `build/Export/IntelliCast.app/Contents/Resources/intellicast-cli`

If neither exists, build the CLI from the repo root:

```bash
xcodebuild -project IntelliCast.xcodeproj -scheme IntelliCastCLI -configuration Debug -derivedDataPath build/DerivedDataCLI build CODE_SIGNING_ALLOWED=NO
```

## Core Rules

- Use the CLI and persisted project model as the source of truth.
- Do not mutate SwiftUI view state or invent alternate persistence files.
- Read project state with `inspect` before changing anything material.
- Prefer the smallest narrow command that matches the requested change.
- Treat `help` and [references/commands.md](references/commands.md) as the complete command inventory.
- Treat `editor style` as legacy compatibility only.
- Treat `export` and `screenshot` as render-only.
- Use `undo` and `redo` only for persisted history traversal.
- Use `del` only when the user explicitly asks to delete a project.

## Required Workflow

### 1. Inspect First

Start from the smallest relevant read command. Use JSON output to decide what to change.

```bash
intellicast-cli status
intellicast-cli inspect -f /path/to/project.intellicast --section summary
intellicast-cli inspect -f /path/to/project.intellicast --section editing
intellicast-cli inspect -f /path/to/project.intellicast --section history
intellicast-cli inspect -f /path/to/project.intellicast --section zoom
```

Choose sections deliberately:

- Use `summary` for recording facts, draft presence, and high-level project state.
- Use `editing` for persisted `EditingMetadata`.
- Use `history` before or after undoable workflows.
- Use `zoom` before changing zoom regions.

### 2. Edit Narrowly

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

Prefer this mapping:

- background or frame changes: inspect `editing`
- cursor, camera, or audio changes: inspect `editing`
- zoom changes: inspect `zoom` and then `history`
- split, undo, or redo: inspect `history` and then `editing` when needed
- record, stop, or status: use `status`

### 3. Validate Persisted State

Read back the affected section immediately after each edit.

```bash
intellicast-cli inspect -f /path/to/project.intellicast --section editing
intellicast-cli inspect -f /path/to/project.intellicast --section zoom
intellicast-cli inspect -f /path/to/project.intellicast --section history
```

If the user cares about visuals or rendered output, validate with a render-only command after the persisted state looks correct.

```bash
intellicast-cli screenshot -f /path/to/project.intellicast --time 00:01
intellicast-cli export -f /path/to/project.intellicast
```

## Command Selection

- Use `help` when you need a quick human-readable command summary from the CLI itself.
- Use `inspect --section summary` to check recording facts, history counts, and draft presence.
- Use `inspect --section editing` when a caller needs raw persisted `EditingMetadata`.
- Use `inspect --section history` before or after undoable workflows.
- Use `inspect --section zoom` before changing zoom regions.
- Use `editor background`, `editor cursor`, `editor camera`, `editor zoom`, `editor frame`, and `editor audio` as the preferred persistent edit surface.
- Use `editor style` only for legacy compatibility when a caller explicitly wants the composite command surface.
- Use `split` only for persisted segment edits.
- Use `screenshot` and `export` as render-only commands.
- Use `record`, `stop`, and `status` for host recording control.
- Use `del` only when the user explicitly wants project deletion.

## Safety

- Prefer absolute project paths.
- Assume commands are persistent unless the product context classifies them as render-only or host control.
- If a change is ambiguous, inspect first and modify one category at a time.
- If a command fails, confirm the CLI binary path, run `status`, and re-run the relevant `inspect` section before making another edit.
- If validating a new command surface, confirm both `project.json` and `history.json` semantics through `inspect`.

## References

- Read [references/intellicast-product-context.md](references/intellicast-product-context.md) for product context, supported workflows, and current CLI capability boundaries.
- Read [references/consistency.md](references/consistency.md) for the persistence model and command classification.
- Read [references/commands.md](references/commands.md) for the supported command surface and examples.
