import customtkinter

# Устанавливаем внешний вид приложения (тёмный режим)
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class CalculatorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- Настройка основного окна ---
        self.title("Calculator")
        self.geometry("300x450")
        self.resizable(False, False) # Запрещаем изменение размера

        # --- Переменные состояния ---
        self.expression = ""

        # --- Настройка сетки (grid) для размещения виджетов ---
        # Делаем ячейки растягиваемыми для равномерного распределения кнопок
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)

        # --- Поле ввода/вывода (Дисплей) ---
        self.display = customtkinter.CTkEntry(
            self,
            font=("Arial", 30),
            placeholder_text="0",
            justify='right', # Выравнивание текста по правому краю
            fg_color="#1F1F1F", # Фон дисплея (немного темнее общего фона)
            border_width=0,
            corner_radius=10
        )
        # Занимает 4 колонки в первой строке, с отступом снизу
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(20, 10), sticky="nsew")

        # --- Создание кнопок ---
        # Список кнопок для удобства размещения в цикле
        buttons = [
            ('C', 1, 0, 'gray'), ('/', 1, 1, 'orange'), ('*', 1, 2, 'orange'), ('DEL', 1, 3, 'gray'),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('-', 2, 3, 'orange'),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('+', 3, 3, 'orange'),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('=', 4, 3, 'green', 2),
            ('0', 5, 0, None, 2), ('.', 5, 2), ('%', 5, 3)
        ]

        # Размещение кнопок
        for (text, row, col, color, colspan) in [(b[0], b[1], b[2], b[3] if len(b) > 3 else 'blue', b[4] if len(b) > 4 else 1) for b in buttons]:
            self.create_button(text, row, col, color, colspan)

    def create_button(self, text, row, col, color='blue', colspan=1):
        """Создает и размещает кнопку на сетке."""
        # Выбор цвета кнопки
        if color == 'orange':
            fg_color = "#FF9500"
            hover_color = "#FFA520"
        elif color == 'gray':
            fg_color = "#505050"
            hover_color = "#686868"
        elif color == 'green':
            fg_color = "#34A853"
            hover_color = "#4BB669"
        else: # blue
            fg_color = "#2B2B2B"
            hover_color = "#3A3A3A"

        # Создание самой кнопки
        button = customtkinter.CTkButton(
            self,
            text=text,
            command=lambda t=text: self.button_click(t),
            font=("Arial", 20, "bold"),
            fg_color=fg_color,
            hover_color=hover_color,
            text_color="white",
            corner_radius=10
        )
        # Размещение кнопки
        button.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")

    def button_click(self, char):
        """Обрабатывает нажатия на кнопки."""

        if char == 'C':
            # Очистить все
            self.expression = ""
            self.display.delete(0, customtkinter.END)
            self.display.insert(0, "0")
        elif char == 'DEL':
            # Удалить последний символ
            self.expression = self.expression[:-1]
            self.display.delete(0, customtkinter.END)
            if self.expression:
                self.display.insert(0, self.expression)
            else:
                self.display.insert(0, "0")
        elif char == '=':
            # Вычислить результат
            try:
                # Замена % на /100 для корректного вычисления
                # (хотя в реальном калькуляторе % работает сложнее)
                safe_expression = self.expression.replace('%', '/100')
                result = str(eval(safe_expression))
                self.expression = result
                self.display.delete(0, customtkinter.END)
                self.display.insert(0, result)
            except Exception:
                self.expression = ""
                self.display.delete(0, customtkinter.END)
                self.display.insert(0, "Ошибка")
        elif char == '%':
            # Добавляем символ процента.
            self.expression += char
            self.display.delete(0, customtkinter.END)
            self.display.insert(0, self.expression)
        else:
            # Добавление символа в выражение
            if self.display.get() == "0" and char in "123456789":
                self.expression = char
            elif self.expression == "0" and char == ".":
                self.expression += char
            elif self.display.get() == "0" and char not in "/*-+":
                # Это условие позволяет начать ввод после 0
                self.expression = char
            else:
                self.expression += char

            self.display.delete(0, customtkinter.END)
            self.display.insert(0, self.expression)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()