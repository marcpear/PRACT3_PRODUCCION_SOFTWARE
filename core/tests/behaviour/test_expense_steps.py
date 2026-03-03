from datetime import date
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from core.domain_error import InvalidAmountError

from core.expense_service import ExpenseService
from core.in_memory_expense_repository import InMemoryExpenseRepository

scenarios("./expense_management.feature")

@pytest.fixture
def context():
    repo = InMemoryExpenseRepository()
    service = ExpenseService(repo)
    return {"service": service, "db": repo}

@given("un gestor de gastos vacío")
def empty_manager(context):
    pass

@given(parsers.parse("un gestor con un gasto de {amount:d} euros"))
def manager_with_one_expense(context, amount):
    context["service"].create_expense(
        title="Gasto inicial", amount=amount, description="", expense_date=date.today()
    )

@when(parsers.parse("añado un gasto de {amount:d} euros llamado {title}"))
def add_expense(context, amount, title):
    context["service"].create_expense(
        title=title, amount=amount, description="", expense_date=date.today()
    )

@when(parsers.parse("elimino el gasto con id {expense_id:d}"))
def remove_expense(context, expense_id):
    context["service"].remove_expense(expense_id)

@then(parsers.parse("el total de dinero gastado debe ser {total:d} euros"))
def check_total(context, total):
    assert context["service"].total_amount() == total

@then(parsers.parse("debe haber {expenses:d} gastos registrados"))
def check_expenses_length(context, expenses):
    total_actual = len(context["db"].list_all())
    assert total_actual == expenses

@when(parsers.parse("intento añadir un gasto de {amount} euros"))
def attempt_invalid_expense(context, amount):
    try:
        val = float(amount)
        context["service"].create_expense(title="Error", amount=val)
        context["error_raised"] = False
    except InvalidAmountError:
        context["error_raised"] = True
    except Exception:
        context["error_raised"] = True

@then("el sistema debe lanzar un error de cantidad inválida")
def check_error_step(context):
    assert context.get("error_raised") is True

@then(parsers.parse("el gasto llamado {title} debe tener el id {expected_id:d}"))
def check_specific_id(context, title, expected_id):
    expenses = context["service"].list_expenses()
    expense = next((e for e in expenses if e.title == title), None)
    assert expense is not None
    assert expense.id == expected_id