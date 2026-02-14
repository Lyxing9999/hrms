# HRMS Complete Implementation Guide

## 🎯 Overview

This guide provides a complete implementation roadmap for the HRMS system. The system is built following DDD architecture patterns established in the Employee and Leave modules.

## 📊 Current Status

### ✅ Completed
- Employee Management (8 endpoints) - Backend + Frontend
- Leave Management (9 endpoints) - Backend + Frontend
- Domain models for: DeductionRule, WorkLocation, PublicHoliday
- Error exceptions for configuration modules
- Request DTOs for configuration modules

### 🔨 In Progress
- Configuration modules (Working Schedule, Location, Holidays, Deduction Rules)

## 🏗️ Implementation Architecture

### File Structure Pattern
Every module follows this structure:

```
module_name/
├── domain/module.py              # Business entity
├── services/module_service.py    # Application logic
├── repositories/module_repository.py  # Data access
├── read_models/module_read_model.py   # Query optimization
├── factories/module_factory.py   # Object creation
├── mapper/module_mapper.py       # DTO ↔ Domain conversion
├── policies/module_policy.py     # Business rules (optional)
├── data_transfer/
│   ├── request/module_request.py # Request DTOs
│   └── response/module_response.py # Response DTOs
├── routes/module_route.py        # HTTP endpoints
└── errors/module_exceptions.py   # Domain exceptions
```

## 📝 Implementation Checklist

### Phase 1: Configuration Modules (Foundation)

#### 1. Working Schedule Management
- [x] Domain model (`working_schedule.py`) - EXISTS
- [x] Request DTOs - CREATED
- [ ] Response DTOs
- [ ] Factory
- [ ] Mapper
- [ ] Repository
- [ ] Read Model
- [ ] Service
- [ ] Routes
- [ ] Frontend API service
- [ ] Frontend page

#### 2. Work Location Management
- [x] Domain model (`work_location.py`) - CREATED
- [x] Error exceptions - CREATED
- [x] Request DTOs - CREATED
- [ ] Response DTOs
- [ ] Factory
- [ ] Mapper
- [ ] Repository
- [ ] Read Model
- [ ] Service
- [ ] Routes
- [ ] Frontend API service
- [ ] Frontend page

#### 3. Public Holiday Management
- [x] Domain model (`public_holiday.py`) - CREATED
- [x] Error exceptions - CREATED
- [x] Request DTOs - CREATED
- [ ] Response DTOs
- [ ] Factory
- [ ] Mapper
- [ ] Repository
- [ ] Read Model
- [ ] Service
- [ ] Routes
- [ ] Frontend API service
- [ ] Frontend page

#### 4. Deduction Rules
- [x] Domain model (`deduction_rule.py`) - CREATED
- [x] Error exceptions - CREATED
- [x] Request DTOs - CREATED
- [ ] Response DTOs
- [ ] Factory
- [ ] Mapper
- [ ] Repository
- [ ] Read Model
- [ ] Service
- [ ] Routes
- [ ] Frontend API service
- [ ] Frontend page

### Phase 2: Core Operations

#### 5. Attendance System
- [ ] Domain model (`attendance.py`)
- [ ] Error exceptions
- [ ] Request/Response DTOs
- [ ] Factory, Mapper, Repository, Read Model
- [ ] Service (with location validation)
- [ ] Routes (8 endpoints)
- [ ] Frontend API service
- [ ] Frontend page

#### 6. Overtime Management
- [ ] Domain model (`overtime.py`)
- [ ] Error exceptions
- [ ] Request/Response DTOs
- [ ] Factory, Mapper, Repository, Read Model
- [ ] Service (with rate calculation)
- [ ] Routes (7 endpoints)
- [ ] Frontend API service
- [ ] Frontend page

### Phase 3: Payroll

