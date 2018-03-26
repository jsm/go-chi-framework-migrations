"""Email Logins table

Revision ID: 6e251914c21b
Revises: c72ec260b330
Create Date: 2018-03-16 18:10:54.646290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e251914c21b'
down_revision = 'c72ec260b330'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'email_logins',
        sa.Column('id', sa.BigInteger(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
    )

    op.execute('alter table email_logins alter column created_at set default current_timestamp;')
    op.execute('alter table email_logins alter column updated_at set default current_timestamp;')

    op.execute(
        'CREATE UNIQUE INDEX remail_logins_email_idx ON email_logins(email) WHERE deleted_at IS NULL;'
    )
    op.execute(
        'CREATE TRIGGER email_logins_updated_at BEFORE UPDATE ON email_logins FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();'
    )


def downgrade():
    op.drop_table('email_logins')
