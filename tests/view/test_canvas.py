from mvc import BaseCanvas, BaseCanvasScene


class _Scene(BaseCanvasScene):
    """Minimale konkrete Szene nur für Tests."""

    def setup_scene(self) -> None:
        pass

    def on_reset(self) -> None:
        self.clear()


def test_canvas_starts_maximized(qapp):
    scene = _Scene()
    canvas = BaseCanvas(scene)

    canvas.show_fullscreen()
    qapp.processEvents()

    assert canvas.window().isMaximized(), (
        "Canvas-Fenster sollte nach show_fullscreen() maximiert sein"
    )

    canvas.close()
