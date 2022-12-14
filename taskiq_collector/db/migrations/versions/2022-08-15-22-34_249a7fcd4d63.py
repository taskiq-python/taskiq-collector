"""Created task model

Revision ID: 249a7fcd4d63
Revises:
Create Date: 2022-08-15 22:34:35.785627

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "249a7fcd4d63"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "taskiq_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), nullable=True),
        sa.Column("task_id", sa.String(length=100), nullable=False),
        sa.Column("task_name", sa.String(length=250), nullable=False),
        sa.Column("labels", sa.JSON(), nullable=False),
        sa.Column("args", sa.JSON(), nullable=False),
        sa.Column("kwargs", sa.JSON(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.Column("is_err", sa.Boolean(), nullable=True),
        sa.Column("log", sa.Text(), nullable=True),
        sa.Column("return_value", sa.Text(), nullable=True),
        sa.Column("execution_time", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_taskiq_tasks_task_id"),
        "taskiq_tasks",
        ["task_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_taskiq_tasks_task_name"),
        "taskiq_tasks",
        ["task_name"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_taskiq_tasks_task_name"), table_name="taskiq_tasks")
    op.drop_index(op.f("ix_taskiq_tasks_task_id"), table_name="taskiq_tasks")
    op.drop_table("taskiq_tasks")
    # ### end Alembic commands ###
