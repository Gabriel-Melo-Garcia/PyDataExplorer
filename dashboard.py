from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit, QListWidget, QListWidgetItem,
    QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QGridLayout, QTextEdit, QTabWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import plotly.express as px
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class DashboardView(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data
        self.graph_list = []  # Lista única para todos os gráficos (padrão e agrupados)
        self.setWindowTitle("Dashboard de Análise de Dados")
        self.setMinimumSize(1000, 700)

        # Widget central e layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Painel de controle (esquerda)
        self.control_panel = QVBoxLayout()
        self.main_layout.addLayout(self.control_panel, 1)

        # Área de gráficos (direita)
        self.graph_area = QGridLayout()
        self.main_layout.addLayout(self.graph_area, 3)

        # Tabs para separar controles
        self.tabs = QTabWidget()
        self.tab_standard = QWidget()
        self.tab_grouped = QWidget()
        self.tabs.addTab(self.tab_standard, "Gráficos Padrão")
        self.tabs.addTab(self.tab_grouped, "Gráficos Agrupados")

        # Layouts das abas
        self.standard_layout = QVBoxLayout(self.tab_standard)
        self.grouped_layout = QVBoxLayout(self.tab_grouped)

        # Controles para gráficos padrão (aba 1)
        self.cb_graph_type = QComboBox()
        self.cb_graph_type.addItems(["Histogram", "Scatter", "Line", "Bar", "Heatmap", "Boxplot"])
        self.cb_graph_type.currentIndexChanged.connect(self.update_controls)

        self.cb_column_x = QComboBox()
        self.cb_column_y = QComboBox()
        self.cb_general = QComboBox()
        self.update_columns()

        self.txt_input_title = QLineEdit()
        self.txt_input_title.setPlaceholderText("Título do Gráfico")

        self.btn_generate = QPushButton("Gerar Gráfico")
        self.btn_generate.clicked.connect(self.generate_graph)

        self.standard_layout.addWidget(self.cb_graph_type)
        self.standard_layout.addWidget(self.cb_column_x)
        self.standard_layout.addWidget(self.cb_column_y)
        self.standard_layout.addWidget(self.cb_general)
        self.standard_layout.addWidget(self.txt_input_title)
        self.standard_layout.addWidget(self.btn_generate)
        self.standard_layout.addStretch()

        # Controles para agrupamento (aba 2)
        self.cb_col_to_group = QComboBox()
        self.cb_col_target = QComboBox()
        self.cb_method = QComboBox()
        self.cb_col_to_group.addItems(self.data.columns)
        self.cb_col_target.addItems(self.data.columns)
        self.cb_method.addItems(['mean', 'sum'])

        self.txt_group_result = QTextEdit()
        self.txt_group_result.setReadOnly(True)
        font = QFont()
        font.setPointSize(12)
        self.txt_group_result.setFont(font)
        self.txt_group_result.setMaximumHeight(100)

        self.btn_show_group = QPushButton("Mostrar Agrupamento")
        self.btn_show_group.clicked.connect(self.show_group)

        self.btn_plot_group = QPushButton("Plotar Agrupamento")
        self.btn_plot_group.clicked.connect(self.plot_group)

        self.grouped_layout.addWidget(self.cb_col_to_group)
        self.grouped_layout.addWidget(self.cb_col_target)
        self.grouped_layout.addWidget(self.cb_method)
        self.grouped_layout.addWidget(self.btn_show_group)
        self.grouped_layout.addWidget(self.btn_plot_group)
        self.grouped_layout.addWidget(self.txt_group_result)
        self.grouped_layout.addStretch()

        # Lista unificada de gráficos e botão "Visualizar Tudo" fora das abas
        self.graph_list_widget = QListWidget()
        self.btn_show_all = QPushButton("Visualizar Tudo")
        self.btn_show_all.clicked.connect(self.show_all_graphs)

        # Adicionar ao painel de controle
        self.control_panel.addWidget(self.tabs)
        self.control_panel.addWidget(self.btn_show_all)
        self.control_panel.addWidget(self.graph_list_widget)
        self.control_panel.addStretch()

        # Área de gráficos inicialmente vazia
        self.graph_view = QWebEngineView()
        self.graph_area.addWidget(self.graph_view, 0, 0)

    def update_columns(self):
        self.cb_column_x.clear()
        self.cb_column_y.clear()
        if self.data is not None and not self.data.empty:
            self.cb_column_x.addItems(self.data.columns)
            self.cb_column_y.addItems(self.data.columns)
            self.update_controls()
        else:
            self.cb_column_x.addItem("Sem dados")
            self.cb_column_y.addItem("Sem dados")

    def update_controls(self):
        graph_type = self.cb_graph_type.currentText()
        self.cb_general.clear()
        if graph_type == "Histogram":
            self.cb_column_y.hide()
            self.cb_general.addItems(['5', '10', '15', '20', '25', '30', '50'])
            self.cb_general.show()
        elif graph_type == "Heatmap":
            self.cb_column_x.hide()
            self.cb_column_y.hide()
            self.cb_general.addItems(['viridis', 'plasma', 'inferno', 'magma'])
            self.cb_general.show()
        else:
            self.cb_column_x.show()
            self.cb_column_y.show()
            self.cb_general.hide()

    def generate_graph(self):
        if self.data is None or self.data.empty:
            print("Sem dados carregados.")
            return

        graph_type = self.cb_graph_type.currentText()
        col_x = self.cb_column_x.currentText()
        col_y = self.cb_column_y.currentText()
        title = self.txt_input_title.text() or f"{graph_type} - {col_x}"

        try:
            if graph_type == "Histogram":
                fig = px.histogram(self.data, x=col_x, nbins=int(self.cb_general.currentText()), title=title)
            elif graph_type == "Scatter":
                fig = px.scatter(self.data, x=col_x, y=col_y, title=title)
            elif graph_type == "Line":
                fig = px.line(self.data, x=col_x, y=col_y, title=title)
            elif graph_type == "Bar":
                fig = px.bar(self.data, x=col_x, y=col_y, title=title)
            elif graph_type == "Heatmap":
                fig = px.imshow(self.data.corr(numeric_only=True), color_continuous_scale=self.cb_general.currentText(), title=title)
            elif graph_type == "Boxplot":
                fig = px.box(self.data, x=col_x, y=col_y, title=title)

            html_content = fig.to_html(include_plotlyjs="cdn")
            self.graph_list.append({"title": title, "html": html_content})
            self.update_graph_list_widget()
            print(f"Gráfico padrão '{title}' adicionado. Total: {len(self.graph_list)} gráficos.")
            self.graph_view.setHtml(html_content)

        except Exception as e:
            print(f"Erro ao gerar o gráfico: {e}")

    def show_group(self):
        try:
            txt_col_1 = self.cb_col_to_group.currentText()
            txt_col_2 = self.cb_col_target.currentText()
            txt_method = self.cb_method.currentText()

            if txt_method == 'mean':
                result = self.data.groupby(txt_col_1)[txt_col_2].mean()
            else:
                result = self.data.groupby(txt_col_1)[txt_col_2].sum()

            group_string = [f'{txt_method} {txt_col_2} grouped by {txt_col_1}']
            group_string.extend(f"{index}:  {value:.2f}" for index, value in result.items())
            self.txt_group_result.setPlainText("\n".join(group_string))

            self.grouped_data = result.reset_index()
        except Exception as e:
            self.txt_group_result.setPlainText(f'Erro: {e}')

    def plot_group(self):
        if not hasattr(self, 'grouped_data') or self.grouped_data.empty:
            print("Nenhum agrupamento disponível para plotar. Execute 'Mostrar Agrupamento' primeiro.")
            return

        try:
            txt_col_1 = self.cb_col_to_group.currentText()
            txt_col_2 = self.cb_col_target.currentText()
            txt_method = self.cb_method.currentText()
            title = f"{txt_method.capitalize()} de {txt_col_2} por {txt_col_1}"

            fig = px.bar(self.grouped_data, x=txt_col_1, y=txt_col_2, title=title)
            html_content = fig.to_html(include_plotlyjs="cdn")
            self.graph_list.append({"title": title, "html": html_content})
            self.update_graph_list_widget()
            print(f"Gráfico agrupado '{title}' adicionado. Total: {len(self.graph_list)} gráficos.")
            self.graph_view.setHtml(html_content)

        except Exception as e:
            print(f"Erro ao plotar o agrupamento: {e}")

    def update_graph_list_widget(self):
        self.graph_list_widget.clear()
        for idx, graph in enumerate(self.graph_list):
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)

            label = QLineEdit(graph["title"])
            label.setReadOnly(True)
            item_layout.addWidget(label)

            btn_delete = QPushButton("X")
            btn_delete.setMaximumWidth(20)
            btn_delete.clicked.connect(lambda _, i=idx: self.delete_graph(i))
            item_layout.addWidget(btn_delete)

            item = QListWidgetItem(self.graph_list_widget)
            item.setSizeHint(item_widget.sizeHint())
            self.graph_list_widget.setItemWidget(item, item_widget)

    def delete_graph(self, index):
        if 0 <= index < len(self.graph_list):
            del self.graph_list[index]
            self.update_graph_list_widget()
            print(f"Gráfico {index} removido. Total: {len(self.graph_list)} gráficos.")
            if self.graph_area.count() > 1:
                self.show_all_graphs()

    def show_all_graphs(self):
        if not self.graph_list:
            print("Nenhum gráfico gerado ainda.")
            return

        for i in reversed(range(self.graph_area.count())):
            self.graph_area.itemAt(i).widget().deleteLater()

        num_graphs = len(self.graph_list)
        cols = 2
        rows = (num_graphs + cols - 1) // cols

        for idx, graph in enumerate(self.graph_list):
            graph_widget = QWebEngineView()
            graph_widget.setHtml(graph["html"])
            row = idx // cols
            col = idx % cols
            self.graph_area.addWidget(graph_widget, row, col)