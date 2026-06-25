from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..core.database import get_session
from ..models.ticket import Ticket, TicketCreate, TicketRead
from ..services.ml_service import ml_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketRead)
async def create_ticket(
    ticket: TicketCreate, session: AsyncSession = Depends(get_session)
):
    """Create ticket with AI predictions"""
    # Get ML predictions
    prediction = await ml_service.predict(ticket.subject, ticket.description)

    # Enrich the ticket
    db_ticket = Ticket.model_validate(ticket)
    db_ticket.category = prediction["category"]
    db_ticket.urgency = prediction["urgency"]
    db_ticket.predicted_resolution_time_hours = prediction[
        "predicted_resolution_time_hours"
    ]
    db_ticket.priority_score = prediction["priority_score"]

    session.add(db_ticket)
    await session.commit()
    await session.refresh(db_ticket)

    logger.success(
        f"Ticket #{db_ticket.id} created with AI category: {db_ticket.category}"
    )
    return db_ticket


@router.get("/", response_model=list[TicketRead])
async def list_tickets(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Ticket))
    return result.scalars().all()


@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(ticket_id: int, session: AsyncSession = Depends(get_session)):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# Bonus: Quick prediction without saving
@router.post("/predict/")
async def quick_predict(subject: str, description: str):
    prediction = await ml_service.predict(subject, description)
    return prediction
