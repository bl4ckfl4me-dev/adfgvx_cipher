import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox


def create_key_square(key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    key_square = []
    seen = set()

    # Удаляем дубликаты из ключа и добавляем его в квадрат
    for char in key:
        if char not in seen and char in alphabet:
            seen.add(char)
            key_square.append(char)

    # Добавляем оставшиеся буквы
    for char in alphabet:
        if char not in seen:
            key_square.append(char)

    # Преобразуем список в 6x6 квадрат
    return [key_square[i:i + 6] for i in range(0, 36, 6)]


def encrypt(plain_text, key):
    key_square = create_key_square(key)
    char_to_code = {key_square[i][j]: "ADFGVX"[i] + "ADFGVX"[j] for i in range(6) for j in range(6)}

    # Заменяем текст в код
    encrypted_text = ''.join(char_to_code[char] for char in plain_text.upper() if char in char_to_code)

    return encrypted_text


def decrypt(encrypted_text, key):
    key_square = create_key_square(key)
    code_to_char = {"ADFGVX"[i] + "ADFGVX"[j]: key_square[i][j] for i in range(6) for j in range(6)}

    # Группируем коды по два символа
    grouped_codes = [encrypted_text[i:i + 2] for i in range(0, len(encrypted_text), 2)]
    decrypted_text = ''.join(code_to_char[code] for code in grouped_codes if code in code_to_char)

    return decrypted_text


class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("Введите ключ шифрования")
        layout.addWidget(self.key_input)

        self.plaintext_input = QTextEdit(self)
        self.plaintext_input.setPlaceholderText("Введите текст для шифрования")
        layout.addWidget(self.plaintext_input)

        self.encrypt_button = QPushButton("Зашифровать", self)
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encrypt_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("Шифрование ADFGVX")
        self.show()

    def encrypt_text(self):
        key = self.key_input.text()
        plain_text = self.plaintext_input.toPlainText()

        if not key or not plain_text:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        encrypted_text = encrypt(plain_text, key)
        decrypted_text = decrypt(encrypted_text, key)

        self.result_label.setText(f"Зашифрованный текст: {encrypted_text}\nРасшифрованный текст: {decrypted_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CryptoApp()
    sys.exit(app.exec_())

