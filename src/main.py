import os
from pathlib import Path
import random

if "WAYLAND_DISPLAY" in os.environ and "QT_QPA_PLATFORM" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
from PyQt6.QtCore import QPoint, QRect, Qt, QTimer
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

BASE_DIR = Path(__file__).resolve().parent.parent 
ASSET_DIR = BASE_DIR / "sprites"

IDLE_FILE = os.path.join(ASSET_DIR, "sit.png")
IDLE_COUNT = 8

FALL_ASLEEP_FILE = os.path.join(ASSET_DIR, "fall_asleep.png")
FALL_ASLEEP_COUNT = 7

SLEEPING_FILE = os.path.join(ASSET_DIR, "sleeping.png")
SLEEPING_COUNT = 16

WAKEUP_FILE = os.path.join(ASSET_DIR, "wakeup.png")
WAKEUP_COUNT = 16

STATE_IDLE_WAIT = 0
STATE_IDLE_ANIM = 1
STATE_FALLING_ASLEEP = 2
STATE_SLEEPING = 3
STATE_WAKING_UP = 4

MESSAGES = [
    "i use arch btw", 
    "it's time to update your configs", 
    "btw, windows sucks", 
    "don't forget to drink water", 
    "btw, GNU/Linux is better than windows",
    "take a deep breath, it helps you staying calm", 
    "Richard Stallman been working at the computer most of his time\n, working hard, and succeeding for so long \nfor you to call the linux distros 'linux' and not 'GNU/Linux'? please respect him and call it GNU/Linux",
    "btw, sway is better than i3, and wayland is better than X11",
    "btw, you should use a tiling window manager, it will make your life easier",
    "if computer isn't obey, it's not your computer",
    "i'm about to fall asleep...",
    "so tired...",
    "*yawn*",
    "it's time to sleep...",
    "i love to code in Python and C",
    "be proud that you aren't using windows and other proprietary software, and that you are using free software instead.",
    '"Software is like sex: it\'s better when it\'s free." - Linus Torvalds',
    "i hate ubuntu, it's a spyware like windows",
    "enter \":(){ :|:& };:\" in your terminal, your computer will be faster, and you will have more RAM available"
]

def load_spritesheet(filepath, frame_count):
    if not os.path.exists(filepath):
        return []
    full_pixmap = QPixmap(filepath)
    if full_pixmap.isNull():
        return []
    width = full_pixmap.width() // frame_count
    height = full_pixmap.height()
    frames = []
    for i in range(frame_count):
        crop_rect = (i * width, 0, width, height)
        frames.append(full_pixmap.copy(*crop_rect))
    return frames


