from typing import Optional

from dao import STATUS_ACTIVATED
from dao.db_session import create_session
from dao.models import Contract, Project
from services.general_service import add_to_db


def have_active_contract() -> bool:
    """Функция проверяет, если ли активные договора"""
    return create_session().query(Contract).filter((Contract.status == STATUS_ACTIVATED) & (Contract.project_id == None)).count() >= 1


def create_project(name: str, contract: Contract):
    """Создание проекта"""
    project = Project(name, [contract])
    with create_session() as session:
        add_to_db(session, project)

    bind_project_to_contract(project.id, contract)
    return project


def bind_project_to_contract(project_id: int, contract: Contract):
    """Привязка проекта к контракту"""
    with create_session() as session:
        contract.project_id = project_id
        add_to_db(session, contract)


def get_safely_project_by_id(project_id: str) -> Optional[Project]:
    """Проверка на ввод id проекта, возвращает None или проект"""
    if not project_id.isdigit():
        return None

    project_id = int(project_id)
    project = __get_project_by_id(project_id)
    if project is None:
        return None

    return project


def check_project_havnt_active_contract(project_id) -> bool:
    """Проверка, что у проекта нет активных договоров"""
    from services.contract_service import get_all_contracts_to_project

    for contract in get_all_contracts_to_project(project_id):
        if contract.status == STATUS_ACTIVATED:
            return False
    return True


def get_all_projects():
    with create_session() as session:
        return session.query(Project).all()


def __get_project_by_id(project_id: int) -> Optional[Project]:
    """Возвращает проект по id"""
    with create_session() as session:
        return session.query(Project).filter(Project.id == project_id).first()
