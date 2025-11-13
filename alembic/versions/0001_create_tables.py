"""Create users, projects, tasks tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2025-11-13 17:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '0001_create_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=50)),
        sa.Column('last_name', sa.String(length=50)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('assignee_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade():
    op.drop_table('tasks')
    op.drop_table('projects')
    op.drop_table('users')
