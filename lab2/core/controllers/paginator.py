class PaginationController:
    """
    Контроллер для управления постраничным выводом данных в таблице.

    Обеспечивает связь между данными модели и графическим интерфейсом таблицы,
    вычисляя границы отображаемых срезов данных и управляя состоянием навигации.
    """

    def __init__(self, table, ui):
        """
        Инициализирует контроллер пагинации.

        :param table: Объект таблицы (BaseTable), в которой отображаются данные.
        :param ui: Объект интерфейса управления (PaginationUI).
        """
        self.table = table
        self.ui = ui
        self.data = []
        self.current_page = 1
        self.per_page = 10
        self.ui.connect_controller(self)

    def set_data(self, data):
        """
        Устанавливает новый набор данных для отображения и сбрасывает указатель на первую страницу.

        :param data: Список объектов, которые нужно распределить по страницам.
        """
        self.data = data
        self.current_page = 1
        self.refresh()

    def refresh(self):
        """
        Обновляет содержимое таблицы и информацию в интерфейсе управления.

        Рассчитывает общее количество страниц, корректирует текущую позицию
        и передает в таблицу срез данных, соответствующий текущей странице.
        """
        total_pages = max(1, (len(self.data) - 1) // self.per_page + 1)

        if self.current_page > total_pages:
            self.current_page = total_pages

        start = (self.current_page - 1) * self.per_page

        self.table.populate(self.data[start: start + self.per_page])
        self.ui.update_info(self.current_page, total_pages, len(self.data))

    def go_first(self):
        """Переход на самую первую страницу данных."""
        self.current_page = 1
        self.refresh()

    def go_last(self):
        """Переход на последнюю доступную страницу."""
        self.current_page = 9999
        self.refresh()

    def go_next(self):
        """Переход на следующую страницу (без проверки границ, корректировка произойдет в refresh)."""
        self.current_page += 1
        self.refresh()

    def go_prev(self):
        """Переход на предыдущую страницу с ограничением минимального значения."""
        self.current_page = max(1, self.current_page - 1)
        self.refresh()

    def change_per_page(self, val):
        """
        Изменяет количество записей, отображаемых на одной странице.

        :param val: Новое количество записей (извлекается из QSpinBox в UI).
        """
        self.per_page = val
        self.refresh()
