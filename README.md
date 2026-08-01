<div align="center">

<img width="400" height="600" alt="hyprchan_present" src="https://github.com/b42h4n/Hyprchan/blob/main/sprites/icon.jpg" />

## HyprChan!

A lightweight desktop mascot for Hyprland written in Python with PyQt6. It sits on your desktop, animates, shows random remarks, and can be configured with a small set of visual and behavior options.

All sprites are taken from https://github.com/AscenderTeam/Hyprchan/

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Hyprland](https://img.shields.io/badge/Hyprland-CC1111?style=for-the-badge&logo=linux&logoColor=white)](https://hyprland.org/)

## Requirements
- PyQt6
- XWayland support on Linux systems

Install dependencies:

```shell
pip install PyQt6
```

## Installation

From the project root:

```shell
python src/install.py
```

This adds an autostart entry so the mascot launches with your desktop session.

## Running manually

```shell
python src/main.py
```

## Project structure

```text
.
├── src/
│   ├── main.py
│   └── install.py
├── sprites/
└── README.md
```
