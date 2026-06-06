# Super Mario Python

A Super Mario game built with Python + Pygame, now available as an Android APK!

## Run on Desktop

```bash
pip install pygame
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| ← → | Move |
| Space | Jump |
| Shift | Boost |
| Esc | Pause |

## Build Android APK

This repo uses GitHub Actions to automatically build APK. Push to `main` branch or trigger manually from the **Actions** tab.

Or build locally with Buildozer (requires Linux/WSL2):
```bash
buildozer android debug
```
