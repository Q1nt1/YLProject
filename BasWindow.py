import sys
import pygame
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QPushButton, QLabel, QVBoxLayout, QWidget)
from PyQt6.QtGui import QPixmap  # Импортируем QPixmap для работы с изображениями
from DatabaseWindow import SecondWindow
from CreateBdWindow import CreateDbWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        pygame.init()  # Инициализируем Pygame
        pygame.mixer.init()  # Инициализируем Pygame mixer

        self.audio = None  # Добавляем атрибут для хранения загруженного файла
        self.current_time = 0

    def initUI(self):
        self.setWindowTitle('AudioProg')
        self.setGeometry(500, 300, 700, 350)

        # Создаем QLabel для изображения
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("data/image_audio.jpg"))  # Указываем путь к изображению
        self.image_label.setScaledContents(True)  # Масштабируем изображение, чтобы оно вписывалось в QLabel
        self.image_label.setFixedHeight(450)  # Устанавливаем фиксированную высоту для QLabel с изображением

        self.load_button = QPushButton('Загрузить аудио', self)
        self.play_button = QPushButton('Воспроизвести', self)
        self.stop_button = QPushButton('Остановить', self)
        self.open_second_window = QPushButton('Открыть форму для загрузки БД', self)
        self.open_tri_window = QPushButton('Открыть форму для создания БД', self)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)  # Добавляем QLabel с изображением в layout
        layout.addWidget(self.load_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.open_second_window)
        layout.addWidget(self.open_tri_window)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_button.clicked.connect(self.load_audio)
        self.play_button.clicked.connect(self.play_audio)
        self.stop_button.clicked.connect(self.stop_audio)
        self.open_second_window.clicked.connect(self.second_window)
        self.open_tri_window.clicked.connect(self.tri_window)

        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def load_audio(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Загрузить аудиофайл", "", "Аудио файлы (*.mp3)")
        if filepath:
            try:
                self.audio = filepath
                self.play_button.setEnabled(True)
                self.stop_button.setEnabled(True)
            except Exception as e:
                print(f"Ошибка загрузки: {str(e)}")

    def play_audio(self):
        if self.audio:
            try:
                pygame.mixer.music.load(self.audio)
                pygame.mixer.music.play(start=self.current_time)  # Начинаем воспроизведение с сохраненного времени
                pygame.mixer.music.set_volume(0.1)
            except Exception as e:
                print(f"Ошибка воспроизведения: {str(e)}")

    def stop_audio(self):
        if pygame.mixer.music.get_busy():
            self.current_time = pygame.mixer.music.get_pos() / 1000.0  # Сохраняем текущее время воспроизведения
            pygame.mixer.music.stop()
            print("Воспроизведение остановлено")

    def second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()

    def tri_window(self):
        self.create_db = CreateDbWindow()
        self.create_db.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
