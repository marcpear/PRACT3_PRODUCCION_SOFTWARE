from datetime import date

from core.expense_service import ExpenseService
from core.no_tocar.sqlite_expense_repository import SQLiteExpenseRepository


def create_service():
    repo = SQLiteExpenseRepository()
    repo.empty()
    return ExpenseService(repo)


def test_create_and_list_expenses():
    service = create_service()

    service.create_expense(
        title="Comida", amount=10, description="", expense_date=date.today()
    )

    expenses = service.list_expenses()

    assert len(expenses) == 1
    assert expenses[0].title == "Comida"


def test_remove_expense():
    service = create_service()

    service.create_expense("A", 5, "", date.today())
    service.create_expense("B", 7, "", date.today())

    service.remove_expense(1)

    expenses = service.list_expenses()
    assert len(expenses) == 1
    assert expenses[0].title == "B"


def test_update_expense():
    service = create_service()

    service.create_expense("Café", 2, "", date.today())

    service.update_expense(expense_id=1, title="Café grande", amount=3)

    expense = service.list_expenses()[0]
    assert expense.title == "Café grande"
    assert expense.amount == 3


def test_update_non_existing_expense_does_nothing():
    service = create_service()

    service.update_expense(expense_id=999, title="Nada")

    assert service.list_expenses() == []


def test_total_amount():
    service = create_service()

    service.create_expense("A", 10, "", date.today())
    service.create_expense("B", 5, "", date.today())

    assert service.total_amount() == 15


def test_total_by_month():
    service = create_service()

    service.create_expense("Enero 1", 10, "", date(2025, 1, 10))
    service.create_expense("Enero 2", 5, "", date(2025, 1, 20))
    service.create_expense("Febrero", 7, "", date(2025, 2, 1))

    totals = service.total_by_month()

    assert totals["2025-01"] == 15
    assert totals["2025-02"] == 7


def test_create_multiple_expenses_and_list():
    """
    Verifica la creación y listado de múltiples gastos[cite: 20, 148].
    """
    service = create_service()

    service.create_expense(title="Pan", amount=3, description="Mercado")
    service.create_expense(title="Leche", amount=4, description="Supermercado")

    expenses = service.list_expenses()
    titles = [e.title for e in expenses]

    assert len(expenses) == 2
    assert "Pan" in titles
    assert "Leche" in titles


def test_remove_expense_reduces_total():
    service = create_service()

    service.create_expense("Libro", 10, "Estudio")
    service.create_expense("Revista", 5, "Ocio")

    service.remove_expense(1)

    expenses = service.list_expenses()
    assert len(expenses) == 1
    assert expenses[0].title == "Revista"


def test_update_expense_partial_fields():
    service = create_service()
    service.create_expense("Camiseta", 15, "Ropa")

    service.update_expense(expense_id=1, amount=18)

    expense = service.list_expenses()[0]
    assert expense.title == "Camiseta"
    assert expense.amount == 18
    assert expense.description == "Ropa"


def test_total_amount_after_removal():
    service = create_service()

    service.create_expense("Cursos", 30)
    service.create_expense("Internet", 25)

    assert service.total_amount() == 55

    service.remove_expense(1)
    assert service.total_amount() == 25
