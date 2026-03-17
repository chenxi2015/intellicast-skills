# IntelliCast CLI Command Surface

Use these commands from the IntelliCast repo root.

## Read commands

```bash
intellicast-cli status
intellicast-cli inspect -f /path/to/project.intellicast --section summary
intellicast-cli inspect -f /path/to/project.intellicast --section editing
intellicast-cli inspect -f /path/to/project.intellicast --section history
intellicast-cli inspect -f /path/to/project.intellicast --section zoom
```

## Persistent editor commands

```bash
intellicast-cli editor background -f /path/to/project.intellicast --background-mode solid --background-color '#1E7AF0'
intellicast-cli editor cursor -f /path/to/project.intellicast --auto-zoom true --show-cursor false --cursor-scale 1.8 --cursor-type glow
intellicast-cli editor camera -f /path/to/project.intellicast --camera-position tm --camera-size 0.31 --camera-effect comic
intellicast-cli editor zoom -f /path/to/project.intellicast --action add --start 1.0 --end 3.5 --zoom-level 2.2 --focus 0.25,0.75
intellicast-cli editor frame -f /path/to/project.intellicast --resolution 1080p --aspect_ratio 16:9 --screen-scale 0.9
intellicast-cli editor audio -f /path/to/project.intellicast --mute-system-audio true --enhance-microphone true
intellicast-cli split -f /path/to/project.intellicast --type keep-range --start 00:02 --end 00:08
intellicast-cli undo -f /path/to/project.intellicast
intellicast-cli redo -f /path/to/project.intellicast
```

## Render-only commands

```bash
intellicast-cli screenshot -f /path/to/project.intellicast --time 00:01
intellicast-cli export -f /path/to/project.intellicast
```

## Recording lifecycle

```bash
intellicast-cli record --system-audio --mic
intellicast-cli stop
intellicast-cli status
```

## Notes

- Use absolute project paths.
- Prefer `inspect` before and after edits.
- Treat `editor style` as legacy compatibility.
