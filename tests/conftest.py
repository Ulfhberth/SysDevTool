import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Einzelne QApplication-Instanz für alle GUI-Tests."""
    app = QApplication.instance() or QApplication([])
    yield app
