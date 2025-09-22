from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '20250922_0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('firstname', sa.String(length=20), nullable=False),
        sa.Column('lastname', sa.String(length=20), nullable=False),
        sa.Column('date_of_birth', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('users')
