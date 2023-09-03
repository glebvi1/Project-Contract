from typing import Optional

from dao.models import Contract
from services.contract_service import (check_contract_is_active,
                                       confirm_contract, create_contract,
                                       end_contract, get_safely_contract_by_id)
from services.project_service import (bind_project_to_contract,
                                      check_project_havnt_active_contract,
                                      create_project, get_all_projects,
                                      get_safely_project_by_id,
                                      have_active_contract)
from strings import UNCORRECT_INPUT, UNKNOW_COMMAND


def process_query():
    """Обработка первичного запроса пользователя"""
    query = input("Команда: ")

    if query == "1а":
        __process_create_project()
    elif query == "1б":
        __process_add_contract_to_project()
    elif query == "1в":
        __process_end_contract_by_project()
    elif query == "2а":
        __process_create_contract()
    elif query == "2б":
        __process_confirm_contract()
    elif query == "2в":
        __process_end_contract()
    elif query == "3":
        __process_get_all()
    elif query == "4":
        print("До свидания!")
        return
    else:
        print(UNKNOW_COMMAND)

    print()
    process_query()


def __process_create_contract():
    """Функция создания договора"""
    print("Создание контракта")
    name = input("Введите название: ")
    contract = create_contract(name)
    print(f"Контракт создан: {contract}")


def __process_confirm_contract():
    """Функция подтверждения договора"""
    contract_id = input("Введите id договора: ")
    contract = get_safely_contract_by_id(contract_id)

    if contract is None:
        print(UNCORRECT_INPUT)
        return

    confirm_contract(contract)

    print(contract)
    print("Договор успешно подтвержден!")


def __process_end_contract():
    """Функция завершения договора"""
    contract_id = input("Введите id договора: ")
    contract = get_safely_contract_by_id(contract_id)

    if contract is None:
        print(UNCORRECT_INPUT)
        return

    end_contract(contract)
    print(contract)
    print("Договор успешно завершен!")


def __process_create_project():
    """Функция создания проекта"""
    if not have_active_contract():
        print("Активных договоров нет!")
        return

    name = input("Введите названия проекта: ")
    contract = __process_bind_project_to_contract()
    if contract is None:
        print("Это не подходящий проект!")
        return

    project = create_project(name, contract)

    print(project)
    print("Проект успешно создан!")


def __process_add_contract_to_project():
    """Функция добавления договоров к проекту"""
    project_id = input("Введите id проекта: ")
    project = get_safely_project_by_id(project_id)
    if project is None:
        print(UNCORRECT_INPUT)
        return
    if not check_project_havnt_active_contract(project.id):
        print("У этого проекта уже есть активный договор.")
        return

    contract = __process_bind_project_to_contract()
    if contract is None:
        print("Это не подходящий проект!")
        return

    bind_project_to_contract(project.id, contract)

    print(project)
    print("Договор добавлен!")


def __process_end_contract_by_project():
    """Завершения договора по проекту"""
    project_id = input("Введите id проекта: ")
    project = get_safely_project_by_id(project_id)
    if project is None:
        print(UNCORRECT_INPUT)
        return

    print(project)

    contract_id = input("Введите id договора: ")
    contract = get_safely_contract_by_id(contract_id)

    if contract is None:
        print(UNCORRECT_INPUT)
        return

    end_contract(contract)
    print(contract)
    print("Договор успешно завершен!")


def __process_bind_project_to_contract() -> Optional[Contract]:
    """Функция привязки контрактов к проекту"""
    contract_id = input("Введите id договора: ")
    contract = get_safely_contract_by_id(contract_id)

    if check_contract_is_active(contract):
        return contract
    return None


def __process_get_all():
    for project in get_all_projects():
        print(project, end="\n\n")
