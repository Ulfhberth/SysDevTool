"""
BaseCanvas — generische Basisklasse für interaktive Vollbild-Canvases.

Verantwortlichkeiten:
  - Vollbilddarstellung einer QGraphicsScene
  - Zoom per Mausrad (zentriert auf Mauszeiger)
  - Pan per Linksklick-Ziehen
  - Tastaturkürzel: Pos1 → Szene einpassen, +/- → Zoom
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QPainter, QWheelEvent
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView

_ZOOM_MIN = 0.02
_ZOOM_MAX = 50.0
_ZOOM_FACTOR = 1.15


class BaseCanvas(QGraphicsView):
    """
    Interaktiver Vollbild-Canvas.

    Nutzung
    -------
    canvas = ConcreteCanvas(scene)
    canvas.show_fullscreen()          # Elternfenster in den Vollbildmodus

    Interaktion
    -----------
    Mausrad          – Zoom (unter Mauszeiger)
    Linksklick+Drag  – Verschieben (Pan)
    Pos1 / H         – Szene vollständig einpassen
    +  /  =          – Einzoomen
    -                – Auszoomen
    """

    def __init__(self, scene: QGraphicsScene, parent=None) -> None:
        super().__init__(scene, parent)
        self._setup()

    # ------------------------------------------------------------------
    # Einrichtung
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate
        )
        self.setBackgroundBrush(Qt.GlobalColor.darkGray)

    # ------------------------------------------------------------------
    # Öffentliche Methoden
    # ------------------------------------------------------------------

    def show_fullscreen(self) -> None:
        """Maximiert das Elternfenster (Titelleiste bleibt sichtbar)."""
        self.window().showMaximized()

    def fit_scene(self) -> None:
        """Passt die gesamte Szene in den sichtbaren Bereich ein."""
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def zoom_in(self) -> None:
        """Zoomt um einen Schritt heran."""
        self._apply_zoom(_ZOOM_FACTOR)

    def zoom_out(self) -> None:
        """Zoomt um einen Schritt heraus."""
        self._apply_zoom(1.0 / _ZOOM_FACTOR)

    # ------------------------------------------------------------------
    # Event-Overrides
    # ------------------------------------------------------------------

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        if delta > 0:
            self._apply_zoom(_ZOOM_FACTOR)
        elif delta < 0:
            self._apply_zoom(1.0 / _ZOOM_FACTOR)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key in (Qt.Key.Key_Home, Qt.Key.Key_H):
            self.fit_scene()
        elif key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
            self.zoom_in()
        elif key == Qt.Key.Key_Minus:
            self.zoom_out()
        else:
            super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Intern
    # ------------------------------------------------------------------

    def _apply_zoom(self, factor: float) -> None:
        current = self.transform().m11()
        new_scale = current * factor
        if _ZOOM_MIN <= new_scale <= _ZOOM_MAX:
            self.scale(factor, factor)
