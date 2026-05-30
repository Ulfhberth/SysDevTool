"""
BaseToolboxScene — dedizierte QGraphicsScene für BaseToolbox-Views.

Nur BaseToolbox-Instanzen dürfen diese Scene als View verwenden.
BaseCanvasEntity-Items werden abgewiesen, da sie ausschließlich auf
einem BaseCanvas dargestellt werden dürfen.
"""

from __future__ import annotations

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene

_BACKGROUND_COLOR = QColor(0x1A, 0x4D, 0x4E)


class BaseToolboxScene(QGraphicsScene):
    """
    QGraphicsScene, die ausschließlich mit BaseToolbox-Views kompatibel ist.

    Schutz
    ------
    addItem wirft TypeError, wenn versucht wird, eine BaseCanvasEntity
    (oder Ableitung) hinzuzufügen.

    Die Gegenseite — dass nur BaseToolbox-Views diese Scene nutzen dürfen —
    wird von BaseToolbox.setScene() erzwungen.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setBackgroundBrush(_BACKGROUND_COLOR)

    def addItem(self, item: QGraphicsItem) -> None:
        from .base_canvas_entity import BaseCanvasEntity  # lokaler Import verhindert Zirkelimport

        if isinstance(item, BaseCanvasEntity):
            raise TypeError(
                f"BaseToolboxScene akzeptiert keine BaseCanvasEntity-Instanzen. "
                f"Übergeben: {type(item).__name__}"
            )
        super().addItem(item)
