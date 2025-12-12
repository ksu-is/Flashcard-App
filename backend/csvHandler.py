import csv
from datetime import datetime
from typing import List

from .flashcard import Flashcard


def loadFlashcards(filename: str) -> List[Flashcard]:
    """
    Load flashcards from a CSV file with headers:
    Front,Back,Box,NextReviewDate (YYYY-MM-DD)
    """
    flashcards: List[Flashcard] = []
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    nr = datetime.strptime(row["NextReviewDate"], "%Y-%m-%d").date()
                except Exception:
                    nr = None
                flashcards.append(
                    Flashcard(
                        front=row.get("Front", ""),
                        back=row.get("Back", ""),
                        box=int(row.get("Box", "1") or 1),
                        nextReviewDate=nr,
                    )
                )
    except FileNotFoundError:
        # If file doesn't exist, return empty list
        return []
    return flashcards


def saveFlashcards(flashcards: List[Flashcard], filename: str) -> None:
    """Save flashcards to CSV file (overwrites)."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Front", "Back", "Box", "NextReviewDate"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in flashcards:
            writer.writerow(
                {
                    "Front": c.front,
                    "Back": c.back,
                    "Box": c.box,
                    "NextReviewDate": c.nextReviewDate.strftime("%Y-%m-%d"),
                }
            )