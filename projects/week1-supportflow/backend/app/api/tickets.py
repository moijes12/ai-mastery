from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..core.database import get_session
from ..models.ticket import Ticket, TicketCreate, TicketRead

router = APIRouter()


@router.post("/tickets/", response_model=TicketRead)
async def create_ticket(
    ticket: TicketCreate, session: AsyncSession = Depends(get_session)
):
    db_ticket = Ticket.model_validate(ticket)
    session.add(db_ticket)
    await session.commit()
    await session.refresh(db_ticket)
    return db_ticket


@router.get("/tickets/", response_model=list[TicketRead])
async def list_tickets(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Ticket))
    return result.scalars().all()


@router.get("/tickets/{ticket_id}", response_model=TicketRead)
async def get_ticket(ticket_id: int, session: AsyncSession = Depends(get_session)):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
