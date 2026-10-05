"""
Модуль с функциями для библиотеки.
Содержит функции с обработкой граничных случаев.
"""
import sqlite3


def validate_year(year):
    """
    Проверяет корректность года издания книги.

    Args:
        year (int): год издания

    Returns:
        bool: True, если год корректен

    Raises:
        ValueError: если год не входит в диапазон 1000-2100
    """
    if not isinstance(year, int):
        raise ValueError("Год должен быть целым числом")

    if year < 1000 or year > 2100:
        raise ValueError(f"Год {year} вне допустимого диапазона (1000-2100)")

    return True


def validate_quantity(quantity):
    """
    Проверяет корректность количества экземпляров.

    Args:
        quantity (int): количество экземпляров

    Returns:
        bool: True, если количество корректно

    Raises:
        ValueError: если количество отрицательное или ноль
    """
    if not isinstance(quantity, int):
        raise ValueError("Количество должно быть целым числом")

    if quantity <= 0:
        raise ValueError(f"Количество должно быть положительным (получено {quantity})")

    return True


def validate_student_card(student_card):
    """
    Проверяет корректность номера студенческого билета.

    Args:
        student_card (str): номер студенческого билета

    Returns:
        bool: True, если номер корректен

    Raises:
        ValueError: если номер пустой или слишком длинный
    """
    if not student_card or not student_card.strip():
        raise ValueError("Номер студенческого билета не может быть пустым")

    if len(student_card) > 20:
        raise ValueError("Номер студенческого билета слишком длинный (макс. 20 символов)")

    return True


def calculate_overdue_days(due_date, return_date):
    """
    Вычисляет количество дней просрочки.

    Args:
        due_date (str): планируемая дата возврата (YYYY-MM-DD)
        return_date (str): фактическая дата возврата (YYYY-MM-DD)

    Returns:
        int: количество дней просрочки (0, если не просрочено)

    Raises:
        ValueError: если даты в неверном формате
    """
    from datetime import datetime

    try:
        due = datetime.strptime(due_date, '%Y-%m-%d')
        returned = datetime.strptime(return_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Даты должны быть в формате YYYY-MM-DD")

    delta = (returned - due).days

    if delta < 0:
        return 0  # Не просрочено

    return delta


def format_book_title(title, max_length=30):
    """
    Форматирует название книги для вывода.

    Args:
        title (str): название книги
        max_length (int): максимальная длина

    Returns:
        str: отформатированное название

    Raises:
        ValueError: если название пустое
    """
    if not title or not title.strip():
        raise ValueError("Название книги не может быть пустым")

    if len(title) <= max_length:
        return title

    return title[:max_length - 3] + "..."
