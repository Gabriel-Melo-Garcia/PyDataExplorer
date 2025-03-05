import sys
from PyQt6.QtWidgets import QApplication
from src.views.MainView import MainView
from src.controller.MainWindowController import Controller
from src.model.DataModel import DataModel



if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = DataModel()
    view = MainView()
    controller = Controller(model, view)
    view.show()
    app.exec()
    