import xml.sax
import xml.dom.minidom
from core.models.patient import Patient


class PatientHandler(xml.sax.ContentHandler):
    """
    Обработчик событий SAX для парсинга XML-файлов с данными пациентов.

    Этот класс реализует событийную модель: методы вызываются системным
    парсером автоматически при обнаружении соответствующих узлов в файле.
    """

    def __init__(self):
        """Инициализирует пустой список пациентов и временные буферы для данных."""
        super().__init__()
        self.patients = []
        self.current_data = ""
        self.p_data = {}

    def startElement(self, tag, attrs):
        """
        Вызывается парсером при встрече открывающего тега.

        :param tag: Имя обнаруженного тега.
        :param attrs: Атрибуты тега.
        """
        self.current_data = tag

    def characters(self, content):
        """
        Вызывается парсером для извлечения текстового содержимого внутри тегов.

        :param content: Строковое содержимое между тегами.
        """
        if content.strip():
            self.p_data[self.current_data] = content.strip()

    def endElement(self, tag):
        """
        Вызывается парсером при встрече закрывающего тега.
        Если закрывается тег 'patient', создает объект Patient и очищает буфер.

        :param tag: Имя закрывающегося тега.
        """
        if tag == "patient":
            self.patients.append(Patient(**self.p_data))
            self.p_data = {}


class PatientRepository:
    """
    Репозиторий для управления массивом записей пациентов.

    Отвечает за хранение данных в оперативной памяти, а также за их
    импорт (SAX) и экспорт (DOM) в формате XML.
    """

    def __init__(self):
        """Создает пустой список записей репозитория."""
        self.records = []

    def load_xml(self, path):
        """
        Загружает данные из XML-файла, используя SAX-парсер.

        :param path: Путь к файлу для чтения.
        """
        handler = PatientHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(path)
        self.records = handler.patients

    def save_xml(self, path):
        """
        Сохраняет текущий массив записей в XML-файл, используя DOM-парсер.

        :param path: Путь к файлу для сохранения.
        """
        impl = xml.dom.minidom.getDOMImplementation()
        doc = impl.createDocument(None, "patients", None)
        root = doc.documentElement
        for p in self.records:
            node = doc.createElement("patient")
            for key, val in p.__dict__.items():
                child = doc.createElement(key)
                child.appendChild(doc.createTextNode(str(val)))
                node.appendChild(child)
            root.appendChild(node)
        with open(path, "w", encoding="utf-8") as f:
            doc.writexml(f, addindent="  ", newl="\n", encoding="utf-8")

    def filter_records(self, c_type, val1, val2=None):
        """
        Фильтрует записи по заданным критериям.

        :param c_type: Тип фильтра (0 - ФИО/Адрес, 1 - Рождение, 2 - Врач/Прием).
        :param val1: Основное значение для поиска.
        :param val2: Дополнительное значение.
        :return: Список объектов Patient, подходящих под условия.
        """
        results = []
        for p in self.records:
            if self._matches(p, c_type, val1, val2):
                results.append(p)
        return results

    def delete_records(self, c_type, val1, val2=None):
        """
        Удаляет записи из репозитория по заданным критериям.

        :return: Количество удаленных записей.
        """
        initial = len(self.records)
        self.records = [p for p in self.records if not self._matches(p, c_type, val1, val2)]
        return initial - len(self.records)

    @staticmethod
    def _matches(p, c_type, v1, v2):
        """
        Проверяет соответствие записи пациента заданным критериям фильтрации.

        Реализует логику поиска по началу слов (prefix search) и обеспечивает
        независимость от порядка слов в поисковом запросе.

        :param p: Объект класса Patient для проверки.
        :param c_type: Индекс выбранного условия (0 - ФИО/Адрес, 1 - Дата рождения,
                       2 - Врач/Дата приема).
        :param v1: Основная строка поиска или дата (в формате yyyy-mm-dd).
        :param v2: Дополнительная дата приема для условия типа 2 (может быть None).
        :return: True, если запись соответствует условиям, иначе False.
        """

        def check_words(search_query, target_string):
            """
            Внутренняя функция для сопоставления слов запроса со словами в целевой строке.
            """
            if not search_query or not search_query.strip():
                return False
            search_words = search_query.lower().replace(',', ' ').replace('.', ' ').split()
            target_words = target_string.lower().replace(',', ' ').replace('.', ' ').split()

            return all(any(t_word.startswith(s_word) for t_word in target_words) for s_word in search_words)

        if c_type == 0:
            if not v1 or not v1.strip():
                return False
            return check_words(v1, p.full_name) or check_words(v1, p.address)

        if c_type == 1:
            return p.birth_date == v1

        if c_type == 2:
            match_doc = check_words(v1, p.doctor_name)
            match_date = (p.appointment_date == v2) if v2 else False

            if (v1 and v1.strip()) and v2:
                return match_doc or match_date
            return match_doc or match_date

        return False
