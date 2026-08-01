<div align="center">

<img width="400" height="600" alt="hyprchan_present" src="https://github.com/b42h4n/Hyprchan/blob/main/sprites/icon.jpg" />

## HyprChan!

A lightweight desktop mascot for Hyprland written in Python with PyQt6. It sits on your desktop, animates, shows random remarks, and can be configured with a small set of visual and behavior options.

All sprites are taken from https://github.com/AscenderTeam/Hyprchan/

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Hyprland](https://img.shields.io/badge/Hyprland-CC1111?style=for-the-badge&logo=linux&logoColor=white)](https://hyprland.org/)

# Visuals

<div align="center">
  <table border="0">
    <tr>
      <td width="50%">
        <img src="https://github.com/b42h4n/Hyprchan/blob/main/sprites/screenshot.png" width="100%" alt="screenshot 1">
        <p align="center"><i>Animated Hyprland overlay with tool-calling capabilities.</i></p>
      </td>
    </tr>
  </table>
</div>

## Quick start

Installing requirements:

```shell
sudo apt install python3 pip -y
pip install PyQt6 --break-system-packages
sudo apt install xwayland -y
```
(Or
```shell
sudo pacman -S python3 python3-pip
pip install PyQt6 pip install PyQt6 --break-system-packages
sudo pacman -S xwayland
```
if you using arch or arch based)

Installing hyprchan from the project root:

```shell
python src/install.py
```

This adds an autostart entry so the mascot launches with your desktop session(Sway, i3, driftwm, hyprland, kde plasma support).
If you don't wan't this on autostart for some reasons, you can run script manually:

```shell
python src/main.py
```

## Features
* **Sleep & Dreaming:** Automatically falls asleep after a certain period.
* **Animations:** It is animated and has (so far) 4 animations!
* **Talking:** She can say different phrases and reminders. Convenient!
