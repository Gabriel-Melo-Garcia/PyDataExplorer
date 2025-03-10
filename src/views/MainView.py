from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, 
    QTableWidget, QDockWidget, QTextEdit, QTableWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction

class MainView(QMainWindow):
    # Sinais existentes
    load_data_signal = pyqtSignal(str)
    filter_data_signal = pyqtSignal()
    clean_filter_signal = pyqtSignal()
    show_duplicates_signal = pyqtSignal()
    drop_duplicates_signal = pyqtSignal()
    describe_numeric_signal = pyqtSignal()
    describe_categorical_signal = pyqtSignal()
    open_change_type_dialog_signal = pyqtSignal(str)
    open_handle_null_dialog_signal = pyqtSignal(str)
    open_graph_view_signal = pyqtSignal()
    open_map_values_view_signal = pyqtSignal()
    

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_drawer()

    def init_ui(self):
        self.setWindowTitle("PyDataExplorer")
        self.setMinimumSize(850, 550)

        # Menu bar
        menubar = self.menuBar()
        self.change_type_menu = menubar.addMenu("Change Type")
        self.null_value_handling_menu = menubar.addMenu("Handle Null")
        self.description_menu = menubar.addMenu("description")

        # Layout principal
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        left_btn_list_layout = QVBoxLayout()
        table_layout = QVBoxLayout()

        # Widgets
        self.table_widget = QTableWidget()
        self.btn_add_dataframe = QPushButton("Add DataFrame")
        self.btn_show_details = QPushButton("Show Details")
        # self.btn_group_by = QPushButton("Group")
        self.btn_filter_data = QPushButton("Filter")
        self.btn_clean_filter = QPushButton("Clean Filter")
        self.btn_map_values = QPushButton("Map")
        self.btn_open_graph = QPushButton("Graph")
        self.lb_status = QLabel(" ")

        # Conectar botões
        self.btn_add_dataframe.clicked.connect(self.open_file_dialog)
        self.btn_show_details.clicked.connect(self.toggle_drawer)
        self.btn_filter_data.clicked.connect(self.filter_data_signal.emit)
        self.btn_clean_filter.clicked.connect(self.clean_filter_signal.emit)
        self.btn_map_values.clicked.connect(self.open_map_values_view_signal.emit)
        self.btn_open_graph.clicked.connect(self.open_graph_view_signal.emit)

        # Montar layout
        left_btn_list_layout.addWidget(self.btn_add_dataframe)
        left_btn_list_layout.addWidget(self.btn_show_details)
        # left_btn_list_layout.addWidget(self.btn_group_by)
        left_btn_list_layout.addWidget(self.btn_filter_data)
        left_btn_list_layout.addWidget(self.btn_clean_filter)
        left_btn_list_layout.addWidget(self.btn_map_values)
        left_btn_list_layout.addWidget(self.btn_open_graph)

        table_layout.addWidget(self.table_widget, 4)
        table_layout.addWidget(self.lb_status, 1)

        main_layout.addLayout(left_btn_list_layout, 1)
        main_layout.addLayout(table_layout, 3)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open csv/xlsx File", "./data", "Files (*.csv *.xlsx)")
        if file_path:
            self.load_data_signal.emit(file_path)

    def update_table(self, dataframe):
        if dataframe is not None:
            self.table_widget.setRowCount(dataframe.shape[0])
            self.table_widget.setColumnCount(dataframe.shape[1])
            self.table_widget.setHorizontalHeaderLabels(dataframe.columns)
            for row in range(dataframe.shape[0]):
                for col in range(dataframe.shape[1]):
                    item = QTableWidgetItem(str(dataframe.iat[row, col]))
                    self.table_widget.setItem(row, col, item)
        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

    def update_status(self, message):
        self.lb_status.setText(message)

    def update_menus(self, columns):
        self.change_type_menu.clear()
        self.null_value_handling_menu.clear()
        self.description_menu.clear()
        if columns:
            for column in columns:
                change_action = QAction(column, self)
                null_action = QAction(column, self)
                change_action.triggered.connect(lambda _, col=column: self.open_change_type_dialog_signal.emit(col))
                null_action.triggered.connect(lambda _, col=column: self.open_handle_null_dialog_signal.emit(col))
                self.change_type_menu.addAction(change_action)
                self.null_value_handling_menu.addAction(null_action)
            desc_numeric = QAction("Numeric Columns", self)
            desc_categoric = QAction("Categoric Columns", self)
            desc_numeric.triggered.connect(self.describe_numeric_signal.emit)
            desc_categoric.triggered.connect(self.describe_categorical_signal.emit)
            self.description_menu.addAction(desc_numeric)
            self.description_menu.addAction(desc_categoric)
        else:
            self.change_type_menu.addAction("No Dataframe Loaded").setEnabled(False)
            self.null_value_handling_menu.addAction("No Dataframe Loaded").setEnabled(False)
            self.description_menu.addAction("No Dataframe Loaded").setEnabled(False)

    def init_drawer(self):
        self.drawer = QDockWidget("Details", self)
        self.drawer.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        container = QWidget()
        layout = QVBoxLayout()
        self.drawer_text = QTextEdit()
        self.drawer_text.setReadOnly(True)
        self.btn_duplicate_show = QPushButton("Show Duplicates")
        self.btn_duplicate_drop = QPushButton("Drop Duplicates")
        self.btn_duplicate_show.clicked.connect(self.show_duplicates_signal.emit)
        self.btn_duplicate_drop.clicked.connect(self.drop_duplicates_signal.emit)
        layout.addWidget(self.drawer_text)
        layout.addWidget(self.btn_duplicate_show)
        layout.addWidget(self.btn_duplicate_drop)
        container.setLayout(layout)
        self.drawer.setWidget(container)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.drawer)
        self.drawer.hide()

    def toggle_drawer(self):
        self.drawer.setVisible(not self.drawer.isVisible())

    def update_drawer(self, info, has_duplicates):
        self.drawer_text.setPlainText(info)
        self.btn_duplicate_show.setVisible(has_duplicates)
        self.btn_duplicate_drop.setVisible(has_duplicates)