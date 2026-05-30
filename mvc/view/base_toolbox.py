"""
BaseToolbox — statische Seitenleiste links neben dem BaseCanvas.

Verantwortlichkeiten:
  - Darstellung von Werkzeugen / Steuerelementen als QGraphicsScene
  - Kein Zoom, kein Pan — rein statische Anzeige
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QWheelEvent
from PyQt6.QtWidgets import QGraphicsView, QSizePolicy

from .base_toolbox_scene import BaseToolboxScene

_DEFAULT_WIDTH = 220


class BaseToolbox(QGraphicsView):
    """
    Statischer Toolbox-Canvas für die linke Seitenleiste.

    Nicht navigierbar, nicht zoombar. Akzeptiert ausschließlich
    BaseToolboxScene-Instanzen als Scene.

    Fehler
    ------
    TypeError
        Wenn eine Scene übergeben wird, die keine BaseToolboxScene ist.
    """

    def __init__(self, scene: BaseToolboxScene | None = None, parent=None) -> None:
        if scene is None:
            scene = BaseToolboxScene()
        super().__init__(scene, parent)
        self._setup()

    def setScene(self, scene: BaseToolboxScene) -> None:
        if not isinstance(scene, BaseToolboxScene):
            raise TypeError(
                f"BaseToolbox akzeptiert nur BaseToolboxScene-Instanzen. "
                f"Übergeben: {type(scene).__name__}"
            )
        super().setScene(scene)

    # ------------------------------------------------------------------
    # Einrichtung
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        self.setFixedWidth(_DEFAULT_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
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
