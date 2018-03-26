"""Users table

Revision ID: c72ec260b330
Revises: 
Create Date: 2018-03-16 17:59:17.592238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c72ec260b330'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$ language 'plpgsql';")
    
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )

    op.execute('alter table users alter column created_at set default current_timestamp;')
    op.execute('alter table users alter column updated_at set default current_timestamp;')

    op.execute(
        'CREATE TRIGGER users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();'
    )


def downgrade():
    op.drop_table('users')
