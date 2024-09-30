from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Vacancy:
    """
    Представляет вакансию в системе HH.ru.

    Attributes:
        name (str): Название вакансии.
        desc (str): Описание вакансии.
        salary_from (Optional[int]): Минимальная зарплата. Может быть None, если зарплата не указана.
        salary_to (Optional[int]): Максимальная зарплата. Может быть None, если зарплата не указана.
        currency (str): Валюта зарплаты.
        url (str): URL вакансии.
        requirement (str): Требования к вакансии. По умолчанию 'Информация отсутствует'.
    """
    name: str
    desc: str
    salary_from: Optional[int] = field(default=None, compare=False)
    salary_to: Optional[int] = field(default=None, compare=False)
    currency: str = field(default="RUB", compare=False)
    url: str = field(default="", compare=False)
    requirement: str = field(default='Информация отсутствует', compare=False)

    def __post_init__(self):
        """
        Выполняет валидацию данных после инициализации экземпляра.
        """
        if self.salary_from is not None and self.salary_from < 0:
            raise ValueError("salary_from не может быть отрицательным.")
        if self.salary_to is not None and self.salary_to < 0:
            raise ValueError("salary_to не может быть отрицательным.")
        if self.salary_from is not None and self.salary_to is not None:
            if self.salary_from > self.salary_to:
                raise ValueError("salary_from не может быть больше salary_to.")
        if self.url and not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("url должен начинаться с 'http://' или 'https://'.")
        if not self.name:
            raise ValueError("Название вакансии не может быть пустым.")
        if not self.desc:
            self.desc = "Описание отсутствует"

    def get_salary_range(self) -> str:
        """
        Возвращает диапазон зарплаты в читаемом формате.

        Returns:
            str: Диапазон зарплаты или сообщение о его отсутствии.
        """
        if self.salary_from and self.salary_to:
            return f"{self.salary_from} - {self.salary_to} {self.currency}"
        elif self.salary_from:
            return f"От {self.salary_from} {self.currency}"
        elif self.salary_to:
            return f"До {self.salary_to} {self.currency}"
        else:
            return "Не указана"

    def to_dict(self) -> dict:
        """
        Преобразует объект Vacancy в словарь.

        Returns:
            dict: Словарь с данными вакансии.
        """
        return {
            "name": self.name,
            "desc": self.desc,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "url": self.url,
            "requirement": self.requirement
        }

    def average_salary(self) -> Optional[float]:
        """
        Вычисляет среднее значение зарплаты.

        Returns:
            Optional[float]: Среднее значение зарплаты или None, если зарплата не указана.
        """
        if self.salary_from is not None and self.salary_to is not None:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from is not None:
            return float(self.salary_from)
        elif self.salary_to is not None:
            return float(self.salary_to)
        return None

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.average_salary() == other.average_salary()

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (self.average_salary() or 0) < (other.average_salary() or 0)

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return not self <= other

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return not self < other
