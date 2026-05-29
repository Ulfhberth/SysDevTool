"""
TaskController — konkreter Controller: Aufgabenliste (Beispielanwendung).
"""

from mvc.base import BaseController
from mvc.example.model import TaskModel
from mvc.example.view import TaskView


class TaskController(BaseController):
    """
    Verbindet TaskModel und TaskView.

    Routing-Tabelle (action → Handler):
      "add_task"    → model.add_task(title)
      "remove_task" → model.remove_task(index)
      "toggle_task" → model.toggle_task(index)
      "load"        → model.load()
      "save"        → model.save()

    Zusätzlich werden modell-spezifische Signale (task_added, task_removed,
    task_toggled) direkt mit der View verdrahtet, falls differenziertere
    Reaktionen benötigt werden.
    """

    def __init__(self, model: TaskModel, view: TaskView, **kwargs) -> None:
        # _action_handlers muss vor super().__init__ existieren,
        # weil initialize() dort aufgerufen wird.
        self.__handlers: dict = {}
        super().__init__(model, view, **kwargs)

    # ------------------------------------------------------------------
    # BaseController-Schnittstelle
    # ------------------------------------------------------------------

    @property
    def _action_handlers(self) -> dict:
        return self.__handlers

    def initialize(self) -> None:
        model: TaskModel = self._model  # type: ignore[assignment]
        view: TaskView = self._view  # type: ignore[assignment]

        # Routing-Tabelle aufbauen
        self.__handlers = {
            "add_task": lambda payload: model.add_task(str(payload)),
            "remove_task": lambda payload: model.remove_task(int(payload)),
            "toggle_task": lambda payload: model.toggle_task(int(payload)),
            "load": lambda _: model.load(),
            "save": lambda _: model.save(),
        }

        # Granulare Modell-Signale → View (Erweiterungspunkt)
        model.task_added.connect(
            lambda idx, task: view.show_status(f'"{task.title}" hinzugefügt', 2000)
        )
        model.task_removed.connect(
            lambda idx: view.show_status(f"Aufgabe {idx} entfernt", 2000)
        )
        model.task_toggled.connect(
            lambda idx, done: view.show_status(
                f"Aufgabe {idx} als {'erledigt' if done else 'offen'} markiert", 2000
            )
        )

        # Initiales Laden
        model.load()
        # Nach load() data_reset emittiert; data_changed für "tasks" folgt in load()
        view.refresh("tasks", model.tasks)
