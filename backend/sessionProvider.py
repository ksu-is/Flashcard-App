import random
from collections import deque
from datetime import datetime
from typing import Deque, Dict, Iterable, List, Optional

from .flashcard import Flashcard


class SessionProvider:
    """
    Provides a review session generator for a list of Flashcard objects.
    Uses a simple attempt tracker to handle 'see again' and promotion/demotion.
    """

    def __init__(self, flashcards: Optional[List[Flashcard]] = None) -> None:
        self.flashcards: List[Flashcard] = flashcards or []
        self.reviewQueue: Deque[Flashcard] = deque(self.getCardsForReview())
        self.attemptTracker: Dict[Flashcard, int] = {}

    def getCardsForReview(self) -> List[Flashcard]:
        # select cards due today or earlier
        today = datetime.now().date()
        cards = [c for c in self.flashcards if c.nextReviewDate <= today]
        random.shuffle(cards)
        return cards

    def startSession(self) -> Iterable[Flashcard]:
        """Generator that yields cards for a review session."""
        while self.reviewQueue:
            card = self.reviewQueue.popleft()
            self.attemptTracker[card] = self.attemptTracker.get(card, 0) + 1
            yield card

    def processResponse(self, card: Flashcard, response: str) -> None:
        """Process user's response: 'right' or 'wrong'."""
        first_attempt = self.attemptTracker.get(card, 0) == 1

        if response == "right":
            if first_attempt:
                card.promote()
            else:
                card.updateNextReviewDate()
            self.attemptTracker.pop(card, None)

        elif response == "wrong":
            if first_attempt:
                # see the card again this session
                self.reviewQueue.append(card)
                self.attemptTracker[card] = 2
            else:
                # missed twice: demote and stop tracking
                card.demote()
                self.attemptTracker.pop(card, None)
                if card in self.reviewQueue:
                    try:
                        self.reviewQueue.remove(card)
                    except ValueError:
                        pass

    def endSession(self) -> None:
        self.attemptTracker.clear()
        # optionally update nextReviewDates or persist externally