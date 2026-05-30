"""
ERDCanvasEntity — rechteckiges ERD-Entity-Element für den BaseCanvas.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt6.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget

from mvc.view.base_canvas_entity import BaseCanvasEntity

_MIN_WIDTH = 200
_MIN_HEIGHT = 52
_PAD_H = 24
_PAD_V = 10
_FONT_SIZE = 14
_BORDER_WIDTH = 2
_COLOR_FILL = QColor(0xE2, 0xD0, 0xB6)
_COLOR_STROKE = QColor(0, 0, 0)
_COLOR_TEXT = QColor(20, 20, 20)


class ERDCanvasEntity(BaseCanvasEntity):
    """
    Stellt eine ERD-Entität als flaches Rechteck mit zentriertem Namen dar.

    Attribute
    ---------
    ID          : eindeutiger Bezeichner der Entität
    name        : angezeigter Name (fett, 14 px, zentriert)
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
        self.description = description
        self._name = name
        self._font = QFont()
        self._font.setPointSize(_FONT_SIZE)
        self._font.setBold(True)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self.prepareGeometryChange()
        self._name = value

    # ------------------------------------------------------------------
    # Geometrie
    # ------------------------------------------------------------------

    def _text_width(self) -> float:
        return QFontMetrics(self._font).horizontalAdvance(self._name)

    def _rect_width(self) -> float:
        return max(_MIN_WIDTH, self._text_width() + 2 * _PAD_H)

    def _rect_height(self) -> float:
        return max(_MIN_HEIGHT, QFontMetrics(self._font).height() + 2 * _PAD_V)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._rect_width(), self._rect_height())

    # ------------------------------------------------------------------
    # Darstellung
    # ------------------------------------------------------------------

    def paint(
        self,
        painter: QPainter,
        _option: QStyleOptionGraphicsItem,
        _widget: QWidget | None = None,
    ) -> None:
        rect = self.boundingRect()

        painter.setFont(self._font)
        painter.setPen(QPen(_COLOR_STROKE, _BORDER_WIDTH))
        painter.setBrush(_COLOR_FILL)
        painter.drawRect(rect)

        painter.setPen(_COLOR_TEXT)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self._name)
