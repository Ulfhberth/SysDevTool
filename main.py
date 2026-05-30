"""
Einstiegspunkt — MVC-Framework mit PyQt6.
"""

import sys

from PyQt6.QtWidgets import QApplication

from mvc import BaseCanvas, BaseCanvasScene, BaseToolbox, MainWindow
from mvc.view.ERDelements import ERDCanvasEntity, ERDCanvasRelationship


class Scene(BaseCanvasScene):
    def setup_scene(self) -> None:
        kunde = ERDCanvasEntity(ID="1", name="Kunde", description="Ein Kunde")
        bestellung = ERDCanvasEntity(ID="2", name="Bestellung", description="Eine Bestellung")
        produkt = ERDCanvasEntity(ID="3", name="Produkt", description="Ein Produkt")

        kunde.setPos(-350, 0)
        bestellung.setPos(0, 0)
        produkt.setPos(350, 0)

        self.addItem(kunde)
        self.addItem(bestellung)
        self.addItem(produkt)

        erteilt = ERDCanvasRelationship(
            source=kunde,
            target=bestellung,
            label="erteilt",
            source_cardinality="1",
            target_cardinality="n",
        )
        enthaelt = ERDCanvasRelationship(
            source=bestellung,
            target=produkt,
            label="enthält",
            source_cardinality="n",
            target_cardinality="m",
        )

        self.addItem(erteilt)
        self.addItem(enthaelt)

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
