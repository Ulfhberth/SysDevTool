"""
BaseToolbox — statische Seitenleiste links neben dem BaseCanvas.

Verantwortlichkeiten:
  - Darstellung von Werkzeugen / Steuerelementen als QGraphicsScene
  - Kein Zoom, kein Pan — rein statische Anzeige
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QWheelEvent
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QSizePolicy

_DEFAULT_WIDTH = 220


class BaseToolbox(QGraphicsView):
    """
    Statischer Toolbox-Canvas für die linke Seitenleiste.

    Nicht navigierbar, nicht zoombar. Konkrete Toolboxen befüllen
    eine eigene QGraphicsScene und übergeben sie im Konstruktor.
    """

    def __init__(self, scene: QGraphicsScene | None = None, parent=None) -> None:
        super().__init__(scene, parent)
        self._setup()

    # ------------------------------------------------------------------
    # Einrichtung
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        self.setFixedWidth(_DEFAULT_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setBackgroundBrush(Qt.GlobalColor.darkGray)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setInteractive(False)

    # ------------------------------------------------------------------
    # Navigation deaktivieren
    # ------------------------------------------------------------------

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()

    def keyPressEvent(self, event) -> None:
        event.ignore()
