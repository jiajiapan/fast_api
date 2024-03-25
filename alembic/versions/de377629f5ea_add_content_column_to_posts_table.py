"""add content column to posts table

Revision ID: de377629f5ea
Revises: d56d44c8e806
Create Date: 2024-03-24 13:13:09.890291

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de377629f5ea"
down_revision: Union[str, None] = "d56d44c8e806"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
