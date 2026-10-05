"""
Тесты для функций библиотеки с использованием pytest.
Включают тестирование граничных случаев.
"""
import pytest
from library_functions import (
    validate_year,
    validate_quantity,
    validate_student_card,
    calculate_overdue_days,
    format_book_title,
)


# ==========================================
# ТЕСТЫ ДЛЯ validate_year
# ==========================================
def test_validate_year_valid():
    """Проверяет корректный год."""
    assert validate_year(1869) is True
    assert validate_year(2000) is True
    assert validate_year(2100) is True


def test_validate_year_too_old():
    """Граничный случай: год слишком старый."""
    with pytest.raises(ValueError):
        validate_year(999)


def test_validate_year_too_new():
    """Граничный случай: год из будущего."""
    with pytest.raises(ValueError):
        validate_year(2101)


def test_validate_year_not_integer():
    """Граничный случай: год — не число."""
    with pytest.raises(ValueError):
        validate_year("1869")


@pytest.mark.parametrize("year", [1000, 1500, 1869, 2000, 2026, 2100])
def test_validate_year_boundaries(year):
    """Параметризованный тест: проверка границ диапазона."""
    assert validate_year(year) is True


# ==========================================
# ТЕСТЫ ДЛЯ validate_quantity
# ==========================================
def test_validate_quantity_valid():
    """Проверяет корректное количество."""
    assert validate_quantity(1) is True
    assert validate_quantity(100) is True


def test_validate_quantity_zero():
    """Граничный случай: ноль экземпляров."""
    with pytest.raises(ValueError):
        validate_quantity(0)


def test_validate_quantity_negative():
    """Граничный случай: отрицательное количество."""
    with pytest.raises(ValueError):
        validate_quantity(-5)


def test_validate_quantity_float():
    """Граничный случай: дробное число."""
    with pytest.raises(ValueError):
        validate_quantity(1.5)


# ==========================================
# ТЕСТЫ ДЛЯ validate_student_card
# ==========================================
def test_validate_student_card_valid():
    """Проверяет корректный номер билета."""
    assert validate_student_card("СБ-001") is True
    assert validate_student_card("12345") is True


def test_validate_student_card_empty():
    """Граничный случай: пустая строка."""
    with pytest.raises(ValueError):
        validate_student_card("")


def test_validate_student_card_whitespace():
    """Граничный случай: только пробелы."""
    with pytest.raises(ValueError):
        validate_student_card(" ")


def test_validate_student_card_none():
    """Граничный случай: None."""
    with pytest.raises(ValueError):
        validate_student_card(None)


def test_validate_student_card_too_long():
    """Граничный случай: слишком длинный номер."""
    with pytest.raises(ValueError):
        validate_student_card("А" * 21)


# ==========================================
# ТЕСТЫ ДЛЯ calculate_overdue_days
# ==========================================
def test_calculate_overdue_days_not_overdue():
    """Книга возвращена вовремя."""
    assert calculate_overdue_days("2026-10-01", "2026-09-25") == 0


def test_calculate_overdue_days_on_time():
    """Книга возвращена в срок."""
    assert calculate_overdue_days("2026-10-01", "2026-10-01") == 0


def test_calculate_overdue_days_overdue():
    """Книга просрочена на 5 дней."""
    assert calculate_overdue_days("2026-10-01", "2026-10-06") == 5


def test_calculate_overdue_days_long_overdue():
    """Книга просрочена на 30 дней."""
    assert calculate_overdue_days("2026-10-01", "2026-10-31") == 30


def test_calculate_overdue_days_invalid_format():
    """Граничный случай: неверный формат даты."""
    with pytest.raises(ValueError):
        calculate_overdue_days("01.10.2026", "2026-10-06")


@pytest.mark.parametrize("due, returned, expected", [
    ("2026-10-01", "2026-09-30", 0),
    ("2026-10-01", "2026-10-01", 0),
    ("2026-10-01", "2026-10-02", 1),
    ("2026-10-01", "2026-10-10", 9),
    ("2026-10-01", "2026-11-01", 31),
])
def test_calculate_overdue_days_parametrized(due, returned, expected):
    """Параметризованный тест для расчёта просрочки."""
    assert calculate_overdue_days(due, returned) == expected


# ==========================================
# ТЕСТЫ ДЛЯ format_book_title
# ==========================================
def test_format_book_title_short():
    """Короткое название не обрезается."""
    assert format_book_title("Война и мир") == "Война и мир"


def test_format_book_title_exact_length():
    """Название ровно 30 символов."""
    title = "А" * 30
    assert format_book_title(title) == title


def test_format_book_title_long():
    """Длинное название обрезается."""
    title = "Очень длинное название книги, которое точно превышает 30 символов"
    result = format_book_title(title)
    assert len(result) == 30
    assert result.endswith("...")


def test_format_book_title_empty():
    """Граничный случай: пустое название."""
    with pytest.raises(ValueError):
        format_book_title("")


def test_format_book_title_whitespace():
    """Граничный случай: только пробелы."""
    with pytest.raises(ValueError):
        format_book_title(" ")
