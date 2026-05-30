"""
ERDCanvasRelationship — Diamant-förmige ERD-Relationship für den BaseCanvas.
"""

from __future__ import annotations

import math

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QPolygonF
from PyQt6.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget

from mvc.view.base_canvas_entity import BaseCanvasEntity
from mvc.view.base_canvas_relationship import BaseCanvasRelationship

_DIAMOND_MIN_HALF = 35
_PAD = 14
_FONT_SIZE_LABEL = 12
_FONT_SIZE_CARD = 12
_BORDER_WIDTH = 2
_CARD_DISTANCE = 50   # Abstand Kardinalitätslabel vom Entity-Zentrum in Px
_CARD_SIZE = 20       # Zeichenfläche für ein Kardinalitätszeichen (Quadrat)
_BOUNDING_MARGIN = 30

_COLOR_FILL = QColor(0xF0, 0x8D, 0x00)
_COLOR_STROKE = QColor(00, 00, 00)
_COLOR_TEXT = QColor(20, 20, 20)


class ERDCanvasRelationship(BaseCanvasRelationship):
    """
    Stellt eine ERD-Relationship als Diamant mit Verbindungslinien dar.

    Attribute
    ---------
    label              : Verb-Phrase, zentriert im Diamant (regular, 12 px)
    source_cardinality : Zeichen nahe der Quell-Entity ('1', 'm', 'n')
    target_cardinality : Zeichen nahe der Ziel-Entity  ('1', 'm', 'n')
    """

    def __init__(
        self,
        source: BaseCanvasEntity,
        target: BaseCanvasEntity,
        label: str = "",
        source_cardinality: str = "1",
        target_cardinality: str = "1",
        parent: QGraphicsObject | None = None,
    ) -> None:
        super().__init__(source, target, parent)
        self._label = label
        self._source_cardinality = source_cardinality
        self._target_cardinality = target_cardinality

        self._label_font = QFont()
        self._label_font.setPointSize(_FONT_SIZE_LABEL)

        self._card_font = QFont()
        self._card_font.setPointSize(_FONT_SIZE_CARD)

        # Geometrie neu berechnen wenn Entities verschoben werden
        self._source.xChanged.connect(self._on_entity_moved)
        self._source.yChanged.connect(self._on_entity_moved)
        self._target.xChanged.connect(self._on_entity_moved)
        self._target.yChanged.connect(self._on_entity_moved)

    def _on_entity_moved(self) -> None:
        self.prepareGeometryChange()
        self.update()

    # ------------------------------------------------------------------
    # Geometrie-Hilfsmethoden
    # ------------------------------------------------------------------

    def _entity_center(self, entity: BaseCanvasEntity) -> QPointF:
        return entity.mapToScene(entity.boundingRect().center())

    def _diamond_half(self) -> float:
        label_w = QFontMetrics(self._label_font).horizontalAdvance(self._label)
        label_h = QFontMetrics(self._label_font).height()
        # Einbeschriebenes Quadrat im Diamant hat Seite = half * sqrt(2)
        # → half = Seite / sqrt(2)
        needed = (max(label_w, label_h) + 2 * _PAD) / math.sqrt(2)
        return max(_DIAMOND_MIN_HALF, needed)

    def _diamond_center(self) -> QPointF:
        src = self._entity_center(self._source)
        tgt = self._entity_center(self._target)
        return QPointF((src.x() + tgt.x()) / 2, (src.y() + tgt.y()) / 2)

    def _diamond_polygon(self, center: QPointF, half: float) -> QPolygonF:
        return QPolygonF([
            QPointF(center.x(),        center.y() - half),  # oben
            QPointF(center.x() + half, center.y()),          # rechts
            QPointF(center.x(),        center.y() + half),  # unten
            QPointF(center.x() - half, center.y()),          # links
        ])

    def _nearest_vertex(self, center: QPointF, half: float, ref: QPointF) -> QPointF:
        """Diamant-Vertex, der ref am nächsten liegt."""
        vertices = [
            QPointF(center.x(),        center.y() - half),
            QPointF(center.x() + half, center.y()),
            QPointF(center.x(),        center.y() + half),
            QPointF(center.x() - half, center.y()),
        ]
        return min(vertices, key=lambda v: (v.x() - ref.x()) ** 2 + (v.y() - ref.y()) ** 2)

    def _point_along(self, from_: QPointF, to: QPointF, distance: float) -> QPointF:
        """Punkt im Abstand distance von from_ in Richtung to."""
        dx, dy = to.x() - from_.x(), to.y() - from_.y()
        length = math.hypot(dx, dy)
        if length == 0:
            return from_
        return QPointF(from_.x() + dx / length * distance,
                       from_.y() + dy / length * distance)

    # ------------------------------------------------------------------
    # QGraphicsItem-Schnittstelle
    # ------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        src = self._entity_center(self._source)
        tgt = self._entity_center(self._target)
        center = QPointF((src.x() + tgt.x()) / 2, (src.y() + tgt.y()) / 2)
        half = self._diamond_half()

        xs = [src.x(), tgt.x(), center.x() - half, center.x() + half]
        ys = [src.y(), tgt.y(), center.y() - half, center.y() + half]

        return QRectF(
            min(xs) - _BOUNDING_MARGIN,
            min(ys) - _BOUNDING_MARGIN,
            max(xs) - min(xs) + 2 * _BOUNDING_MARGIN,
            max(ys) - min(ys) + 2 * _BOUNDING_MARGIN,
        )

    def paint(
        self,
        painter: QPainter,
        _option: QStyleOptionGraphicsItem,
        _widget: QWidget | None = None,
    ) -> None:
        src = self._entity_center(self._source)
        tgt = self._entity_center(self._target)
        center = self._diamond_center()
        half = self._diamond_half()

        src_vertex = self._nearest_vertex(center, half, src)
        tgt_vertex = self._nearest_vertex(center, half, tgt)

        pen = QPen(_COLOR_STROKE, _BORDER_WIDTH)

        # Verbindungslinien (unter dem Diamant)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(src, src_vertex)
        painter.drawLine(tgt, tgt_vertex)

        # Diamant (überdeckt die Linienenden sauber)
        painter.setBrush(_COLOR_FILL)
        painter.drawPolygon(self._diamond_polygon(center, half))

        # Label im Diamant
        if self._label:
            painter.setFont(self._label_font)
            painter.setPen(_COLOR_TEXT)
            painter.drawText(
                QRectF(center.x() - half, center.y() - half, 2 * half, 2 * half),
                Qt.AlignmentFlag.AlignCenter,
                self._label,
            )

        # Kardinalitäten nahe der Entities
        painter.setFont(self._card_font)
        painter.setPen(_COLOR_TEXT)
        for entity_center, vertex, cardinality in [
            (src, src_vertex, self._source_cardinality),
            (tgt, tgt_vertex, self._target_cardinality),
        ]:
            pos = self._point_along(entity_center, vertex, _CARD_DISTANCE)
            painter.drawText(
                QRectF(pos.x() - _CARD_SIZE / 2, pos.y() - _CARD_SIZE / 2,
                       _CARD_SIZE, _CARD_SIZE),
                Qt.AlignmentFlag.AlignCenter,
                cardinality,
            )
