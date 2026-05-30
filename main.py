"""
Einstiegspunkt — MVC-Framework mit PyQt6.
"""

import sys

from PyQt6.QtWidgets import QApplication

from mvc import BaseCanvas, BaseScene, BaseToolbox, MainWindow
from mvc.view.ERDelements import EntityCanvasEntity


class Scene(BaseScene):
    def setup_scene(self) -> None:
        entity = EntityCanvasEntity(ID="1", name="Kunde", description="Ein Kunde")
        self.addItem(entity)
        entity.setPos(100, 100)

    def on_reset(self) -> None:
        self.clear()


class View(MainWindow):
    def setup_ui(self) -> None:
        toolbox = BaseToolbox()
        canvas = BaseCanvas(Scene())
        self._build_split_layout(toolbox, canvas)

    def connect_signals(self) -> None:
        pass

    def refresh(self, _key: str, _value: object) -> None:
        pass

    def reset(self) -> None:
        pass


def main() -> None:
    app = QApplication(sys.argv)

    view = View()
    view.setup_ui()
    view.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
