from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
    QTabWidget,QApplication
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.express as px
import pandas as pd
import sys

class GraphView(QMainWindow):
    # Sinais para o Controller
    graph_type_changed_signal = pyqtSignal(str, str, str)  # graph_type, x_column, y_column

    def __init__(self):
        super().__init__()
        # self.columns = columns
        self.setWindowTitle("Dashboard de Análise de Dados")
        self.setMinimumSize(1000, 700)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Painel de controle à esquerda
        self.control_panel = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tab_standard = QWidget()
        self.tab_grouped = QWidget()
        self.tabs.addTab(self.tab_standard, "defaut")
        self.tabs.addTab(self.tab_grouped, "grouped")

        # standard tab
        self.lb_name_graph = QLabel("Graph Type")
        self.cb_graph_name = QComboBox()
        self.cb_graph_name.addItems(["Scatter", "Bar", "Line", "Histogram"])
        self.cb_graph_name.currentIndexChanged.connect(self.update_butons)
        # self.cb_graph_name.currentTextChanged.connect(self.update_graph)

        self.lb_x_column = QLabel("X Axis")
        self.cb_x_column = QComboBox()
        self.cb_x_column.addItems(['coluna1','coluna2','coluna3'])
        # self.cb_x_column.currentTextChanged.connect(self.update_graph)

        self.lb_y_column = QLabel("Y Axis")
        self.cb_y_column = QComboBox()
        self.cb_y_column.addItems(['coluna1','coluna2','coluna3'])
        # self.cb_y_column.currentTextChanged.connect(self.update_graph)
        
        self.standard_layout = QVBoxLayout(self.tab_standard)
        
        self.standard_layout.addWidget(self.lb_name_graph)
        self.standard_layout.addWidget(self.cb_graph_name)
        self.standard_layout.addWidget(self.lb_x_column)
        self.standard_layout.addWidget(self.cb_x_column)
        self.standard_layout.addWidget(self.lb_y_column)
        self.standard_layout.addWidget(self.cb_y_column)
        self.standard_layout.addStretch() 
        
        # --------------------------------------------------------------------
        
        # tab grouped
        self.lb_group_column = QLabel("group column")
        self.cb_group_column = QComboBox()
        self.cb_group_column.addItems(['coluna1','coluna2','coluna3'])  # Tipos de gráficos suportados
        # self.cb_graph_name.currentTextChanged.connect(self.update_graph)

        self.lb_x_column_group = QLabel("X column")
        self.cb_x_column_group = QComboBox()
        self.cb_x_column_group.addItems(['coluna1','coluna2','coluna3'])
        # self.cb_x_column.currentTextChanged.connect(self.update_graph)

        self.lb_y_column_group = QLabel("Y Axis")
        self.cb_y_column_group = QComboBox()
        self.cb_y_column_group.addItems(['sum','mean','coluna3'])
        # self.cb_y_column.currentTextChanged.connect(self.update_graph)
        
        self.grouped_layout = QVBoxLayout(self.tab_grouped)
        
        self.grouped_layout.addWidget(self.lb_group_column)
        self.grouped_layout.addWidget(self.cb_group_column)
        self.grouped_layout.addWidget(self.lb_x_column_group)
        self.grouped_layout.addWidget(self.cb_x_column_group)
        self.grouped_layout.addWidget(self.lb_y_column_group)
        self.grouped_layout.addWidget(self.cb_y_column_group)
        self.grouped_layout.addStretch() 
        self.btn_show_graph = QPushButton('show')

        # graph area
        self.graph_display = QWebEngineView()  # Usaremos Plotly com QWebEngineView
        
        self.control_panel.addWidget(self.tabs)
        self.control_panel.addWidget(self.btn_show_graph)
        self.main_layout.addLayout(self.control_panel, 1)  
        self.main_layout.addWidget(self.graph_display, 4)  

    def update_butons(self):
        if self.cb_graph_name.currentText() == 'Histogram':
            self.lb_y_column.setVisible(False)
            self.cb_y_column.setVisible(False)
        else:
            self.lb_y_column.setVisible(True)
            self.cb_y_column.setVisible(True)
            
    def update_graph(self):
        # Emite sinal apenas se ambos os eixos estiverem selecionados
        if self.cb_x_column.currentText() and self.cb_y_column.currentText():
            self.graph_type_changed_signal.emit(
                self.cb_graph_name.currentText(),
                self.cb_x_column.currentText(),
                self.cb_y_column.currentText()
            )

    def display_graph(self, html_content):
        # Exibe o gráfico gerado pelo Controller
        self.graph_display.setHtml(html_content)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = GraphView()
    graph.show()
    app.exec()