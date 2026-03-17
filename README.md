# IntelliCast Skills

Agent skills for operating IntelliCast projects through the supported `intellicast-cli` command surface.

## Available Skills

### `intellicast-cli-operator`

Operate `.intellicast` projects through IntelliCast's CLI instead of touching SwiftUI view state directly.

Use it for:

- inspecting persisted project state
- applying persistent editor commands
- validating `project.json` and `history.json` changes
- exporting or capturing screenshots
- traversing undo / redo history
- controlling recording through the host app

## Install with skills.sh

Install the skill from this repo:

```bash
npx skills add https://github.com/chenxi2015/intellicast-skills --skill intellicast-cli-operator
```

## Validate locally

Use the bundled no-dependency Python validator:

```bash
python3 scripts/validate_skill.py intellicast-cli-operator
```

If you want a second parser implementation, the Ruby validator also works on macOS:

```bash
ruby scripts/validate_skill.rb intellicast-cli-operator
```

## Repository Layout

```text
intellicast-skills/
└── intellicast-cli-operator/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── commands.md
        └── consistency.md
        └── intellicast-product-context.md
```

## Notes

- The skill assumes the agent is working inside the IntelliCast repository or a machine where `intellicast-cli` can be built or found.
- The skill includes `references/intellicast-product-context.md` so another agent can understand the IntelliCast product and current CLI boundaries without re-reading the whole app first.
- The skill is aligned to the current CLI command surface:
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
- Preferred persistent edit surface:
  - `inspect`
  - `editor background`
  - `editor cursor`
  - `editor camera`
  - `editor zoom`
  - `editor frame`
  - `editor audio`
  - `split`
  - `undo`
  - `redo`
  - `export`
  - `screenshot`
  - `record`
  - `stop`
  - `status`
  - `del`
- Recommended agent loop:
  1. `inspect`
  2. one narrow edit command
  3. `inspect` again
  4. optional `screenshot` or `export`
