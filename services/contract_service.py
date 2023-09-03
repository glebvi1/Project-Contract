from typing import List, Optional

from dao import STATUS_ACTIVATED, STATUS_END
from dao.db_session import create_session
from dao.models import Contract, Project
from services.general_service import add_to_db
from services.project_service import __get_project_by_id


def create_contract(name: str) -> Contract:
    """Создание договора по названию"""
    contract = Contract(name)

    with create_session() as session:
        add_to_db(session, contract)
    return contract


def confirm_contract(contract: Contract) -> None:
    """Подтверждение договора"""
    with create_session() as session:
        contract.set_status(STATUS_ACTIVATED, session)


def end_contract(contract: Contract):
    """Завершение договора"""
    with create_session() as session:
        contract.set_status(STATUS_END, session)


def get_safely_contract_by_id(contract_id: str) -> Optional[Contract]:
    """Проверка на ввод id договора, возвращает None или договор"""
    if not contract_id.isdigit():
        return None

    contract_id = int(contract_id)
    contract = get_contract_by_id(contract_id)
    if contract is None:
        return None

    return contract


def check_contract_is_active(contract: Contract) -> bool:
    """Функция проверяет можно ли добавить договор к проекту"""
    return contract is not None and contract.status == STATUS_ACTIVATED and __get_project_by_id(contract.project_id) is None


def get_all_contracts_to_project(project_id) -> List[Contract]:
    """Все договоры, которые принадлежат этому проекту"""
    with create_session() as session:
        return session.query(Contract).filter(Contract.project_id == project_id)


def get_contract_by_id(contract_id: int) -> Contract:
    """Поиск договора по id"""
    with create_session() as session:
        return session.query(Contract).filter(Contract.id == contract_id).first()
