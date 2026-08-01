# HyprChan

A lightweight desktop mascot for Hyprland written in Python with PyQt6. It sits on your desktop, animates, shows random remarks, and can be configured with a small set of visual and behavior options.

This project is a hobby project and is not affiliated with the official Hyprland project.

## Features

- Animated desktop mascot for Hyprland
- Idle, sleeping, and wake-up states
- Random speech messages
- Transparent floating window with desktop-like behavior
- Simple autostart setup for Linux sessions

## Requirements

- Python 3.9+
- PyQt6
- XWayland support on Linux systems

Install dependencies:

```bash
pip install PyQt6
```

## Installation

From the project root:

```bash
python src/install.py
```

This adds an autostart entry so the mascot launches with your desktop session.

## Running manually

```bash
python src/main.py
```

## Project structure

```text
.
├── src/
│   ├── main.py
│   └── install.py
├── sprites/
├── README.md
├── Requirements.txt
└── Requirements(pip).txt
```

## Notes

HyprChan is intentionally simple and playful: it is designed as a desktop companion rather than a full productivity tool or official Hyprland component.
