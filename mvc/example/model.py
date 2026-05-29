"""
TaskModel — konkretes Modell: Aufgabenliste (Beispielanwendung).
"""

from dataclasses import dataclass, field

from PyQt6.QtCore import pyqtSignal

from mvc.base import BaseModel


@dataclass
class Task:
    title: str
    done: bool = False


class TaskModel(BaseModel):
    """
    Verwaltet eine Liste von Tasks.

    Zusätzliche Signale
    -------------------
    task_added(index, task)   – ein neuer Task wurde hinzugefügt
    task_removed(index)       – ein Task wurde entfernt
    task_toggled(index, done) – der Done-Status eines Tasks hat sich geändert
    """

    task_added: pyqtSignal = pyqtSignal(int, object)
    task_removed: pyqtSignal = pyqtSignal(int)
    task_toggled: pyqtSignal = pyqtSignal(int, bool)

    def __init__(self) -> None:
        super().__init__()
        self._tasks: list[Task] = []

    # ------------------------------------------------------------------
    # Eigenschaften
    # ------------------------------------------------------------------

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    # ------------------------------------------------------------------
    # Geschäftslogik
    # ------------------------------------------------------------------

    def add_task(self, title: str) -> None:
        title = title.strip()
        if not title:
            self.error_occurred.emit("Aufgabentitel darf nicht leer sein.")
            return
        task = Task(title=title)
        self._tasks.append(task)
        index = len(self._tasks) - 1
        self.task_added.emit(index, task)
        self.data_changed.emit("tasks", self._tasks)

    def remove_task(self, index: int) -> None:
        if not (0 <= index < len(self._tasks)):
            self.error_occurred.emit(f"Ungültiger Index: {index}")
            return
        self._tasks.pop(index)
        self.task_removed.emit(index)
        self.data_changed.emit("tasks", self._tasks)

    def toggle_task(self, index: int) -> None:
        if not (0 <= index < len(self._tasks)):
            self.error_occurred.emit(f"Ungültiger Index: {index}")
            return
        task = self._tasks[index]
        task.done = not task.done
        self.task_toggled.emit(index, task.done)
        self.data_changed.emit("tasks", self._tasks)

    # ------------------------------------------------------------------
    # BaseModel-Schnittstelle
    # ------------------------------------------------------------------

    def load(self) -> None:
        """In einer echten App: Daten aus Datenbank / Datei laden."""
        self._tasks = [
            Task("Framework testen"),
            Task("Dokumentation lesen", done=True),
        ]
        self.data_reset.emit()

    def save(self) -> None:
        """In einer echten App: Daten in Datenbank / Datei schreiben."""
        print(f"[TaskModel] {len(self._tasks)} Tasks gespeichert.")
