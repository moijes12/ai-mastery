from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TicketBase(SQLModel):
    subject: str = Field(max_length=500)
    description: str = Field(max_length=4000)
    category: Optional[str] = Field(default=None, max_length=100)
    urgency: Optional[str] = Field(default=None, max_length=50)
    predicted_resolution_time_hours: Optional[float] = None
    priority_score: Optional[float] = None


class Ticket(TicketBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TicketCreate(TicketBase):
    pass


class TicketRead(TicketBase):
    id: int
    created_at: datetime
