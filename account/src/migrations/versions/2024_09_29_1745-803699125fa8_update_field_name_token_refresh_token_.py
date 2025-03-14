"""update field name token > refresh_token in session table

Revision ID: 803699125fa8
Revises: 91b04c13388b
Create Date: 2024-09-29 17:45:16.039442

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "803699125fa8"
down_revision: Union[str, None] = "91b04c13388b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sessions", sa.Column("refresh_token", sa.String(), nullable=False)
    )
    op.drop_column("sessions", "token")
    op.drop_column("sessions", "expires_at")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sessions",
        sa.Column(
            "expires_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "sessions",
        sa.Column(
            "token",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("sessions", "refresh_token")
    # ### end Alembic commands ###
