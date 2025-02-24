from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QComboBox
)
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class GraphView(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data

        self.setWindowTitle("Graph Viewer")

        self.layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.config_list = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.graph_widget = FigureCanvas(self.figure)

        # ComboBox para selecionar o tipo de gráfico
        self.cb_graph_type = QComboBox()
        self.cb_graph_type.addItems(["Histograma", "Dispersão", "Linha", "Barras"])
        self.cb_graph_type.currentIndexChanged.connect(self.buttons_visibility)

        self.cb_column_x = QComboBox()
        self.cb_column_y = QComboBox()
        self.update_cb_column()

        self.cb_bins = QComboBox()
        self.cb_bins.addItems(['5', '10', '15', '20'])

        self.txt_input_title = QLineEdit()
        self.txt_input_title.setPlaceholderText("Title")

        self.txt_input_xLabel = QLineEdit()
        self.txt_input_xLabel.setPlaceholderText("X Label")

        self.txt_input_yLabel = QLineEdit()
        self.txt_input_yLabel.setPlaceholderText("Y Label")

        self.btn_graph = QPushButton("Generate Graph")
        self.btn_graph.clicked.connect(self.generate_graph)

        self.config_list.addWidget(self.cb_graph_type)
        self.config_list.addWidget(self.cb_column_x)
        self.config_list.addWidget(self.cb_column_y)
        self.config_list.addWidget(self.cb_bins)
        self.config_list.addWidget(self.txt_input_title)
        self.config_list.addWidget(self.txt_input_xLabel)
        self.config_list.addWidget(self.txt_input_yLabel)
        self.config_list.addWidget(self.btn_graph)

        self.layout.addLayout(self.config_list, 1)
        self.layout.addWidget(self.graph_widget, 3)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setMinimumSize(800, 600)

    def update_cb_column(self):
        self.cb_column_x.clear()
        self.cb_column_y.clear()

        if self.data is not None and not self.data.empty:
            self.cb_column_x.addItems(self.data.columns)
            self.cb_column_y.addItems(self.data.columns)
        else:
            self.cb_column_x.addItem("No data loaded")
            self.cb_column_y.addItem("No data loaded")
            
    def buttons_visibility(self):
        if self.cb_graph_type.currentText() == "Histograma":
            self.cb_column_y.hide()
            self.cb_bins.show()
        else:
            self.cb_column_y.show()
            self.cb_bins.hide()

    def generate_graph(self):
        if self.data is not None and not self.data.empty:
            graph_type = self.cb_graph_type.currentText()
            col_x = self.cb_column_x.currentText()
            col_y = self.cb_column_y.currentText()

            self.ax.clear()

            try:
                if graph_type == "Histograma":
                    self.plot_histogram(col_x)
                elif graph_type == "Dispersão":
                    self.plot_scatter(col_x, col_y)
                elif graph_type == "Linha":
                    self.plot_line(col_x, col_y)
                elif graph_type == "Barras":
                    self.plot_bar(col_x, col_y)

                self.ax.set_title(self.txt_input_title.text())
                self.ax.set_xlabel(self.txt_input_xLabel.text())
                self.ax.set_ylabel(self.txt_input_yLabel.text())
                self.graph_widget.draw()

            except Exception as e:
                print("Erro ao gerar o gráfico:", e)
        else:
            print("No data loaded.")

    def plot_histogram(self, column):
        if column in self.data.columns:
            sns.histplot(self.data[column], bins=int(self.cb_bins.currentText()), ax=self.ax)

    def plot_scatter(self, x_col, y_col):
        if x_col in self.data.columns and y_col in self.data.columns:
            sns.scatterplot(data=self.data, x=x_col, y=y_col, ax=self.ax)

    def plot_line(self, x_col, y_col):
        if x_col in self.data.columns and y_col in self.data.columns:
            sns.lineplot(data=self.data, x=x_col, y=y_col, ax=self.ax)

    def plot_bar(self, x_col, y_col):
        if x_col in self.data.columns and y_col in self.data.columns:
            sns.barplot(data=self.data, x=x_col, y=y_col, ax=self.ax)

    