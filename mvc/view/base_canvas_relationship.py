"""
BaseCanvasRelationship — abstrakte Basisklasse für gerichtete Verbindungen zwischen
BaseCanvasEntity-Instanzen auf einem BaseCanvas.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget

if TYPE_CHECKING:
    from .base_canvas_entity import BaseCanvasEntity


class BaseCanvasRelationship(QGraphicsObject):
    """
    Abstrakte Basisklasse für visuelle Verknüpfungen zwischen Canvas-Entities.

    Eine Relationship verbindet genau eine Quell-Entity (source) mit einer
    Ziel-Entity (target) und wird von Qt als eigenständiges GraphicsItem
    gerendert.

    Konkrete Ableitungen implementieren boundingRect() und paint() sowie
    bei Bedarf shape() für präzise Maus-Treffererkennung auf Linien.

    Fehler
    ------
    TypeError
        Wenn source oder target None sind.
    """

    def __init__(
        self,
        source: BaseCanvasEntity,
        target: BaseCanvasEntity,
        parent: QGraphicsObject | None = None,
    ) -> None:
        if source is None or target is None:
            raise TypeError("source und target dürfen nicht None sein.")
        super().__init__(parent)
        self._source = source
        self._target = target
        self.setFlags(
            QGraphicsObject.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsObject.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setZValue(-1)

    # ------------------------------------------------------------------
    # Zugriff
    # ------------------------------------------------------------------

    @property
    def source(self) -> BaseCanvasEntity:
        return self._source

    @property
    def target(self) -> BaseCanvasEntity:
        return self._target

    # ------------------------------------------------------------------
    # Abstrakte Schnittstelle – von konkreten Relationships zu implementieren
    # ------------------------------------------------------------------

    @abstractmethod
    def boundingRect(self) -> QRectF:
        """Begrenzungsrechteck der Verbindung (wird von Qt für Culling genutzt)."""

    @abstractmethod
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None,
    ) -> None:
        """Zeichnet die Verbindung in den Canvas."""
