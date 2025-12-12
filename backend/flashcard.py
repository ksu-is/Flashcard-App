from datetime import datetime, timedelta, date
from typing import Optional


class Flashcard:
    """
    Simple Flashcard object used by the frontend and session provider.
    Stores front/back text, a Leitner-style box number, and a nextReviewDate.
    """

    def __init__(
        self,
        front: str,
        back: str,
        box: int = 1,
        nextReviewDate: Optional[date] = None,
    ) -> None:
        self.front = front
        self.back = back
        self.box = box
        self.nextReviewDate: date = nextReviewDate or datetime.now().date()

    def promote(self) -> None:
        """Promote card to next box (max 3) and update next review date."""
        if self.box < 3:
            self.box += 1
        self.updateNextReviewDate()

    def demote(self) -> None:
        """Demote card to previous box (min 1) and update next review date."""
        if self.box > 1:
            self.box -= 1
        self.updateNextReviewDate()

    def updateNextReviewDate(self) -> None:
        """Set the next review date depending on the box."""
        intervals = {1: 1, 2: 3, 3: 5}  # days until next review for each box
        days = intervals.get(self.box, 1)
        self.nextReviewDate = datetime.now().date() + timedelta(days=days)

    def __repr__(self) -> str:
        return (
            f"Flashcard(front={self.front!r}, back={self.back!r}, "
            f"box={self.box}, nextReviewDate={self.nextReviewDate})"
        )