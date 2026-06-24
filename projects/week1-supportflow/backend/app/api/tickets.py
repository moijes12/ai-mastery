from app.core.database import get_session
from app.models.ticket import Ticket, TicketCreate, TicketRead
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.services import ml_service
from loguru import logger

router = APIRouter()


@router.post("/tickets/", response_model=TicketRead)
async def create_ticket(
    ticket: TicketCreate, session: AsyncSession = Depends(get_session)
):
    # Get ML predictions
    prediction = await ml_service.predict_ticket(ticket.subject, ticket.description)

    # Enrich ticket with predictions
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

    logger.info(
        f"Created ticket {db_ticket.id} with predicted category: {db_ticket.category}"
    )
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


# New endpoint for quick prediction without saving
@router.post("/predict/")
async def predict_only(subject: str, description: str):
    prediction = await ml_service.predict_ticket(subject, description)
    return prediction
