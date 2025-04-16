############################
# @author EliasDH Team     #
# @see https://eliasdh.com #
# @since 01/01/2025        #
############################

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, QRect, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from input_control.mouse import move_mouse_to, simulate_click

class MousePadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InputControl")
        self.setGeometry(100, 100, 600, 600)
        # Rond porder af met 16px
        self.setFixedSize(600, 600)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCursor(Qt.BlankCursor)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.second_cursor_pos = None
        self.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)

        self.click_active = False
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.reset_click_animation)

        self.dragging = False
        self.drag_position = QPoint()

        self.handle_rect = QRect(0, 0, self.width(), 30)

        self.close_button = QPushButton("X", self.central_widget)
        self.close_button.setGeometry(self.width() - 40, 5, 30, 20)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("background-color: red; color: white; border-radius: 5px;")

        self.desktop = QDesktopWidget()
        self.virtual_rect = self.desktop.screenGeometry(-1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        painter.setBrush(QBrush(QColor(79, 148, 240, 200)))# #4f94f0
        painter.drawRect(self.handle_rect)

        if self.second_cursor_pos:
            screen_x, screen_y = self.pos_to_screen(self.second_cursor_pos[0], self.second_cursor_pos[1])
            if (screen_x < self.virtual_rect.left() or screen_x > self.virtual_rect.right() or
                screen_y < self.virtual_rect.top() or screen_y > self.virtual_rect.bottom()):
                painter.setBrush(QBrush(QColor(255, 0, 0)))
                painter.drawEllipse(self.second_cursor_pos[0] - 10, self.second_cursor_pos[1] - 10, 20, 20)
            else:
                if self.click_active:
                    painter.setBrush(QBrush(QColor(255, 255, 255))) # #ffffff
                    painter.drawEllipse(self.second_cursor_pos[0] - 20, self.second_cursor_pos[1] - 20, 40, 40)
                else:
                    painter.setBrush(QBrush(QColor(79, 148, 240, 200)))# #4f94f0
                    painter.drawEllipse(self.second_cursor_pos[0] - 15, self.second_cursor_pos[1] - 15, 30, 30)

    def mouseMoveEvent(self, event):
        self.second_cursor_pos = (event.x(), event.y())
        self.update()

        if self.dragging:
            self.move(self.mapToGlobal(event.pos() - self.drag_position))
            return

        if not self.handle_rect.contains(event.pos()):
            screen_x, screen_y = self.pos_to_screen(event.x(), event.y())
            move_mouse_to(screen_x, screen_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.handle_rect.contains(event.pos()):
            self.dragging = True
            self.drag_position = event.pos()
            self.setCursor(Qt.SizeAllCursor)
        elif event.button() == Qt.LeftButton and self.second_cursor_pos:
            simulate_click()
            self.click_active = True
            self.click_timer.start(100)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.BlankCursor)

    def reset_click_animation(self):
        self.click_active = False
        self.update()

    def pos_to_screen(self, x, y):
            window_width, window_height = self.width(), self.height()
            if window_width == 0 or window_height == 0:
                return 0, 0

            virtual_width = self.virtual_rect.width()
            virtual_height = self.virtual_rect.height()
            virtual_left = self.virtual_rect.left()
            virtual_top = self.virtual_rect.top()

            screen_x = virtual_left + (x / window_width) * virtual_width
            screen_y = virtual_top + (y / window_height) * virtual_height

            return screen_x, screen_y