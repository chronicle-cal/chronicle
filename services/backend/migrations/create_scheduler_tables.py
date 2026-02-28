from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.create_table(
        "sync_configs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("destination", sa.String(255), nullable=False),
        sa.Column("username", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
    )

    op.create_table(
        "scheduler_configs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("calendar_url", sa.String(2048), nullable=False),
        sa.Column("calendar_password", sa.String(255), nullable=False),
        sa.Column("calendar_username", sa.String(255), nullable=False),
    )

    op.create_table(
        "sources",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "sync_config_id",
            sa.String(64),
            sa.ForeignKey("sync_configs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("url", sa.String(2048), nullable=False),
    )

    op.create_table(
        "rules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "source_id",
            sa.String(64),
            sa.ForeignKey("sources.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("name", sa.String(255), nullable=False),
    )

    op.create_table(
        "conditions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "rule_id",
            sa.Integer(),
            sa.ForeignKey("rules.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("field", sa.String(255), nullable=False),
        sa.Column("operator", sa.String(64), nullable=False),
        sa.Column("value", sa.String(2048), nullable=False),
    )

    op.create_table(
        "actions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "rule_id",
            sa.Integer(),
            sa.ForeignKey("rules.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("field", sa.JSON(), nullable=False),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "scheduler_config_id",
            sa.String(64),
            sa.ForeignKey("scheduler_configs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.String(4096), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "duration", sa.Integer(), nullable=False, server_default=sa.text("30")
        ),
        sa.Column("not_before", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "priority", sa.Integer(), nullable=False, server_default=sa.text("3")
        ),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("actions")
    op.drop_table("conditions")
    op.drop_table("rules")
    op.drop_table("sources")
    op.drop_table("scheduler_configs")
    op.drop_table("sync_configs")
