"""
BaseScene — generische Basisklasse für alle Szenen im MVC-Framework.

Verantwortlichkeiten:
  - Verwaltung der grafischen Szenenobjekte (QGraphicsItem)
  - Bereitstellung einer abstrakten Schnittstelle für konkrete Szenen
"""

from abc import abstractmethod

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsScene

_DEFAULT_SCENE_RECT = QRectF(-5000, -5000, 10000, 10000)


class BaseScene(QGraphicsScene):
    """
    Abstrakte Basisklasse für Szenen.

    Konkrete Szenen implementieren setup_scene(), um Szenenobjekte
    initial zu erzeugen, sowie on_reset() für vollständige Neu-Initialisierungen.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(_DEFAULT_SCENE_RECT, parent)
        self.setup_scene()

    # ------------------------------------------------------------------
    # Abstrakte Schnittstelle – von konkreten Szenen zu implementieren
    # ------------------------------------------------------------------

    @abstractmethod
    def setup_scene(self) -> None:
        """Szenenobjekte erzeugen und initial positionieren."""

    @abstractmethod
    def on_reset(self) -> None:
        """Szene vollständig zurücksetzen (z. B. nach data_reset des Modells)."""
