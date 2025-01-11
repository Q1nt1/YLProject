import sys
import pygame
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QPushButton, QLabel, QVBoxLayout, QWidget,
                             QListWidget)  # Добавляем QListWidget для отображения треков


class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        pygame.init()
        pygame.mixer.init()

        self.audio = None
        self.current_time = 0
        self.db_connection = None  # Добавляем атрибут для подключения к БД

    def initUI(self):
        self.setWindowTitle('AudioProg')
        self.setGeometry(500, 300, 500, 400)

        self.load_db_button = QPushButton('Загрузить БД', self)  # Кнопка для загрузки БД
        self.load_button = QPushButton('Загрузить аудио', self)
        self.play_button = QPushButton('Воспроизвести', self)
        self.stop_button = QPushButton('Остановить', self)
        self.add_track = QPushButton('Добавть трек в БД', self)
        self.remove_track = QPushButton('Удалить трек из БД', self)

        self.audio_label = QLabel("Аудиофайл не загружен", self)
        self.track_list = QListWidget(self)  # Список для отображения треков

        layout = QVBoxLayout()
        layout.addWidget(self.audio_label)
        layout.addWidget(self.load_db_button)  # Добавляем кнопку загрузки БД
        layout.addWidget(self.track_list)  # Добавляем список треков
        layout.addWidget(self.load_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.add_track)
        layout.addWidget(self.remove_track)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_db_button.clicked.connect(self.load_database)  # Подключаем кнопку к функции
        self.load_button.clicked.connect(self.load_audio)
        self.play_button.clicked.connect(self.play_audio)
        self.stop_button.clicked.connect(self.stop_audio)
        self.add_track.clicked.connect(self.add_tracks)
        self.remove_track.clicked.connect(self.remove_tracks)

        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def load_database(self):
        db_path, _ = QFileDialog.getOpenFileName(self, "Загрузить базу данных", "", "SQLite Database (*.db)")
        if db_path:
            try:
                self.db_connection = sqlite3.connect(db_path)  # Подключаемся к базе данных
                self.load_tracks()  # Загружаем треки из базы данных
            except Exception as e:
                self.audio_label.setText(f"Ошибка загрузки БД: {str(e)}")
                print(f"Ошибка загрузки БД: {str(e)}")

    def load_tracks(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT track_filepath FROM tracks")  # У нас есть таблица 'tracks' с колонкой 'track_name'
        tracks = cursor.fetchall()
        self.track_list.clear()  # Очищаем список перед добавлением новых треков
        for track in tracks:
            self.track_list.addItem(track[0])  # Добавляем треки в список

    def load_audio(self):
        selected_track = self.track_list.currentItem()  # Получаем выбранный трек
        if selected_track:
            self.audio = selected_track.text()  # Сохраняем имя трека
            self.audio_label.setText(f"Загружен: {self.audio}")
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)

    def play_audio(self):
        if self.audio:
            try:
                pygame.mixer.music.load(self.audio)  # Загрузка аудиофайла
                pygame.mixer.music.play(start=self.current_time)
                pygame.mixer.music.set_volume(0.1)
            except Exception as e:
                self.audio_label.setText(f"Ошибка воспроизведения: {str(e)}")
                print(f"Ошибка воспроизведения: {str(e)}")

    def stop_audio(self):
        if pygame.mixer.music.get_busy():
            self.current_time = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.stop()
            self.audio_label.setText("Воспроизведение остановлено")

    def add_tracks(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Добавить трек", "", "Аудио файлы (*.mp3; *.wav)")
        if filepath:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("INSERT INTO tracks (track_filepath) VALUES (?)", (filepath,))
                self.db_connection.commit()  # Сохраняем изменения в базе данных
                self.load_tracks()  # Обновляем список треков
                self.audio_label.setText(f"Трек добавлен: {filepath}")
            except Exception as e:
                self.audio_label.setText(f"Ошибка добавления трека: {str(e)}")
                print(f"Ошибка добавления трека: {str(e)}")

    def remove_tracks(self):
        selected_track = self.track_list.currentItem()  # Получаем выбранный трек
        if selected_track:
            track_filepath = selected_track.text()  # Получаем путь к треку
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("DELETE FROM tracks WHERE track_filepath = ?", (track_filepath,))
                self.db_connection.commit()  # Сохраняем изменения в базе данных
                self.load_tracks()  # Обновляем список треков
                self.audio_label.setText(f"Трек удален: {track_filepath}")
            except Exception as e:
                self.audio_label.setText(f"Ошибка удаления трека: {str(e)}")
                print(f"Ошибка удаления трека: {str(e)}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecondWindow()
    window.show()
    sys.exit(app.exec())