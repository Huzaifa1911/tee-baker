from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
