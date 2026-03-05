from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QDateEdit, QComboBox, QPushButton, QLabel,
                             QMessageBox, QCheckBox, QWidget, QHBoxLayout)
from PyQt6.QtCore import QDate
from core.views.components import BaseTable, PaginationUI
from core.controllers.paginator import PaginationController


class AddDialog(QDialog):
    """
    Диалоговое окно для добавления новой записи о пациенте в систему.

    Обеспечивает ввод всех атрибутов сущности "Пациент" с использованием
    соответствующих типов виджетов (строки, даты) и базовую валидацию.
    """

    def __init__(self, parent=None):
        """
        Инициализирует форму ввода с предопределенными значениями дат.

        :param parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        form = QFormLayout(self)

        self.inputs = {
            "full_name": QLineEdit(),
            "address": QLineEdit(),
            "birth_date": QDateEdit(calendarPopup=True, date=QDate.currentDate().addYears(-20)),
            "appointment_date": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "doctor_name": QLineEdit(),
            "conclusion": QLineEdit()
        }

        for label, widget in zip(["ФИО", "Адрес", "Рождение", "Прием", "Врач", "Заключение"], self.inputs.values()):
            form.addRow(label, widget)

        btn = QPushButton("Сохранить")
        btn.clicked.connect(self.accept)
        form.addRow(btn)

    def accept(self):
        """
        Переопределенный метод подтверждения диалога.

        Проверяет все текстовые поля на наличие данных. Если хотя бы одно поле
        пустое, прерывает операцию и выводит предупреждение.
        """
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit) and not widget.text().strip():
                QMessageBox.warning(self, "Ошибка валидации", "Все текстовые поля должны быть заполнены.")
                return
        super().accept()

    def get_data(self):
        """
        Собирает введенные пользователем данные в словарь.

        :return: Словарь с данными пациента, где даты приведены к формату 'yyyy-MM-dd'.
        """
        return {k: (v.date().toString("yyyy-MM-dd") if isinstance(v, QDateEdit) else v.text().strip())
                for k, v in self.inputs.items()}


class SearchDeleteWidget(QVBoxLayout):
    """
    Универсальный виджет выбора критериев для поиска или удаления записей.

    Реализует динамическую смену полей ввода в зависимости от выбранного
    типа фильтрации согласно требованиям Варианта 5.
    """

    def __init__(self):
        """Инициализирует выпадающий список условий и контейнеры для ввода значений."""
        super().__init__()
        self.combo = QComboBox()
        self.combo.addItems(["ФИО или Адрес", "Дата рождения", "Врач или Дата приема"])

        self.txt = QLineEdit(placeholderText="Введите текст...")
        self.d1 = QDateEdit(calendarPopup=True, visible=False)

        self.d2_container = QWidget()
        self.d2_container.setVisible(False)
        d2_lay = QHBoxLayout(self.d2_container)
        d2_lay.setContentsMargins(0, 0, 0, 0)

        self.d2_cb = QCheckBox("Искать по дате:")
        self.d2 = QDateEdit(calendarPopup=True)
        self.d2.setEnabled(False)
        self.d2_cb.toggled.connect(self.d2.setEnabled)

        d2_lay.addWidget(self.d2_cb)
        d2_lay.addWidget(self.d2)

        self.addWidget(QLabel("Условие поиска:"))
        self.addWidget(self.combo)
        self.addWidget(self.txt)
        self.addWidget(self.d1)
        self.addWidget(self.d2_container)

        self.combo.currentIndexChanged.connect(self._update_visibility)

    def _update_visibility(self, idx):
        """
        Управляет видимостью полей ввода при смене типа фильтра.

        :param idx: Индекс выбранного условия в QComboBox.
        """
        self.txt.setVisible(idx != 1)
        self.d1.setVisible(idx == 1)
        self.d2_container.setVisible(idx == 2)

    def get_criteria(self):
        """
        Возвращает текущие критерии фильтрации, выбранные пользователем.

        :return: Кортеж (индекс условия, основное значение, дата/None).
        """
        idx = self.combo.currentIndex()
        v1 = self.txt.text().strip()

        if idx == 1:
            return idx, self.d1.date().toString("yyyy-MM-dd"), None

        if idx == 2:
            v2 = self.d2.date().toString("yyyy-MM-dd") if self.d2_cb.isChecked() else None
            return idx, v1, v2

        return idx, v1, None


class SearchDialog(QDialog):
    """
    Диалоговое окно поиска записей.

    Включает в себя виджет критериев, таблицу результатов с пагинацией
    и контроллер для управления отображением.
    """

    def __init__(self, model_filter_func, parent=None):
        """
        Инициализирует окно поиска и настраивает систему пагинации результатов.

        :param model_filter_func: Функция фильтрации из модели (PatientRepository.filter_records).
        :param parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Поиск (Вариант 5)")
        self.resize(800, 500)
        layout = QVBoxLayout(self)

        self.crit = SearchDeleteWidget()
        layout.addLayout(self.crit)

        self.table = BaseTable()
        self.pg_ui = PaginationUI()
        layout.addWidget(self.table)
        layout.addWidget(self.pg_ui)

        self.paginator = PaginationController(self.table, self.pg_ui)

        btn = QPushButton("Найти")
        btn.clicked.connect(lambda: self.paginator.set_data(model_filter_func(*self.crit.get_criteria())))
        layout.addWidget(btn)
