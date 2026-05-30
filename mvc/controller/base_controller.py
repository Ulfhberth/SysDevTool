"""
BaseController — generische Basisklasse für alle Controller im MVC-Framework.

Verantwortlichkeiten:
  - Signal-Routing zwischen Model und View
  - Anwendungslogik, die weder in Model noch View gehört
"""

from abc import abstractmethod

from PyQt6.QtCore import QObject

from ..model import BaseModel
from ..view import MainWindow


class BaseController(QObject):
    """
    Abstrakte Basisklasse für Controller.

    Der Controller verbindet:
      View.action_requested  →  self._on_action      (Nutzerinteraktion → Modell)
      Model.data_changed     →  View.refresh          (Modelländerung → View)
      Model.data_reset       →  View.reset            (vollständiges Neuladen)
      Model.error_occurred   →  View.show_error       (Fehlerweiterleitung)

    Konkrete Controller können _on_action überschreiben oder eigene
    Routing-Tabellen (action → Handler) definieren.
    """

    def __init__(
        self,
        model: BaseModel,
        view: MainWindow,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self._view = view
        self._wire_signals()
        self.initialize()

    # ------------------------------------------------------------------
    # Signal-Verdrahtung (intern, einmalig im Konstruktor)
    # ------------------------------------------------------------------

    def _wire_signals(self) -> None:
        """Verbindet Model- und View-Signale mit Controller-Slots."""
        # View → Controller → Model
        self._view.action_requested.connect(self._on_action)

        # Model → View
        self._model.data_changed.connect(self._view.refresh)
        self._model.data_reset.connect(self._view.reset)
        self._model.error_occurred.connect(self._view.show_error)

    # ------------------------------------------------------------------
    # Slot: Nutzeraktion verarbeiten
    # ------------------------------------------------------------------

    def _on_action(self, action: str, payload: object) -> None:
        """
        Dispatcher: leitet action an einen dedizierten Handler weiter.

        Konkrete Controller registrieren Handler in self._action_handlers,
        einem dict[str, Callable[[object], None]], oder überschreiben
        diese Methode direkt.
        """
        handler = self._action_handlers.get(action)
        if handler:
            handler(payload)
        else:
            self._unhandled_action(action, payload)

    def _unhandled_action(self, action: str, payload: object) -> None:
        """Wird aufgerufen, wenn kein Handler für action registriert ist."""
        self._view.show_status(f"Unbekannte Aktion: {action}", 2000)

    # ------------------------------------------------------------------
    # Abstrakte Schnittstelle – von konkreten Controllern zu implementieren
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def _action_handlers(self) -> dict:
        """
        Gibt eine Routing-Tabelle { action_name: handler_callable } zurück.
        Wird von _on_action zur Dispatcher-Auflösung genutzt.
        """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialisiert den Controller nach der Signal-Verdrahtung.
        Typischer Inhalt: erstes Laden der Daten, UI-Initialisierung.
        """
