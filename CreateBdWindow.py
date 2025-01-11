import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QLineEdit, QLabel, QPushButton,
                             QMainWindow, QFileDialog)


class CreateDbWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db_path = None

    def initUI(self):
        self.setGeometry(300, 300, 500, 200)  # Slightly increased height
        self.setWindowTitle('Создание БД')

        self.path_label = QLabel('Путь для сохранения БД:', self)
        self.path_label.move(20, 20)
        self.path_label.resize(150, 30)

        self.path_line_edit = QLineEdit(self)
        self.path_line_edit.move(20, 45)
        self.path_line_edit.resize(300, 25)

        self.browse_button = QPushButton('Обзор', self)
        self.browse_button.move(330, 45)
        self.browse_button.clicked.connect(self.browse_file)

        self.create_button = QPushButton('Создать', self)
        self.create_button.move(150, 90)
        self.create_button.clicked.connect(self.create_database)

        self.status_label = QLabel("", self)
        self.status_label.move(20, 120)
        self.status_label.resize(350, 25)

    def browse_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить БД", "", "Файлы баз данных (*.db);;Все файлы (*.*)")
        if file_name:
            self.path_line_edit.setText(file_name)
            self.db_path = file_name

    def create_database(self):
        if self.path_line_edit.text():
            self.db_path = self.path_line_edit.text()
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tracks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        track_filepath TEXT NOT NULL
                    )
                ''')
                conn.commit()
                conn.close()
                self.status_label.setText("База данных успешно создана!")
                self.status_label.setStyleSheet("color: green;")  # Изменение цвета текста
            except sqlite3.Error as e:
                self.status_label.setText(f"Ошибка создания базы данных: {e}")
                self.status_label.setStyleSheet("color: red;")  # Изменение цвета текста


        else:
            self.status_label.setText("Не выбран путь для сохранения.")
            self.status_label.setStyleSheet("color: red;")  # Изменение цвета текста


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateDbWindow()
    window.show()
    sys.exit(app.exec())
