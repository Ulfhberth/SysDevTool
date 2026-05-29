"""
Einstiegspunkt — MVC-Framework-Demo mit PyQt6.

Startet die Beispielanwendung (Task-Manager).
"""

import sys

from PyQt6.QtWidgets import QApplication

from mvc.example import TaskController, TaskModel, TaskView


def main() -> None:
    app = QApplication(sys.argv)

    model = TaskModel()
    view = TaskView()
    TaskController(model, view, parent=view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
