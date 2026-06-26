from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..core.database import get_session
from ..models.ticket import Ticket, TicketCreate, TicketRead
from ..services.ml_service import ml_service

router = APIRouter()


@router.post("/tickets/", response_model=TicketRead)
async def create_ticket(
    ticket: TicketCreate, session: AsyncSession = Depends(get_session)
):
    prediction = await ml_service.predict(ticket.subject, ticket.description)

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

    logger.success(f"Ticket #{db_ticket.id} created | Category: {db_ticket.category}")
    return db_ticket


@router.post("/predict/")
async def quick_predict(subject: str, description: str):
    return await ml_service.predict(subject, description)


@router.get("/tickets/")
async def list_tickets(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Ticket))
    return result.scalars().all()
