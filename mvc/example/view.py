"""
TaskView — konkrete View: Aufgabenliste (Beispielanwendung).
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mvc.base import BaseView
from mvc.example.model import Task


class TaskView(BaseView):
    """Zeigt eine Aufgabenliste mit Eingabe- und Löschschaltfläche."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MVC Task-Manager")
        self.resize(420, 380)
        self.setup_ui()
        self.connect_signals()

    # ------------------------------------------------------------------
    # BaseView-Implementierung
    # ------------------------------------------------------------------

    def setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        # Eingabezeile + Hinzufügen-Button
        input_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Neue Aufgabe …")
        self._add_btn = QPushButton("Hinzufügen")
        input_row.addWidget(self._input)
        input_row.addWidget(self._add_btn)
        root.addLayout(input_row)

        # Aufgabenliste
        self._list = QListWidget()
        root.addWidget(self._list)

        # Aktionsleiste
        action_row = QHBoxLayout()
        self._remove_btn = QPushButton("Entfernen")
        self._toggle_btn = QPushButton("Erledigt ↕")
        self._load_btn = QPushButton("Laden")
        self._save_btn = QPushButton("Speichern")
        for btn in (self._remove_btn, self._toggle_btn, self._load_btn, self._save_btn):
            action_row.addWidget(btn)
        root.addLayout(action_row)

    def connect_signals(self) -> None:
        self._add_btn.clicked.connect(self._emit_add)
        self._input.returnPressed.connect(self._emit_add)
        self._remove_btn.clicked.connect(self._emit_remove)
        self._toggle_btn.clicked.connect(self._emit_toggle)
        self._load_btn.clicked.connect(lambda: self.action_requested.emit("load", None))
        self._save_btn.clicked.connect(lambda: self.action_requested.emit("save", None))

    def refresh(self, key: str, value: object) -> None:
        if key == "tasks":
            self._rebuild_list(value)  # type: ignore[arg-type]
            self.show_status("Aktualisiert", 1500)

    def reset(self) -> None:
        """Vollständiger Neuaufbau nach model.load()."""
        # Wird indirekt über data_changed ausgelöst; reset signalisiert nur,
        # dass ein vollständiger Neuaufbau sinnvoll ist.
        self.show_status("Daten geladen", 2000)

    # ------------------------------------------------------------------
    # Interne Helfer
    # ------------------------------------------------------------------

    def _rebuild_list(self, tasks: list[Task]) -> None:
        self._list.clear()
        for task in tasks:
            item = QListWidgetItem(task.title)
            item.setCheckState(Qt.CheckState.Checked if task.done else Qt.CheckState.Unchecked)
            self._list.addItem(item)

    def _selected_index(self) -> int | None:
        row = self._list.currentRow()
        return row if row >= 0 else None

    def _emit_add(self) -> None:
        title = self._input.text()
        if title.strip():
            self.action_requested.emit("add_task", title)
            self._input.clear()

    def _emit_remove(self) -> None:
        index = self._selected_index()
        if index is not None:
            self.action_requested.emit("remove_task", index)

    def _emit_toggle(self) -> None:
        index = self._selected_index()
        if index is not None:
            self.action_requested.emit("toggle_task", index)
