from PyQt6.QtWidgets import (QMainWindow, QWidget,
                             QVBoxLayout, QFileDialog,
                             QMessageBox, QToolBar,
                             QDialog, QPushButton)
from PyQt6.QtGui import QAction
from core.views.components import BaseTable, PaginationUI
from core.views.dialogs import AddDialog, SearchDialog, SearchDeleteWidget
from core.controllers.paginator import PaginationController
from core.models.patient import Patient


class MainWindow(QMainWindow):
    """
    Главное окно интеллектуальной системы учета пациентов (Вариант 5).

    Является центральным узлом View в архитектуре MVC. Объединяет таблицу
    отображения, элементы управления пагинацией, меню и панели инструментов,
    а также координирует вызов диалоговых окон.
    """

    def __init__(self, repo):
        """
        Инициализирует главное окно и настраивает его компоненты.

        :param repo: Объект PatientRepository (Model), предоставляющий доступ к данным.
        """
        super().__init__()
        self.repo = repo
        self.setWindowTitle("Система управления записями пациентов (Вариант 5)")
        self.resize(1100, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.table = BaseTable()
        self.pg_ui = PaginationUI()
        layout.addWidget(self.table)
        layout.addWidget(self.pg_ui)

        self.paginator = PaginationController(self.table, self.pg_ui)

        self._create_actions()
        self._create_menu()
        self._create_toolbar()

    def _create_actions(self):
        """Создает объекты QAction для использования в меню и на панели инструментов."""
        self.act_load = QAction("Открыть (SAX)", self)
        self.act_load.triggered.connect(self._load)

        self.act_save = QAction("Сохранить (DOM)", self)
        self.act_save.triggered.connect(self._save)

        self.act_add = QAction("Добавить", self)
        self.act_add.triggered.connect(self._add)

        self.act_search = QAction("Поиск", self)
        self.act_search.triggered.connect(self._search)

        self.act_delete = QAction("Удалить", self)
        self.act_delete.triggered.connect(self._delete)

    def _create_menu(self):
        """Конструирует главное меню приложения."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Файл")
        file_menu.addAction(self.act_load)
        file_menu.addAction(self.act_save)

        edit_menu = menubar.addMenu("&Записи")
        edit_menu.addAction(self.act_add)
        edit_menu.addAction(self.act_search)
        edit_menu.addAction(self.act_delete)

    def _create_toolbar(self):
        """Создает панель инструментов с кнопками быстрого доступа."""
        toolbar = QToolBar("Главная панель")
        self.addToolBar(toolbar)
        toolbar.addActions([self.act_load, self.act_save, self.act_add, self.act_search, self.act_delete])

    def _refresh_main_table(self):
        """Синхронизирует отображение таблицы с текущим состоянием данных в репозитории."""
        self.paginator.set_data(self.repo.records)

    def _load(self):
        """
        Вызывает диалог выбора файла и инициирует загрузку данных через SAX-парсер.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Загрузить данные", "", "XML Files (*.xml)")
        if path:
            try:
                self.repo.load_xml(path)
                self._refresh_main_table()
                QMessageBox.information(self, "Успех", f"Загружено {len(self.repo.records)} записей.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл:\n{str(e)}")

    def _save(self):
        """
        Вызывает диалог сохранения файла и инициирует экспорт данных через DOM-парсер.
        """
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", "XML Files (*.xml)")
        if path:
            try:
                self.repo.save_xml(path)
                QMessageBox.information(self, "Успех", "Данные успешно сохранены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def _add(self):
        """Вызывает диалог добавления записи и обновляет главную таблицу при успехе."""
        dlg = AddDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            new_patient = Patient(**data)
            self.repo.records.append(new_patient)
            self._refresh_main_table()

    def _search(self):
        """Открывает специализированное окно поиска с собственной пагинацией."""
        dlg = SearchDialog(self.repo.filter_records, self)
        dlg.exec()

    def _delete(self):
        """
        Вызывает модальное окно удаления записей по критериям Варианта 5.
        Выводит сообщение о результатах операции (количество удаленных строк).
        """
        dlg = QDialog(self)
        dlg.setWindowTitle("Удаление записей")
        lay = QVBoxLayout(dlg)

        crit_widget = SearchDeleteWidget()
        lay.addLayout(crit_widget)

        btn = QPushButton("Удалить выбранное")
        lay.addWidget(btn)

        def run_delete():
            """Внутренняя функция для выполнения операции удаления."""
            count = self.repo.delete_records(*crit_widget.get_criteria())
            self._refresh_main_table()
            if count > 0:
                QMessageBox.information(dlg, "Результат", f"Удалено записей: {count}")
            else:
                QMessageBox.warning(dlg, "Результат", "Записей по данным условиям не найдено.")
            dlg.accept()

        btn.clicked.connect(run_delete)
        dlg.exec()
