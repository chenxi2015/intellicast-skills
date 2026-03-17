# IntelliCast CLI Command Surface

Use these commands from the IntelliCast repo root. This file is intended to be a complete command inventory aligned with `Sources/IntelliCastCLI/main.swift`.

Default sequence:

1. Inspect current state.
2. Apply the smallest matching edit or host-control command.
3. Inspect again to validate persisted state.
4. Use `screenshot` or `export` only for render validation.

## Top-level commands

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

## Global path rule

- Project commands use `-f /path/to/project.intellicast` or `--file /path/to/project.intellicast`.
- Prefer absolute project paths.

## Read and help commands

```bash
intellicast-cli help
intellicast-cli status
intellicast-cli inspect -f /path/to/project.intellicast --section summary
intellicast-cli inspect -f /path/to/project.intellicast --section editing
intellicast-cli inspect -f /path/to/project.intellicast --section history
intellicast-cli inspect -f /path/to/project.intellicast --section zoom
```

Inspect sections:

- `summary`
- `editing`
- `history`
- `zoom`

## Host control commands

```bash
intellicast-cli record --system-audio --mic
intellicast-cli stop
intellicast-cli status
```

Record options:

- `--display <id>`
- `--resolution <auto|480p|720p|1080p|1440p|2160p>`
- `--region <x,y,width,height>`
- `--system-audio` or `--sys-audio`
- `--microphone` or `--mic`
- `--enhance-microphone`

## Persistent editor commands

Preferred narrow commands:

```bash
intellicast-cli editor background -f /path/to/project.intellicast --background-mode solid --background-color '#1E7AF0'
intellicast-cli editor cursor -f /path/to/project.intellicast --auto-zoom true --show-cursor false --cursor-scale 1.8 --cursor-type glow
intellicast-cli editor camera -f /path/to/project.intellicast --camera-position tm --camera-size 0.31 --camera-effect comic
intellicast-cli editor zoom -f /path/to/project.intellicast --action add --start 1.0 --end 3.5 --zoom-level 2.2 --focus 0.25,0.75
intellicast-cli editor frame -f /path/to/project.intellicast --resolution 1080p --aspect_ratio 16:9 --screen-scale 0.9
intellicast-cli editor audio -f /path/to/project.intellicast --mute-system-audio true --enhance-microphone true
```

Legacy compatibility:

```bash
intellicast-cli editor style -f /path/to/project.intellicast --background-mode gradient --show-cursor true
```

### `editor style`

Legacy composite command. Prefer narrow commands for new automation.

Options:

- `--background-mode <gradient|wallpaper|solid>`
- `--gradient-index <n>`
- `--wallpaper-index <n>`
- `--background-color <#RRGGBB>`
- `--background-blur <value>`
- `--corner-radius <value>`
- `--shadow-blur <value>`
- `--show-zoom <true|false>`
- `--auto-zoom <true|false>`
- `--zoom-level <value>`
- `--show-cursor <true|false>`
- `--cursor-size <value>`
- `--cursor-type <default|mac|dark|dot|glow|ring|cross>`
- `--show-camera <true|false>`
- `--camera-position <lt|tm|rt|lm|lb|mm|mb|rm|rb>`
- `--camera-size <value>`
- `--camera-rounded <value>`
- `--camera-horizontal <true|false>`
- `--camera-shape <square|horizontal|vertical|original>`
- `--camera-effect <original|comic|sketch|bw|smooth|pixel>`

### `editor background`

Options:

- `--background-mode <gradient|wallpaper|solid>`
- `--gradient-index <n>`
- `--wallpaper-index <n>`
- `--background-color <#RRGGBB>`
- `--background-blur <value>`
- `--padding <value>`
- `--corner-radius <value>`
- `--shadow <value>`

Background mode aliases accepted by the CLI parser:

- `solid`
- `solid-color`
- `solid_color`
- `color`

### `editor cursor`

Options:

- `--auto-zoom <true|false>`
- `--show-zoom <true|false>`
- `--zoom-level <value>`
- `--show-cursor <true|false>`
- `--cursor-scale <value>`
- `--cursor-type <default|mac|dark|dot|glow|ring|cross>`

### `editor camera`

Options:

- `--show-camera <true|false>`
- `--camera-position <lt|tm|rt|lm|lb|mm|mb|rm|rb>`
- `--camera-size <value>`
- `--camera-rounded <value>`
- `--camera-horizontal <true|false>`
- `--camera-shape <square|horizontal|vertical|original>`
- `--camera-effect <original|comic|sketch|bw|smooth|pixel>`

Camera effect aliases:

- `bw`
- `b&w`

### `editor zoom`

Options:

- `--action <add|update|remove|clear>`
- `--index <n>`
- `--source <manual|auto-recording|auto-playback>`
- `--start <seconds|mm:ss>`
- `--end <seconds|mm:ss>`
- `--zoom-level <value>`
- `--focus <x,y>`
- `--enabled <true|false>`

Action aliases:

- `update` also accepts `set`
- `remove` also accepts `delete` and `del`

Source aliases:

- `auto-recording`
- `auto_recording`
- `recording`
- `auto-playback`
- `auto_playback`
- `playback`
- `live`

### `editor frame`

Options:

- `--resolution <auto|480p|720p|1080p|1440p|2160p>`
- `--aspect_ratio <default|16:9|1:1|4:3|9:16|3:4|4:5>`
- `--screen-scale <value>`
- `--corner-radius <value>`

### `editor audio`

Options:

- `--mute-system-audio <true|false>`
- `--mute-microphone <true|false>`
- `--enhance-microphone <true|false>`

## Other persistent project commands

```bash
intellicast-cli split -f /path/to/project.intellicast --type keep-range --start 00:02 --end 00:08
intellicast-cli undo -f /path/to/project.intellicast
intellicast-cli redo -f /path/to/project.intellicast
```

Split options:

- `--type <keep-range|remove-range|keep-left|keep-right|split-only>`
- `--start <seconds|mm:ss>`
- `--end <seconds|mm:ss>`

Split type aliases:

- `1` = `keep-range`
- `2` = `remove-range`
- `3` = `keep-left`
- `4` = `keep-right`
- `5` = `split-only`

## Render-only commands

```bash
intellicast-cli screenshot -f /path/to/project.intellicast --time 00:01
intellicast-cli export -f /path/to/project.intellicast
```

Export options:

- `--resolution <auto|480p|720p|1080p|1440p|2160p>`
- `--aspect_ratio <default|16:9|1:1|4:3|9:16|3:4|4:5>`
- `--export_content <all|pure_video|no_mic|no_sys_audio|no_zoom>`
- `--frame <24|30|60|120>`

Screenshot options:

- `--time <seconds|mm:ss>`
- `--output <path>`

## Project deletion

```bash
intellicast-cli del -f /path/to/project.intellicast
```

Use `del` only when the user explicitly wants project deletion.

## Notes

- Prefer `inspect` before and after edits.
- Treat `editor style` as legacy compatibility.
- Bool options accept `true|false`, `1|0`, `yes|no`, and `on|off`.
- Time values accept plain seconds or `mm:ss`.