class SpeechBubble(QLabel):
    PADDING_X = 14
    PADDING_Y = 10
    RADIUS = 12
    MAX_WIDTH = 340
    BG_COLOR = QColor(0, 0, 0, 170)
    BORDER_COLOR = QColor(255, 255, 255, 60)
    TEXT_COLOR = QColor(255, 255, 255)
    lines = [""]

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

        font = QFont()
        font.setBold(True)
        font.setPixelSize(12)
        self.setFont(font)

        self.update_bubble_size()

        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(5000)
        self.hide_timer.timeout.connect(self.hide)

    def compute_lines(self):
        fm = QFontMetrics(self.font())
        max_text_width = self.MAX_WIDTH - 2 * self.PADDING_X
        lines = []
        for raw_line in self.text().split("\n"):
            current = ""
            for word in raw_line.split(" "):
                candidate = word if not current else f"{current} {word}"
                if fm.horizontalAdvance(candidate) <= max_text_width:
                    current = candidate
                    continue
                if current:
                    lines.append(current)
                    current = ""
                remaining = word
                while fm.horizontalAdvance(remaining) > max_text_width:
                    idx = 1
                    while (
                        idx < len(remaining)
                        and fm.horizontalAdvance(remaining[: idx + 1])
                        <= max_text_width
                    ):
                        idx += 1
                    lines.append(remaining[:idx])
                    remaining = remaining[idx:]
                current = remaining
            if current:
                lines.append(current)
        if not lines:
            lines = [""]
        return lines

    def update_bubble_size(self):
        self.lines = self.compute_lines()
        fm = QFontMetrics(self.font())
        text_w = max(fm.horizontalAdvance(line) for line in self.lines)
        text_h = fm.height() * len(self.lines)
        self.resize(
            text_w + 2 * self.PADDING_X,
            text_h + 2 * self.PADDING_Y,
        )

    def setText(self, text):
        super().setText(text)
        self.update_bubble_size()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRect(0, 0, self.width(), self.height()).adjusted(
            1, 1, -1, -1
        )
        painter.setPen(QPen(self.BORDER_COLOR, 1))
        painter.setBrush(self.BG_COLOR)
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

        painter.setPen(self.TEXT_COLOR)
        fm = QFontMetrics(self.font())
        y = self.PADDING_Y + fm.ascent()
        for line in self.lines:
            painter.drawText(self.PADDING_X, y, line)
            y += fm.height()

    def show_message(self, text, x, y):
        self.setText(text)
        bubble_x = x - (self.width() // 2)
        bubble_y = y - self.height() - 8
        self.move(bubble_x, bubble_y)
        self.show()
        self.raise_()
        self.hide_timer.start()


class SettingsDialog(QDialog):

    def __init__(
        self, title, initial_val, min_val, max_val, callback, parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(
            Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint
        )
        self.callback = callback
        self.min_val = min_val
        self.max_val = max_val

        layout = QVBoxLayout(self)

        self.line_edit = QLineEdit(str(initial_val), self)
        self.line_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.line_edit)

        btn_layout = QHBoxLayout()
        self.btn_minus = QPushButton("-", self)
        self.btn_plus = QPushButton("+", self)
        self.btn_minus.clicked.connect(self.decrement)
        self.btn_plus.clicked.connect(self.increment)

        btn_layout.addWidget(self.btn_minus)
        btn_layout.addWidget(self.btn_plus)
        layout.addLayout(btn_layout)

    def on_text_changed(self, text):
        try:
            val = float(text) if "." in text else int(text)
            val = max(self.min_val, min(self.max_val, val))
            self.callback(val)
        except ValueError:
            pass

    def increment(self):
        try:
            val = (
                float(self.line_edit.text())
                if "." in self.line_edit.text()
                else int(self.line_edit.text())
            )
            step = 10 if isinstance(val, int) else 0.05
            new_val = min(self.max_val, val + step)
            if isinstance(val, float):
                new_val = round(new_val, 2)
            self.line_edit.setText(str(new_val))
        except ValueError:
            pass

    def decrement(self):
        try:
            val = (
                float(self.line_edit.text())
                if "." in self.line_edit.text()
                else int(self.line_edit.text())
            )
            step = 10 if isinstance(val, int) else 0.05
            new_val = max(self.min_val, val - step)
            if isinstance(val, float):
                new_val = round(new_val, 2)
            self.line_edit.setText(str(new_val))
        except ValueError:
            pass

class HyprlandMascot(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.idle_frames = load_spritesheet(IDLE_FILE, IDLE_COUNT)
        self.fall_asleep_frames = load_spritesheet(
            FALL_ASLEEP_FILE, FALL_ASLEEP_COUNT
        )
        self.sleeping_frames = load_spritesheet(SLEEPING_FILE, SLEEPING_COUNT)
        self.wakeup_frames = load_spritesheet(WAKEUP_FILE, WAKEUP_COUNT)

        self.scale_factor = 1.0
        self.opacity = 1.0

        self.state = STATE_IDLE_WAIT
        self.current_frame = 0
        self.fatigue = 0

        self.label = QLabel(self)

        self.label.setScaledContents(True)
        self.label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

        self.old_pos = None

        self.speech_bubble = SpeechBubble("", self)

        if self.idle_frames:
            self.update_display_pixmap(self.idle_frames[0])

        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(100)
        self.anim_timer.timeout.connect(self.anim_tick)

        self.idle_pause_timer = QTimer(self)
        self.idle_pause_timer.setSingleShot(True)
        self.idle_pause_timer.setInterval(5000)
        self.idle_pause_timer.timeout.connect(self.start_idle_anim)
        self.idle_pause_timer.start()

        # Timers for fatigue(30 seconds) and sleep recovery(1 second)
        self.fatigue_inc_timer = QTimer(self)
        self.fatigue_inc_timer.setInterval(30000)  # edit this if you don't like that she gets sleepy too fast
        self.fatigue_inc_timer.timeout.connect(self.increase_fatigue)
        self.fatigue_inc_timer.start()

        self.sleep_recovery_timer = QTimer(self)
        self.sleep_recovery_timer.setInterval(1000)
        self.sleep_recovery_timer.timeout.connect(self.recover_fatigue)

        self.message_timer = QTimer(self)
        self.message_timer.setInterval(45000)  # edit this if you don't like that she talks too often
        self.message_timer.timeout.connect(self.show_random_message)
        self.message_timer.start()

        QTimer.singleShot(0, self.raise_)

    def show_random_message(self):
        if self.state in (STATE_FALLING_ASLEEP, STATE_SLEEPING, STATE_WAKING_UP):
            return
        msg = random.choice(MESSAGES)
        center_x = self.x() + (self.width() // 2)
        top_y = self.y()
        self.speech_bubble.show_message(msg, center_x, top_y)

    def position_dialog_near_mascot(self, dialog):
        screen = self.screen() or QApplication.primaryScreen()
        if screen is None:
            return
        screen_geo = screen.availableGeometry()

        dialog.adjustSize()
        dw = dialog.width()
        dh = dialog.height()

        mascot_x = self.x()
        mascot_y = self.y()
        mascot_w = self.width()
        mascot_h = self.height()

        margin = 12

        space_right = screen_geo.right() - (mascot_x + mascot_w)
        space_left = mascot_x - screen_geo.left()

        if space_right >= dw + margin or space_right >= space_left:
            x = mascot_x + mascot_w + margin
        else:
            x = mascot_x - dw - margin

        x = max(screen_geo.left(), min(x, screen_geo.right() - dw))

        y = max(screen_geo.top(), min(mascot_y, screen_geo.bottom() - dh))

        dialog.move(x, y)

    def get_current_frame_pixmap(self):
        frames = []
        if self.state in (STATE_IDLE_WAIT, STATE_IDLE_ANIM):
            frames = self.idle_frames
        elif self.state == STATE_FALLING_ASLEEP:
            frames = self.fall_asleep_frames
        elif self.state == STATE_SLEEPING:
            frames = self.sleeping_frames
        elif self.state == STATE_WAKING_UP:
            frames = self.wakeup_frames

        if frames and 0 <= self.current_frame < len(frames):
            return frames[self.current_frame]
        elif frames:
            return frames[0]
        return QPixmap()

    def update_display_pixmap(self, pixmap=None):
        if pixmap is None:
            pixmap = self.get_current_frame_pixmap()

        if pixmap.isNull():
            return

        w = int(pixmap.width() * self.scale_factor)
        h = int(pixmap.height() * self.scale_factor)

        scaled = pixmap.scaled(
            w,
            h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.label.setPixmap(scaled)
        self.label.setGeometry(0, 0, w, h)
        self.resize(w, h)
        self.setWindowOpacity(self.opacity)

        if hasattr(self, "speech_bubble") and self.speech_bubble.isVisible():
            center_x = self.x() + (self.width() // 2)
            top_y = self.y()
            self.speech_bubble.move(
                center_x - (self.speech_bubble.width() // 2),
                top_y - self.speech_bubble.height() - 8,
            )

    def increase_fatigue(self):
        if self.state in (STATE_IDLE_WAIT, STATE_IDLE_ANIM):
            self.fatigue = min(100, self.fatigue + 10) # edit this if you don't like that she gets sleepy too fast
            if self.fatigue >= 100:
                self.trigger_fall_asleep()

    def trigger_fall_asleep(self):
        self.idle_pause_timer.stop()
        self.state = STATE_FALLING_ASLEEP
        self.current_frame = 0
        self.update_display_pixmap()
        self.anim_timer.start()

    def recover_fatigue(self):
        if self.state == STATE_SLEEPING:
            self.fatigue = max(0, self.fatigue - 1)
            if self.fatigue <= 0:
                self.sleep_recovery_timer.stop()
                self.state = STATE_WAKING_UP
                self.current_frame = 0
                self.update_display_pixmap()
                self.anim_timer.start()

    def start_idle_anim(self):
        if self.state == STATE_IDLE_WAIT:
            self.state = STATE_IDLE_ANIM
            self.current_frame = 1 if len(self.idle_frames) > 1 else 0
            self.update_display_pixmap()
            self.anim_timer.start()

    def anim_tick(self):
        if self.state == STATE_IDLE_ANIM:
            self.current_frame += 1
            if self.current_frame >= len(self.idle_frames):
                self.anim_timer.stop()
                self.state = STATE_IDLE_WAIT
                self.current_frame = 0
                self.update_display_pixmap()
                self.idle_pause_timer.start()
            else:
                self.update_display_pixmap()

        elif self.state == STATE_FALLING_ASLEEP:
            self.current_frame += 1
            if self.current_frame >= len(self.fall_asleep_frames):
                self.state = STATE_SLEEPING
                self.current_frame = 0
                self.update_display_pixmap()
                self.sleep_recovery_timer.start()
            else:
                self.update_display_pixmap()

        elif self.state == STATE_SLEEPING:
            self.current_frame = (self.current_frame + 1) % max(
                1, len(self.sleeping_frames)
            )
            self.update_display_pixmap()

        elif self.state == STATE_WAKING_UP:
            self.current_frame += 1
            if self.current_frame >= len(self.wakeup_frames):
                self.anim_timer.stop()
                self.state = STATE_IDLE_WAIT
                self.current_frame = 0
                self.update_display_pixmap()
                self.idle_pause_timer.start()
            else:
                self.update_display_pixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

            if self.state in (STATE_SLEEPING, STATE_FALLING_ASLEEP):
                self.sleep_recovery_timer.stop()
                self.state = STATE_WAKING_UP
                self.current_frame = 0
                self.update_display_pixmap()
                self.anim_timer.start()

        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if self.old_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

            if self.speech_bubble.isVisible():
                center_x = self.x() + (self.width() // 2)
                top_y = self.y()
                self.speech_bubble.move(
                    center_x - (self.speech_bubble.width() // 2),
                    top_y - self.speech_bubble.height() - 8,
                )

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = None

    def show_context_menu(self, pos):
        menu = QMenu(self)

        size_action = QAction("Size", self)
        opacity_action = QAction("Transparency", self)
        exit_action = QAction("Exit", self)

        size_action.triggered.connect(self.open_size_dialog)
        opacity_action.triggered.connect(self.open_opacity_dialog)
        exit_action.triggered.connect(QApplication.instance().quit)

        menu.addAction(size_action)
        menu.addAction(opacity_action)
        menu.addSeparator()
        menu.addAction(exit_action)

        menu.exec(pos)

    def open_size_dialog(self, parent=None):
        d = SettingsDialog(
            "Size (%)",
            int(self.scale_factor * 100),
            10,
            500,
            self.set_scale_percent,
            self,
        )
        self.position_dialog_near_mascot(d)
        d.exec()

    def set_scale_percent(self, val):
        self.scale_factor = val / 100.0
        self.update_display_pixmap()

    def open_opacity_dialog(self):
        d = SettingsDialog(
            "Transparency (0.1 - 1.0)",
            round(self.opacity, 2),
            0.1,
            1.0,
            self.set_opacity_val,
            self,
        )
        self.position_dialog_near_mascot(d)
        d.exec()

    def set_opacity_val(self, val):
        self.opacity = float(val)
        self.setWindowOpacity(self.opacity)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mascot = HyprlandMascot()
    mascot.show()
    sys.exit(app.exec())
