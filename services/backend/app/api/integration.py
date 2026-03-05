from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.auth import get_current_user
from app.core.db import get_db
from app.models.integration import (
    SyncConfig,
    Source,
    Rule,
    Condition,
    Action,
    SchedulerConfig,
    Task,
)
from app.models.user import User
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


@sync_config_router.get("", response_model=list[SyncConfigSchema])
async def list_sync_configs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SyncConfig).where(SyncConfig.user_id == current_user.id)
    )
    return list(result.scalars().all())


@sync_config_router.get("/{id}", response_model=SyncConfigSchema)
async def get_sync_config(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SyncConfig).where(
            SyncConfig.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")
    return item


@sync_config_router.post(
    "", response_model=SyncConfigSchema, status_code=status.HTTP_201_CREATED
)
async def create_sync_config(
    payload: SyncConfigCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    data = payload.model_dump()
    data["user_id"] = current_user.id

    db_obj = SyncConfig(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@sync_config_router.put("/{id}", response_model=SyncConfigSchema)
async def update_sync_config(
    id: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SyncConfig).where(
            SyncConfig.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "user_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@sync_config_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sync_config(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SyncConfig).where(
            SyncConfig.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")
    await db.delete(item)
    await db.commit()


@scheduler_config_router.get("", response_model=list[SchedulerConfigSchema])
async def list_scheduler_configs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SchedulerConfig).where(SchedulerConfig.user_id == current_user.id)
    )
    return list(result.scalars().all())


@scheduler_config_router.get("/{id}", response_model=SchedulerConfigSchema)
async def get_scheduler_config(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SchedulerConfig).where(
            SchedulerConfig.id == id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")
    return item


@scheduler_config_router.post(
    "", response_model=SchedulerConfigSchema, status_code=status.HTTP_201_CREATED
)
async def create_scheduler_config(
    payload: SchedulerConfigCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    data = payload.model_dump()
    data["user_id"] = current_user.id

    db_obj = SchedulerConfig(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@scheduler_config_router.put("/{id}", response_model=SchedulerConfigSchema)
async def update_scheduler_config(
    id: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SchedulerConfig).where(
            SchedulerConfig.id == id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "user_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@scheduler_config_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduler_config(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SchedulerConfig).where(
            SchedulerConfig.id == id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")
    await db.delete(item)
    await db.commit()


@source_router.get("/sync-config/{sync_config_id}", response_model=list[SourceSchema])
async def list_sources_for_sync_config(
    sync_config_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Source)
        .join(SyncConfig)
        .where(
            Source.sync_config_id == sync_config_id,
            SyncConfig.user_id == current_user.id,
        )
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    parent_result = await db.execute(
        select(SyncConfig).where(
            SyncConfig.id == sync_config_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    parent = parent_result.scalar_one_or_none()
    if parent is None:
        raise HTTPException(status_code=404, detail="SyncConfig not found")

    data = payload.model_dump()
    data["sync_config_id"] = sync_config_id
    db_obj = Source(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@source_router.get("/{id}", response_model=SourceSchema)
async def get_source(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Source)
        .join(SyncConfig)
        .where(
            Source.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return item


@source_router.put("/{id}", response_model=SourceSchema)
async def update_source(
    id: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Source)
        .join(SyncConfig)
        .where(
            Source.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Source not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "sync_config_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@source_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Source)
        .join(SyncConfig)
        .where(
            Source.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Source not found")
    await db.delete(item)
    await db.commit()


@rule_router.get("/source/{source_id}", response_model=list[RuleSchema])
async def list_rules_for_source(
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Rule.source_id == source_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    return list(result.scalars().all())


@rule_router.post(
    "/source/{source_id}",
    response_model=RuleSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_rule_for_source(
    source_id: str,
    payload: RuleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    parent_result = await db.execute(
        select(Source)
        .join(SyncConfig)
        .where(
            Source.id == source_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    parent = parent_result.scalar_one_or_none()
    if parent is None:
        raise HTTPException(status_code=404, detail="Source not found")

    data = payload.model_dump()
    data["source_id"] = source_id
    db_obj = Rule(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@rule_router.get("/{id}", response_model=RuleSchema)
async def get_rule(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Rule.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return item


@rule_router.put("/{id}", response_model=RuleSchema)
async def update_rule(
    id: int,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Rule.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "source_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@rule_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Rule.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    await db.delete(item)
    await db.commit()


@condition_router.get("/rule/{rule_id}", response_model=list[ConditionSchema])
async def list_conditions_for_rule(
    rule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Condition)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Condition.rule_id == rule_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    return list(result.scalars().all())


@condition_router.post(
    "/rule/{rule_id}",
    response_model=ConditionSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_condition_for_rule(
    rule_id: int,
    payload: ConditionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    parent_result = await db.execute(
        select(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Rule.id == rule_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    parent = parent_result.scalar_one_or_none()
    if parent is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    data = payload.model_dump()
    data["rule_id"] = rule_id
    db_obj = Condition(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@condition_router.get("/{id}", response_model=ConditionSchema)
async def get_condition(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Condition)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Condition.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    return item


@condition_router.put("/{id}", response_model=ConditionSchema)
async def update_condition(
    id: int,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Condition)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Condition.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Condition not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "rule_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@condition_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_condition(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Condition)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Condition.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    await db.delete(item)
    await db.commit()


@action_router.get("/rule/{rule_id}", response_model=list[ActionSchema])
async def list_actions_for_rule(
    rule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Action)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Action.rule_id == rule_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    return list(result.scalars().all())


@action_router.post(
    "/rule/{rule_id}",
    response_model=ActionSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_action_for_rule(
    rule_id: int,
    payload: ActionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    parent_result = await db.execute(
        select(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Rule.id == rule_id,
            SyncConfig.user_id == current_user.id,
        )
    )
    parent = parent_result.scalar_one_or_none()
    if parent is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    data = payload.model_dump()
    data["rule_id"] = rule_id
    db_obj = Action(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@action_router.get("/{id}", response_model=ActionSchema)
async def get_action(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Action)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Action.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return item


@action_router.put("/{id}", response_model=ActionSchema)
async def update_action(
    id: int,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Action)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Action.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "rule_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@action_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Action)
        .join(Rule)
        .join(Source)
        .join(SyncConfig)
        .where(
            Action.id == id,
            SyncConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")
    await db.delete(item)
    await db.commit()


@task_router.get(
    "/scheduler-config/{scheduler_config_id}", response_model=list[TaskSchema]
)
async def list_tasks_for_scheduler_config(
    scheduler_config_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task)
        .join(SchedulerConfig)
        .where(
            Task.scheduler_config_id == scheduler_config_id,
            SchedulerConfig.user_id == current_user.id,
        )
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    parent_result = await db.execute(
        select(SchedulerConfig).where(
            SchedulerConfig.id == scheduler_config_id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    parent = parent_result.scalar_one_or_none()
    if parent is None:
        raise HTTPException(status_code=404, detail="SchedulerConfig not found")

    data = payload.model_dump()
    data["scheduler_config_id"] = scheduler_config_id
    db_obj = Task(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@task_router.get("/{id}", response_model=TaskSchema)
async def get_task(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task)
        .join(SchedulerConfig)
        .where(
            Task.id == id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return item


@task_router.put("/{id}", response_model=TaskSchema)
async def update_task(
    id: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task)
        .join(SchedulerConfig)
        .where(
            Task.id == id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Task not found")

    obj_data = payload
    for field, value in obj_data.items():
        if hasattr(item, field) and field != "scheduler_config_id":
            setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task)
        .join(SchedulerConfig)
        .where(
            Task.id == id,
            SchedulerConfig.user_id == current_user.id,
        )
    )
    item = result.unique().scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(item)
    await db.commit()