#### 7. Payroll System
- [ ] Domain model (`payroll.py`) - EXISTS (basic)
- [ ] Error exceptions
- [ ] Request/Response DTOs
- [ ] Factory, Mapper, Repository, Read Model
- [ ] Service (calculation engine)
- [ ] Routes (8 endpoints)
- [ ] Frontend API service
- [ ] Frontend page

### Phase 4: Reporting

#### 8. Reports & Analytics
- [ ] Read models for reports
- [ ] Service (report generation)
- [ ] Routes (6 endpoints)
- [ ] Frontend API service
- [ ] Frontend page

## 🔧 Quick Start Implementation

### Step 1: Complete Configuration Modules

Run this implementation sequence for each config module:

```bash
# For each module (working_schedule, work_location, public_holiday, deduction_rule):

# 1. Create Response DTOs
# 2. Create Factory
# 3. Create Mapper
# 4. Create Repository
# 5. Create Read Model
# 6. Create Service
# 7. Create Routes
# 8. Register routes in __init__.py
# 9. Create Frontend API service
# 10. Create Frontend page
```

### Step 2: Test Configuration Modules

```bash
# Start backend
cd backend
docker-compose up

# Test endpoints
curl http://localhost:5001/api/hrms/admin/schedules
curl http://localhost:5001/api/hrms/admin/locations
curl http://localhost:5001/api/hrms/admin/holidays
curl http://localhost:5001/api/hrms/admin/deduction-rules
```

### Step 3: Implement Operational Modules

Follow the same pattern for Attendance and Overtime modules.

### Step 4: Implement Payroll

Build on attendance and overtime data for payroll calculations.

### Step 5: Add Reporting

Create read models and export functionality.

## 📋 Code Templates

### Response DTO Template

```python
# app/contexts/hrms/data_transfer/response/module_response.py
from pydantic import BaseModel
from datetime import datetime
from app.contexts.common.base_response_dto import LifecycleDTO

class ModuleDTO(BaseModel):
    id: str
    # ... module-specific fields ...
    lifecycle: LifecycleDTO
    
    class Config:
        from_attributes = True

class ModulePaginatedDTO(BaseModel):
    items: list[ModuleDTO]
    total: int
    page: int
    page_size: int
    total_pages: int
```

### Factory Template

```python
# app/contexts/hrms/factories/module_factory.py
from bson import ObjectId
from app.contexts.hrms.domain.module import Module
from app.contexts.shared.lifecycle.domain import Lifecycle

class ModuleFactory:
    @staticmethod
    def create(*, field1: str, field2: str, created_by: ObjectId) -> Module:
        return Module(
            id=ObjectId(),
            field1=field1,
            field2=field2,
            created_by=created_by,
            lifecycle=Lifecycle()
        )
    
    @staticmethod
    def from_dict(data: dict) -> Module:
        return Module(**data)
```

### Mapper Template

```python
# app/contexts/hrms/mapper/module_mapper.py
from app.contexts.hrms.domain.module import Module
from app.contexts.hrms.data_transfer.response.module_response import ModuleDTO
from app.contexts.shared.model_converter import to_pydantic

class ModuleMapper:
    @staticmethod
    def to_dto(domain: Module) -> ModuleDTO:
        return to_pydantic(ModuleDTO, domain)
    
    @staticmethod
    def to_dto_list(domains: list[Module]) -> list[ModuleDTO]:
        return [ModuleMapper.to_dto(d) for d in domains]
```

### Repository Template

```python
# app/contexts/hrms/repositories/module_repository.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.contexts.hrms.domain.module import Module
from app.contexts.hrms.factories.module_factory import ModuleFactory

class ModuleRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["modules"]
    
    async def save(self, module: Module) -> Module:
        doc = {
            "_id": module.id,
            "field1": module.field1,
            # ... all fields ...
            "lifecycle": {
                "created_at": module.lifecycle.created_at,
                "updated_at": module.lifecycle.updated_at,
                "deleted_at": module.lifecycle.deleted_at,
                "deleted_by": module.lifecycle.deleted_by,
            }
        }
        await self.collection.insert_one(doc)
        return module
    
    async def find_one(self, module_id: ObjectId) -> Module | None:
        doc = await self.collection.find_one({"_id": module_id})
        return ModuleFactory.from_dict(doc) if doc else None
    
    async def update(self, module: Module) -> Module:
        doc = {
            "field1": module.field1,
            # ... all fields ...
            "lifecycle.updated_at": module.lifecycle.updated_at,
        }
        await self.collection.update_one(
            {"_id": module.id},
            {"$set": doc}
        )
        return module
```

### Read Model Template

```python
# app/contexts/hrms/read_models/module_read_model.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.contexts.hrms.domain.module import Module
from app.contexts.hrms.factories.module_factory import ModuleFactory

class ModuleReadModel:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["modules"]
    
    async def get_by_id(self, module_id: ObjectId) -> Module | None:
        doc = await self.collection.find_one({"_id": module_id})
        return ModuleFactory.from_dict(doc) if doc else None
    
    async def get_page(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        q: str | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ) -> tuple[list[Module], int]:
        query = {}
        
        if q:
            query["$or"] = [
                {"field1": {"$regex": q, "$options": "i"}},
            ]
        
        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None
        
        skip = (page - 1) * limit
        cursor = self.collection.find(query).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        
        modules = [ModuleFactory.from_dict(doc) for doc in docs]
        return modules, total
```

### Service Template

```python
# app/contexts/hrms/services/module_service.py
from bson import ObjectId
from app.contexts.hrms.domain.module import Module
from app.contexts.hrms.repositories.module_repository import ModuleRepository
from app.contexts.hrms.read_models.module_read_model import ModuleReadModel
from app.contexts.hrms.factories.module_factory import ModuleFactory
from app.contexts.hrms.errors.module_exceptions import ModuleNotFoundException

class ModuleService:
    def __init__(
        self,
        repository: ModuleRepository,
        read_model: ModuleReadModel,
    ):
        self.repository = repository
        self.read_model = read_model
    
    async def create_module(
        self,
        *,
        field1: str,
        field2: str,
        actor_id: ObjectId,
    ) -> Module:
        module = ModuleFactory.create(
            field1=field1,
            field2=field2,
            created_by=actor_id,
        )
        return await self.repository.save(module)
    
    async def get_module(self, module_id: ObjectId) -> Module:
        module = await self.read_model.get_by_id(module_id)
        if not module:
            raise ModuleNotFoundException(str(module_id))
        return module
    
    async def list_modules(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        q: str | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ) -> tuple[list[Module], int]:
        return await self.read_model.get_page(
            page=page,
            limit=limit,
            q=q,
            include_deleted=include_deleted,
            deleted_only=deleted_only,
        )
    
    async def update_module(
        self,
        module_id: ObjectId,
        *,
        field1: str | None = None,
        field2: str | None = None,
    ) -> Module:
        module = await self.get_module(module_id)
        
        if field1 is not None:
            module.field1 = field1
        if field2 is not None:
            module.field2 = field2
        
        return await self.repository.update(module)
    
    async def soft_delete_module(
        self,
        module_id: ObjectId,
        actor_id: ObjectId,
    ) -> Module:
        module = await self.get_module(module_id)
        module.soft_delete(actor_id=actor_id)
        return await self.repository.update(module)
    
    async def restore_module(
        self,
        module_id: ObjectId,
    ) -> Module:
        module = await self.get_module(module_id)
        module.lifecycle.restore()
        return await self.repository.update(module)
```

### Routes Template

```python
# app/contexts/hrms/routes/module_route.py
from fastapi import APIRouter, Depends, Query
from bson import ObjectId
from app.contexts.hrms.services.module_service import ModuleService
from app.contexts.hrms.mapper.module_mapper import ModuleMapper
from app.contexts.hrms.data_transfer.request.module_request import (
    ModuleCreateSchema,
    ModuleUpdateSchema,
)
from app.contexts.hrms.data_transfer.response.module_response import (
    ModuleDTO,
    ModulePaginatedDTO,
)
from app.contexts.core.security.auth_utils import get_current_user_id

router = APIRouter(prefix="/api/hrms/admin/modules", tags=["HRMS - Modules"])

@router.get("", response_model=ModulePaginatedDTO)
async def list_modules(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = None,
    include_deleted: bool = False,
    deleted_only: bool = False,
    service: ModuleService = Depends(),
):
    modules, total = await service.list_modules(
        page=page,
        limit=limit,
        q=q,
        include_deleted=include_deleted,
        deleted_only=deleted_only,
    )
    
    return ModulePaginatedDTO(
        items=ModuleMapper.to_dto_list(modules),
        total=total,
        page=page,
        page_size=limit,
        total_pages=(total + limit - 1) // limit,
    )

@router.get("/{module_id}", response_model=ModuleDTO)
async def get_module(
    module_id: str,
    service: ModuleService = Depends(),
):
    module = await service.get_module(ObjectId(module_id))
    return ModuleMapper.to_dto(module)

@router.post("", response_model=ModuleDTO, status_code=201)
async def create_module(
    data: ModuleCreateSchema,
    actor_id: ObjectId = Depends(get_current_user_id),
    service: ModuleService = Depends(),
):
    module = await service.create_module(
        field1=data.field1,
        field2=data.field2,
        actor_id=actor_id,
    )
    return ModuleMapper.to_dto(module)

@router.patch("/{module_id}", response_model=ModuleDTO)
async def update_module(
    module_id: str,
    data: ModuleUpdateSchema,
    service: ModuleService = Depends(),
):
    module = await service.update_module(
        ObjectId(module_id),
        field1=data.field1,
        field2=data.field2,
    )
    return ModuleMapper.to_dto(module)

@router.delete("/{module_id}/soft-delete", response_model=ModuleDTO)
async def soft_delete_module(
    module_id: str,
    actor_id: ObjectId = Depends(get_current_user_id),
    service: ModuleService = Depends(),
):
    module = await service.soft_delete_module(
        ObjectId(module_id),
        actor_id=actor_id,
    )
    return ModuleMapper.to_dto(module)

@router.post("/{module_id}/restore", response_model=ModuleDTO)
async def restore_module(
    module_id: str,
    service: ModuleService = Depends(),
):
    module = await service.restore_module(ObjectId(module_id))
    return ModuleMapper.to_dto(module)
```

## 🚀 Next Steps

1. **Complete Configuration Modules** (2-3 hours)
   - Implement all layers for 4 config modules
   - Test CRUD operations
   - Create frontend pages

2. **Implement Attendance System** (2-3 hours)
   - Check-in/check-out functionality
   - Location validation
   - Late deduction calculation

3. **Implement Overtime Management** (2 hours)
   - OT request/approval workflow
   - Rate calculation
   - Integration with payroll

4. **Implement Payroll System** (3 hours)
   - Calculation engine
   - Payslip generation
   - Reports

5. **Add Analytics & Reports** (1-2 hours)
   - Daily/monthly reports
   - Export functionality

## 📊 Estimated Timeline

- **Phase 1 (Config)**: 2-3 hours
- **Phase 2 (Operations)**: 4-5 hours
- **Phase 3 (Payroll)**: 3 hours
- **Phase 4 (Reports)**: 1-2 hours

**Total**: 10-13 hours for complete implementation

## 🎯 Success Criteria

- [ ] All 49 endpoints functional
- [ ] All modules follow DDD architecture
- [ ] Frontend pages for all modules
- [ ] Role-based access control
- [ ] Soft delete and lifecycle management
- [ ] Pagination and filtering
- [ ] Error handling and validation
- [ ] Integration tests passing

---

**Ready to implement! Start with Phase 1: Configuration Modules**

