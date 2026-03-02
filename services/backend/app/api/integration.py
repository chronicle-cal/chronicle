from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.core.crud import CRUDBase
from app.models.integration import (
    SyncConfig,
    Source,
    Rule,
    Condition,
    Action,
    SchedulerConfig,
    Task,
)
from app.schemas.integration import (
    SyncConfig as SyncConfigSchema,
    SyncConfigCreate,
    SchedulerConfig as SchedulerConfigSchema,
    SchedulerConfigCreate,
    Source as SourceSchema,
    SourceCreate,
    Rule as RuleSchema,
    RuleCreate,
    Condition as ConditionSchema,
    ConditionCreate,
    Action as ActionSchema,
    ActionCreate,
    Task as TaskSchema,
    TaskCreate,
)

sync_config_router = APIRouter()
scheduler_config_router = APIRouter()
source_router = APIRouter()
rule_router = APIRouter()
condition_router = APIRouter()
action_router = APIRouter()
task_router = APIRouter()

sync_config_crud = CRUDBase(SyncConfig)
scheduler_config_crud = CRUDBase(SchedulerConfig)
source_crud = CRUDBase(Source)
rule_crud = CRUDBase(Rule)
condition_crud = CRUDBase(Condition)
action_crud = CRUDBase(Action)
task_crud = CRUDBase(Task)


@sync_config_router.get("", response_model=list[SyncConfigSchema])
async def list_sync_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await sync_config_crud.get_multi(db, skip=skip, limit=limit)


