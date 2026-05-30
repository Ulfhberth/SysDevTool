"""
MainWindow — generische Basisklasse für alle Views im MVC-Framework.

Verantwortlichkeiten:
  - Darstellung des Modell-Zustands
  - Weiterleitung von Nutzerinteraktionen an den Controller via Signale
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
    QStatusBar,
    QWidget,
)

if TYPE_CHECKING:
    from .base_canvas import BaseCanvas
    from .base_toolbox import BaseToolbox


class MainWindow(QMainWindow):
    """
    Abstrakte Basisklasse für Views.

    Signale
    -------
    action_requested(action, payload)
        Wird emittiert, wenn der Nutzer eine Aktion auslöst.
        action  – symbolischer Aktionsname (str)
        payload – beliebige Nutzdaten (z. B. dict, str, int …)

    Konventionen
    ------------
    Konkrete Views rufen ``self.action_requested.emit("action_name", data)``
    auf, anstatt direkt Controller-Methoden aufzurufen. Der Controller
    registriert sich auf dieses Signal und leitet die Aktion an das Modell
    weiter. Dadurch bleibt die View frei von Controller-Abhängigkeiten.
    """

    action_requested: pyqtSignal = pyqtSignal(str, object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)

    # ------------------------------------------------------------------
    # Layout-Hilfsmethode
    # ------------------------------------------------------------------

    def _build_split_layout(
        self,
        toolbox: BaseToolbox,
        canvas: BaseCanvas,
    ) -> None:
        """Richtet das Zweispaltenlayout ein: Toolbox | Trennlinie | Canvas."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(toolbox)
        layout.addWidget(separator)
        layout.addWidget(canvas, stretch=1)

        self.setCentralWidget(container)

    # ------------------------------------------------------------------
    # Öffentliche Hilfsmethoden
    # ------------------------------------------------------------------

    def show_status(self, message: str, timeout_ms: int = 3000) -> None:
        """Zeigt eine kurzlebige Statusnachricht in der Statusleiste."""
        self._status_bar.showMessage(message, timeout_ms)

    def show_error(self, message: str) -> None:
        """Zeigt eine Fehlermeldung dauerhaft in der Statusleiste."""
        self._status_bar.showMessage(f"Fehler: {message}")

    # ------------------------------------------------------------------
    # Abstrakte Schnittstelle – von konkreten Views zu implementieren
    # ------------------------------------------------------------------

    @abstractmethod
    def setup_ui(self) -> None:
        """Alle Widgets erzeugen und im Layout anordnen."""

    @abstractmethod
    def connect_signals(self) -> None:
        """Widget-Ereignisse mit action_requested verknüpfen."""

    @abstractmethod
    def refresh(self, key: str, value: object) -> None:
        """
        Wird vom Controller aufgerufen, wenn das Modell data_changed emittiert.
        key/value entsprechen den Parametern des Modell-Signals.
        """

    @abstractmethod
    def reset(self) -> None:
        """Wird aufgerufen, wenn das Modell data_reset emittiert."""
