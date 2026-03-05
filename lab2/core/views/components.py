from PyQt6.QtWidgets import (QTableWidget, QTableWidgetItem,
                             QHeaderView, QWidget,
                             QHBoxLayout, QPushButton,
                             QSpinBox, QLabel)


class BaseTable(QTableWidget):
    """
    Класс базовой таблицы для отображения данных о пациентах.

    Наследуется от QTableWidget и настраивает структуру столбцов
    в соответствии с Вариантом 5 задания.
    """

    def __init__(self):
        """
        Инициализирует таблицу, устанавливает заголовки столбцов и
        растягивает их по всей ширине виджета.
        """
        super().__init__()
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Пациент", "Адрес", "Рождение", "Прием", "Врач", "Заключение"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def populate(self, data):
        """
        Заполняет таблицу переданным списком объектов пациентов.

        :param data: Срез списка объектов Patient для отображения на текущей странице.
        """
        self.setRowCount(0)
        for row, p in enumerate(data):
            self.insertRow(row)
            vals = [p.full_name, p.address, p.birth_date, p.appointment_date, p.doctor_name, p.conclusion]
            for col, v in enumerate(vals):
                self.setItem(row, col, QTableWidgetItem(str(v)))


class PaginationUI(QWidget):
    """
    Класс интерфейса управления постраничной навигацией.

    Содержит кнопки навигации, поле выбора количества записей на странице
    и текстовую информацию о текущем состоянии пагинации.
    """

    def __init__(self):
        """
        Создает элементы управления и размещает их в горизонтальном макете.
        """
        super().__init__()
        layout = QHBoxLayout(self)

        self.btn_first = QPushButton("<<")
        self.btn_prev = QPushButton("<")
        self.btn_next = QPushButton(">")
        self.btn_last = QPushButton(">>")

        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        self.spin.setValue(10)

        self.info = QLabel("Стр 1/1")

        for w in [self.btn_first, self.btn_prev, QLabel("Стр:"), self.spin, self.btn_next, self.btn_last, self.info]:
            layout.addWidget(w)

    def connect_controller(self, controller):
        """
        Связывает сигналы элементов интерфейса с методами контроллера пагинации.

        :param controller: Объект PaginationController, управляющий логикой переключения страниц.
        """
        self.btn_first.clicked.connect(controller.go_first)
        self.btn_prev.clicked.connect(controller.go_prev)
        self.btn_next.clicked.connect(controller.go_next)
        self.btn_last.clicked.connect(controller.go_last)
        self.spin.valueChanged.connect(controller.change_per_page)

    def update_info(self, cur, total, count):
        """
        Обновляет текстовую метку с информацией о текущем прогрессе пагинации.

        :param cur: Номер текущей активной страницы.
        :param total: Общее количество доступных страниц.
        :param count: Общее количество записей в текущем наборе данных.
        """
        self.info.setText(f"Стр {cur}/{total} (Всего: {count})")
