"""
EntityCanvasEntity — rechteckiges ERD-Entity-Element für den BaseCanvas.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget

from mvc.view.entity import BaseCanvasEntity

_WIDTH = 160
_HEIGHT = 80
_BORDER_WIDTH = 2
_FONT_SIZE = 11


class EntityCanvasEntity(BaseCanvasEntity):
    """
    Stellt eine ERD-Entität als weißes Rechteck mit schwarzer Umrandung dar.

    Attribute
    ---------
    ID          : eindeutiger Bezeichner der Entität
    name        : angezeigter Name (wird im Rechteck zentriert dargestellt)
    description : optionale Beschreibung
    """

    def __init__(
        self,
        ID: str,
        name: str,
        description: str = "",
        parent: QGraphicsObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.ID = ID
        self.name = name
        self.description = description

    # ------------------------------------------------------------------
    # QGraphicsItem-Schnittstelle
    # ------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, _WIDTH, _HEIGHT)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None,
    ) -> None:
        rect = self.boundingRect()

        # Weißes Rechteck mit schwarzer Umrandung
        painter.setPen(QPen(QColor("black"), _BORDER_WIDTH))
        painter.setBrush(QBrush(QColor("white")))
        painter.drawRect(rect)

        # Name zentriert
        font = QFont()
        font.setPointSize(_FONT_SIZE)
        painter.setFont(font)
        painter.setPen(QPen(QColor("black")))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)
