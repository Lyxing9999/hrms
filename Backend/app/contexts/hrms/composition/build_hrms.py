from __future__ import annotations

from pymongo.database import Database

from app.contexts.hrms.composition.repositories import HrmsRepositories
from app.contexts.hrms.composition.application_services import HrmsApplicationServices


def build_hrms_repositories(db: Database) -> HrmsRepositories:
    return HrmsRepositories(db=db)


def build_hrms(db: Database) -> HrmsApplicationServices:
    repositories = build_hrms_repositories(db)
    return HrmsApplicationServices(repositories=repositories)