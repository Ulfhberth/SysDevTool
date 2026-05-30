"""
BaseCanvasEntity — abstrakte Basisklasse für Elemente auf einem BaseCanvas.

Eine BaseCanvasEntity darf ausschließlich einer Scene zugeordnet werden,
die an einem BaseCanvas (oder einer Ableitung) hängt. Der Versuch, sie
einer BaseToolbox-Scene zuzuordnen, löst einen TypeError aus.
"""

from __future__ import annotations

from abc import abstractmethod

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem, QWidget


class BaseCanvasEntity(QGraphicsObject):
    """
    Abstrakte Basisklasse für interaktive Canvas-Elemente.

    Konkrete Klassen implementieren boundingRect() und paint().

    Standardverhalten
    -----------------
    - Auswählbar per Mausklick (ItemIsSelectable)
    - Verschiebbar per Drag (ItemIsMovable)
    - Meldet Geometrieänderungen via itemChange (ItemSendsGeometryChanges)

    Fehler
    ------
    TypeError
        Wird ausgelöst, wenn versucht wird, das Element einer Scene
        zuzuordnen, die mit einer BaseToolbox verbunden ist.
    """

    def __init__(self, parent: QGraphicsObject | None = None) -> None:
        super().__init__(parent)
        self.setFlags(
            QGraphicsObject.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsObject.GraphicsItemFlag.ItemIsMovable
            | QGraphicsObject.GraphicsItemFlag.ItemSendsGeometryChanges
        )

    # ------------------------------------------------------------------
    # Schutz: kein Einfügen in Toolbox-Scenes
    # ------------------------------------------------------------------

    def itemChange(self, change: QGraphicsObject.GraphicsItemChange, value: object) -> object:
        if change == QGraphicsObject.GraphicsItemChange.ItemSceneChange and value is not None:
            self._assert_not_toolbox_scene(value)
        return super().itemChange(change, value)

    @staticmethod
    def _assert_not_toolbox_scene(scene) -> None:
        from .toolbox import BaseToolbox  # lokaler Import verhindert Zirkelimport

        for view in scene.views():
            if isinstance(view, BaseToolbox):
                raise TypeError(
                    f"BaseCanvasEntity darf nicht auf einer BaseToolbox "
                    f"(oder Ableitung) dargestellt werden. "
                    f"Gefundene View: {type(view).__name__}"
                )

    # ------------------------------------------------------------------
    # Abstrakte Schnittstelle – von konkreten Entities zu implementieren
    # ------------------------------------------------------------------

    @abstractmethod
    def boundingRect(self) -> QRectF:
        """Begrenzungsrechteck des Elements (wird von Qt für Culling genutzt)."""

    @abstractmethod
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None,
    ) -> None:
        """Zeichnet das Element in den Canvas."""
