"""
BaseModel — generische Basisklasse für alle Modelle im MVC-Framework.

Verantwortlichkeiten:
  - Datenhaltung und Geschäftslogik
  - Benachrichtigung von Beobachtern über pyqtSignal (Observer-Pattern)
"""

from abc import abstractmethod
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal


class BaseModel(QObject):
    """
    Abstrakte Basisklasse für Modelle.

    Signale
    -------
    data_changed(key, value)
        Wird ausgelöst, wenn sich ein einzelnes Datum ändert.
        key  – symbolischer Name des geänderten Feldes
        value – neuer Wert (beliebiger Typ)

    data_reset()
        Wird ausgelöst, wenn der gesamte Zustand neu gesetzt wird
        (z. B. nach einem Laden aus der Datenquelle).

    error_occurred(message)
        Wird ausgelöst, wenn ein Fehler in der Geschäftslogik auftritt.
    """

    data_changed: pyqtSignal = pyqtSignal(str, object)
    data_reset: pyqtSignal = pyqtSignal()
    error_occurred: pyqtSignal = pyqtSignal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    # ------------------------------------------------------------------
    # Interne Hilfsmethode – setzt ein Feld und feuert data_changed
    # ------------------------------------------------------------------

    def _set_field(self, key: str, value: Any) -> None:
        """Setzt self.<key> = value und emittiert data_changed."""
        setattr(self, key, value)
        self.data_changed.emit(key, value)

    # ------------------------------------------------------------------
    # Abstrakte Schnittstelle – von konkreten Modellen zu implementieren
    # ------------------------------------------------------------------

    @abstractmethod
    def load(self) -> None:
        """Daten aus der Quelle laden und data_reset emittieren."""

    @abstractmethod
    def save(self) -> None:
        """Aktuellen Zustand persistieren."""
