import sys
import keyboard
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import Qt, QTimer
import random

class Bird(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 100
        self.y_vel = 0
        self.gravity = 0.45
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label = QLabel(self)
        pixmap = QPixmap("bird.png").scaled(
            100, 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())

    def jump(self):
        self.y_vel = -12

    def move_bird(self):
        self.y += self.y_vel
        self.y_vel += self.gravity
        self.move(self.x, int(self.y))

class Pipe(QWidget):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 8
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label = QLabel(self)
        pixmap = QPixmap("pipe.png").scaled(
            150, 650,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        if flipped:
            transform = QTransform().scale(1, -1)
            pixmap = pixmap.transformed(transform)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())
        self.move(self.x, self.y)

    def update(self):
        self.x -= self.speed
        self.move(self.x, self.y)

class Game:
    GAP = 240
    PIPE_H = 650

    def __init__(self):
        self.bird = Bird()
        self.bird.show()
        self.pipes = []
        self.spawn_pipes()
        keyboard.add_hotkey("space", self.bird.jump)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def spawn_pipes(self):
        screen = QApplication.primaryScreen().geometry()
        width  = screen.width()
        height = screen.height()

        for i in range(6):
            x = width + i * 600
            y = random.randrange(350, height - 350)

            bottom_pipe = Pipe(x, y)
            bottom_pipe.show()
            self.pipes.append(bottom_pipe)

            top_y = y - self.GAP - self.PIPE_H
            top_pipe = Pipe(x, top_y, flipped=True)
            top_pipe.show()
            self.pipes.append(top_pipe)

    def check_collisions(self):
        bird_rect = self.bird.geometry().adjusted(15, 15, -15, -15)
        for pipe in self.pipes:
            if bird_rect.intersects(pipe.geometry()):
                self.game_over()
                return

    def game_over(self):
        self.timer.stop()
        for pipe in self.pipes:
            pipe.close()
        self.bird.close()

    def update(self):
        self.bird.move_bird()
        screen_width = QApplication.primaryScreen().geometry().width()
        
        for pipe in self.pipes:
            pipe.update()
            if pipe.x < -1600:
                pipe.x = screen_width
                pipe.move(pipe.x, pipe.y)

        self.check_collisions()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec())