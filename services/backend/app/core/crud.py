from typing import Any, Dict, Generic, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        return await db.get(self.model, id)

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_all(self, db: AsyncSession) -> list[ModelType]:
        result = await db.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump() if isinstance(obj_in, BaseModel) else obj_in
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        id: int,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType | None:
        db_obj = await self.get(db, id)
        if db_obj is None:
            return None

        obj_data = obj_in.model_dump() if isinstance(obj_in, BaseModel) else obj_in
        for field, value in obj_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        db_obj = await self.get(db, id)
        if db_obj is None:
            return False
        await db.delete(db_obj)
        await db.commit()
        return True

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count(self.model.id)))
        return result.scalar_one()
