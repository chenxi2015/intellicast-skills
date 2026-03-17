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

## Repository Layout

```text
intellicast-skills/
└── intellicast-cli-operator/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── commands.md
        └── consistency.md
```

## Notes

- The skill assumes the agent is working inside the IntelliCast repository or a machine where `intellicast-cli` can be built or found.
- The skill is designed around the current persistent command surface:
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