@sync_config_router.get("/{id}", response_model=SyncConfigSchema)
async def get_sync_config(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SyncConfig).where(SyncConfig.id == id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")
    return item


@sync_config_router.post(
    "", response_model=SyncConfigSchema, status_code=status.HTTP_201_CREATED
)
async def create_sync_config(
    payload: SyncConfigCreate, db: AsyncSession = Depends(get_db)
):
    return await sync_config_crud.create(db, payload)


@sync_config_router.put("/{id}", response_model=SyncConfigSchema)
async def update_sync_config(
    id: str, payload: dict, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(SyncConfig).where(SyncConfig.id == id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field):
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@sync_config_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sync_config(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SyncConfig).where(SyncConfig.id == id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")
    await db.delete(item)
    await db.commit()


@scheduler_config_router.get("", response_model=list[SchedulerConfigSchema])
async def list_scheduler_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await scheduler_config_crud.get_multi(db, skip=skip, limit=limit)


@scheduler_config_router.get("/{id}", response_model=SchedulerConfigSchema)
async def get_scheduler_config(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SchedulerConfig).where(SchedulerConfig.id == id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")
    return item


@scheduler_config_router.post(
    "", response_model=SchedulerConfigSchema, status_code=status.HTTP_201_CREATED
)
async def create_scheduler_config(
    payload: SchedulerConfigCreate, db: AsyncSession = Depends(get_db)
):
    return await scheduler_config_crud.create(db, payload)


@scheduler_config_router.put("/{id}", response_model=SchedulerConfigSchema)
async def update_scheduler_config(
    id: str, payload: dict, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(SchedulerConfig).where(SchedulerConfig.id == id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field):
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@scheduler_config_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduler_config(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SchedulerConfig).where(SchedulerConfig.id == id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")
    await db.delete(item)
    await db.commit()


@source_router.get("/sync-config/{sync_config_id}", response_model=list[SourceSchema])
async def list_sources_for_sync_config(
    sync_config_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Source).where(Source.sync_config_id == sync_config_id)
    )
    return list(result.scalars().all())


@source_router.post(
    "/sync-config/{sync_config_id}",
    response_model=SourceSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_source_for_sync_config(
    sync_config_id: str,
    payload: SourceCreate,
    db: AsyncSession = Depends(get_db),
):
    parent = await db.get(SyncConfig, sync_config_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")

    data = payload.model_dump()
    data["sync_config_id"] = sync_config_id
    return await source_crud.create(db, data)


@source_router.get("/{id}", response_model=SourceSchema)
async def get_source(id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Source, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return item


@source_router.put("/{id}", response_model=SourceSchema)
async def update_source(id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    item = await db.get(Source, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Source not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field):
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@source_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Source, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Source not found")
    await db.delete(item)
    await db.commit()


@rule_router.get("/source/{source_id}", response_model=list[RuleSchema])
async def list_rules_for_source(
    source_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Rule).where(Rule.source_id == source_id))
    return list(result.scalars().all())


@rule_router.post(
    "/source/{source_id}",
    response_model=RuleSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_rule_for_source(
    source_id: str,
    payload: RuleCreate,
    db: AsyncSession = Depends(get_db),
):
    parent = await db.get(Source, source_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Source not found")

    data = payload.model_dump()
    data["source_id"] = source_id
    return await rule_crud.create(db, data)


@rule_router.get("/{id}", response_model=RuleSchema)
async def get_rule(id: int, db: AsyncSession = Depends(get_db)):
    item = await rule_crud.get(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return item


@rule_router.put("/{id}", response_model=RuleSchema)
async def update_rule(id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    item = await rule_crud.update(db, id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return item


@rule_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(id: int, db: AsyncSession = Depends(get_db)):
    item = await rule_crud.get(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    await rule_crud.delete(db, id)


@condition_router.get("/rule/{rule_id}", response_model=list[ConditionSchema])
async def list_conditions_for_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Condition).where(Condition.rule_id == rule_id))
    return list(result.scalars().all())


@condition_router.post(
    "/rule/{rule_id}",
    response_model=ConditionSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_condition_for_rule(
    rule_id: int,
    payload: ConditionCreate,
    db: AsyncSession = Depends(get_db),
):
    parent = await db.get(Rule, rule_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    data = payload.model_dump()
    data["rule_id"] = rule_id
    return await condition_crud.create(db, data)


@condition_router.get("/{id}", response_model=ConditionSchema)
async def get_condition(id: int, db: AsyncSession = Depends(get_db)):
    item = await condition_crud.get(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    return item


@condition_router.put("/{id}", response_model=ConditionSchema)
async def update_condition(id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    item = await condition_crud.update(db, id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    return item


@condition_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_condition(id: int, db: AsyncSession = Depends(get_db)):
    item = await condition_crud.get(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    await condition_crud.delete(db, id)


@action_router.get("/rule/{rule_id}", response_model=list[ActionSchema])
async def list_actions_for_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Action).where(Action.rule_id == rule_id))
    return list(result.scalars().all())


@action_router.post(
    "/rule/{rule_id}", response_model=ActionSchema, status_code=status.HTTP_201_CREATED
)
async def create_action_for_rule(
    rule_id: int,
    payload: ActionCreate,
    db: AsyncSession = Depends(get_db),
):
    parent = await db.get(Rule, rule_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    data = payload.model_dump()
    data["rule_id"] = rule_id
    return await action_crud.create(db, data)


@action_router.get("/{id}", response_model=ActionSchema)
async def get_action(id: int, db: AsyncSession = Depends(get_db)):
    item = await action_crud.get(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return item


@action_router.put("/{id}", response_model=ActionSchema)
async def update_action(id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    item = await action_crud.update(db, id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return item


@action_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action(id: int, db: AsyncSession = Depends(get_db)):
    item = await action_crud.get(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")
    await action_crud.delete(db, id)


@task_router.get(
    "/scheduler-config/{scheduler_config_id}", response_model=list[TaskSchema]
)
async def list_tasks_for_scheduler_config(
    scheduler_config_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task).where(Task.scheduler_config_id == scheduler_config_id)
    )
    return list(result.scalars().all())


@task_router.post(
    "/scheduler-config/{scheduler_config_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_for_scheduler_config(
    scheduler_config_id: str,
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    parent = await db.get(SchedulerConfig, scheduler_config_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")

    data = payload.model_dump()
    data["scheduler_config_id"] = scheduler_config_id
    return await task_crud.create(db, data)


@task_router.get("/{id}", response_model=TaskSchema)
async def get_task(id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Task, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return item


@task_router.put("/{id}", response_model=TaskSchema)
async def update_task(id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    item = await db.get(Task, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Task not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field):
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Task, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(item)
    await db.commit()
