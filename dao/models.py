from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from dao import STATUS
from services.general_service import add_to_db

from .db_session import SqlAlchemyBase


class Project(SqlAlchemyBase):
    """Модель проекта"""
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    date_create = Column(DateTime, nullable=False)

    contracts = relationship("Contract", back_populates="project")

    def __init__(self, name, contracts, date_create=datetime.now()):
        self.name = name
        self.date_create = date_create
        self.contracts = contracts

    def __str__(self):
        from services.contract_service import get_all_contracts_to_project
        contracts = get_all_contracts_to_project(self.id)

        return f"Проект. ID: {self.id}. Название: {self.name}. Контракты:\n" + \
               "\n".join([str(contract) for contract in contracts])


class Contract(SqlAlchemyBase):
    """Модель договора"""
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    date_create = Column(DateTime, nullable=False)
    date_of_signing = Column(DateTime)
    status = Column(Integer, nullable=False)

    project_id = mapped_column(ForeignKey("project.id"))
    project = relationship("Project", back_populates="contracts")

    def __init__(self, name, data_create=datetime.now(), date_update=None, status=1, project_id=None):
        self.name = name
        self.date_create = data_create
        self.date_update = date_update
        self.status = status

        self.project_id = project_id

    def set_status(self, status, session):
        self.status = status
        if status == 2:
            self.date_of_signing = datetime.now()

        add_to_db(session, self)

    def __str__(self):
        return f"Контракт. ID: {self.id}. Название: {self.name}. Статус: {STATUS[self.status]}"
