from datetime import datetime
from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Reservation, User
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(
    CRUDBase[Reservation, ReservationCreate, ReservationUpdate]
):

    @staticmethod
    async def get_future_reservations_for_room(
        room_id: int,
        session: AsyncSession
    ) -> list[Reservation]:

        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        return reservations.scalars().all()

    @staticmethod
    async def get_reservations_at_the_same_time(
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        return reservations.scalars().all()

    @staticmethod
    async def get_by_user(
        user: User,
        session: AsyncSession
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(Reservation.user_id == user.id)
        )
        return reservations.scalars().all()

    @staticmethod
    async def get_count_res_at_the_same_time(
        from_reserve: datetime,
        to_reserve: datetime,
        session: AsyncSession
    ) -> list[dict[str, int]]:
        reservations = await session.execute(
            select(
                [
                    Reservation.meetingroom_id,
                    func.count(Reservation.meetingroom_id)
                ]
            ).where(
                Reservation.from_reserve >= from_reserve,
                Reservation.to_reserve <= to_reserve
            ).group_by(Reservation.meetingroom_id)
        )
        return reservations.all()


reservation_crud = CRUDReservation(Reservation)
