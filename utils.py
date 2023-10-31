from datetime import datetime

import sqlalchemy as sa

class Timestamp(object):
    created = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
