"""SSO logins table

Revision ID: a1458daa8288
Revises: 6e251914c21b
Create Date: 2018-03-23 17:49:10.602045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1458daa8288'
down_revision = '6e251914c21b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sso_logins',
        sa.Column('id', sa.BigInteger(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('sso_id', sa.String(), nullable=False),
        sa.Column('sso_type', sa.String(), nullable=False),
    )

    op.execute('alter table sso_logins alter column created_at set default current_timestamp;')
    op.execute('alter table sso_logins alter column updated_at set default current_timestamp;')

    op.execute(
        'CREATE UNIQUE INDEX sso_logins_user_id_sso_type_idx ON sso_logins(user_id, sso_type) WHERE deleted_at IS NULL;'
    )
    op.execute(
        'CREATE UNIQUE INDEX sso_logins_sso_id_sso_type_idx ON sso_logins(sso_id, sso_type) WHERE deleted_at IS NULL;'
    )
    op.execute(
        'CREATE TRIGGER sso_logins_updated_at BEFORE UPDATE ON sso_logins FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();'
    )


def downgrade():
    pass
