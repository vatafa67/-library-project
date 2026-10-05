"""
Тесты для работы с базой данных с использованием pytest.
"""
import pytest
import sqlite3
import os


@pytest.fixture
def test_db():
    """
    Фикстура: создаёт тестовую базу данных перед каждым тестом
    и удаляет её после.
    """
    db_path = 'test_pytest.db'

    # Создаём БД
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        quantity INTEGER DEFAULT 1
    )
    ''')
    cursor.executemany(
        "INSERT INTO books (title, author, year, quantity) VALUES (?, ?, ?, ?)",
        [
            ('Война и мир', 'Лев Толстой', 1869, 3),
            ('Анна Каренина', 'Лев Толстой', 1877, 2),
            ('Преступление и наказание', 'Федор Достоевский', 1866, 1),
        ]
    )
    conn.commit()
    conn.close()

    yield db_path  # Передаём путь к БД в тест

    # Очистка после теста
    if os.path.exists(db_path):
        os.remove(db_path)


def test_search_by_author(test_db):
    """Поиск книг по автору."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", ('%Толстой%',))
    books = cursor.fetchall()
    conn.close()

    assert len(books) == 2
    assert books[0][2] == 'Лев Толстой'


def test_search_nonexistent_author(test_db):
    """Поиск несуществующего автора."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", ('%Пушкин%',))
    books = cursor.fetchall()
    conn.close()

    assert len(books) == 0


def test_book_count(test_db):
    """Проверка количества книг."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 3


@pytest.mark.parametrize("author, expected_count", [
    ("Толстой", 2),
    ("Достоевский", 1),
    ("Пушкин", 0),
    ("", 3),
])
def test_search_parametrized(test_db, author, expected_count):
    """Параметризованный поиск по автору."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", (f'%{author}%',))
    books = cursor.fetchall()
    conn.close()

    assert len(books) == expected_count
