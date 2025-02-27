from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit, QTableWidgetItem, QDockWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit,
    QDialog, QComboBox, QFormLayout, QPushButton, QTableWidget, QListWidget
)
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt
import io
import sys
import pandas as pd
from filter import FilterDialog
from dashboard import DashboardView
from group import GroupByDialog
class Main_window(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.data = None
        self.filtered_data = None
        self.graph_window = None  
        self.initui()
        self.initDrawer()
        
    def initui(self):
        
    # creating menu bar
        menubar = self.menuBar()
        self.change_type_menu = menubar.addMenu("Change Type")
        self.null_value_handling_menu = menubar.addMenu("Handle Null")
        self.description_menu = menubar.addMenu("description")
        
        #initiating the main widget and layouts
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        left_btn_list_layout = QVBoxLayout()
        table_layout = QVBoxLayout()     
        self.table_widget = QTableWidget()   
        
        #btn add dataframe
        self.btn_add_dataframe = QPushButton("Add DataFrame")
        self.btn_add_dataframe.clicked.connect(self.add_data)
        #btn show details
        self.btn_show_details = QPushButton("Show Details")
        self.btn_show_details.clicked.connect(self.toggleDrawer)
        #btn decribe
        self.btn_group_by = QPushButton("Group")
        self.btn_group_by.clicked.connect(self.groupby_dialog)
        #btn filter data
        self.btn_filter_data = QPushButton("filter")
        self.btn_filter_data.clicked.connect(self.filter_data)
        #btn clean filter
        self.btn_clean_filter = QPushButton("clean filter")
        self.btn_clean_filter.clicked.connect(self.update_defaut_table)
        #btn open graph
        self.btn_open_graph = QPushButton("Graph")
        self.btn_open_graph.clicked.connect(self.open_graph_window)
        
        self.lb_4 = QLabel(" ")
        
        left_btn_list_layout.addWidget(self.btn_add_dataframe)
        left_btn_list_layout.addWidget(self.btn_show_details)
        left_btn_list_layout.addWidget(self.btn_group_by)
        left_btn_list_layout.addWidget(self.btn_filter_data)
        left_btn_list_layout.addWidget(self.btn_clean_filter)
        left_btn_list_layout.addWidget(self.btn_open_graph)
        
        table_layout.addWidget(self.table_widget,4)
        table_layout.addWidget(self.lb_4,1)
        
        main_layout.addLayout(left_btn_list_layout,1)
        main_layout.addLayout(table_layout,3)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        # self.setGeometry(200,200,600,400)
        self.setMinimumSize(850,550)
        self.setWindowTitle("PyDataExplorer")
        self.show()
        
    def add_data(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open csv/xlsx File", "./data", "Files (*.csv *.xlsx)")
        try:
            if file_path:
                if file_path.endswith(".csv"):  
                    self.data = pd.read_csv(file_path)
                    self.filterer_data = self.data.copy()
                else:
                    self.data = pd.read_excel(file_path)
                    self.filterer_data = self.data.copy()

            self.lb_4.setText(f'The data was loaded with {self.data.shape[0]} rows and {self.data.shape[1]} columns')
            self.update_change_type_menu() 
            self.update_null_handling_menu()
            self.update_defaut_table()
            self.update_description_menu()
        except Exception as e:
            self.lb_4.setText(f'error{e}')
            
    def update_defaut_table(self):
        if self.data is not None:
            self.table_widget.setRowCount(self.data.shape[0])
            self.table_widget.setColumnCount(self.data.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.data.columns)
            
            for row in range(self.data.shape[0]):
                for col in range(self.data.shape[1]):
                    item = QTableWidgetItem(str(self.data.iat[row, col]))
                    self.table_widget.setItem(row, col, item)
            self.lb_4.setText(f'The dataframe have {self.data.shape[0]} rows and {self.data.shape[1]} columns')
            self.filtered_data = self.data.copy()
        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            
    def update_filtered_table(self):
        if self.filtered_data is not None:
            self.table_widget.setRowCount(self.filtered_data.shape[0])
            self.table_widget.setColumnCount(self.filtered_data.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.filtered_data.columns)
            
            for row in range(self.filtered_data.shape[0]):
                for col in range(self.filtered_data.shape[1]):
                    item = QTableWidgetItem(str(self.filtered_data.iat[row, col]))
                    self.table_widget.setItem(row, col, item)
        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            
    def update_change_type_menu(self):
        self.change_type_menu.clear()
        if self.data is not None:
            for column in self.data.columns:
                action = QAction(column, self)
                action.triggered.connect(self.change_type)
                self.change_type_menu.addAction(action)
        else:
            self.change_type_menu.addAction("No Dataframe Loaded").setEnabled(False)
        
    def update_null_handling_menu(self):
        self.null_value_handling_menu.clear()
        if self.data is not None:
            for column in self.data.columns:
                action = QAction(column, self)
                action.triggered.connect(self.handle_null)
                self.null_value_handling_menu.addAction(action)
        else:
            self.null_value_handling_menu.addAction("No Dataframe Loaded").setEnabled(False)
        
    def update_description_menu(self):
        self.description_menu.clear()
        if self.data is not None:
            action_numeric = QAction('Numeric Columns', self)
            action_categoric = QAction('Categoric Columns', self)
            action_numeric.triggered.connect(self.show_numeric_describe)
            action_categoric.triggered.connect(self.show_numeric_describe)
            self.description_menu.addAction(action_numeric)
            self.description_menu.addAction(action_categoric)
        else:
            self.description_menu.addAction("No Dataframe Loaded").setEnabled(False)
                  
    def change_type(self):
        column = self.sender()
        if self.data is not None and column:
            col_name = column.text()
            current_type = str(self.data[col_name].dtype)

            dialog = QDialog(self)
            dialog.setWindowTitle(f"Change type of column {col_name}")
            dialog.setMinimumSize(300, 120)
            layout = QFormLayout()

            cb_type = QComboBox()
            cb_type.addItems(["str", "int", "float", "bool"])
            cb_type.setCurrentText(current_type)

            lb_bool = QLabel("True value:")
            lb_bool.setVisible(False)
            cb_bool = QComboBox()
            cb_bool.setVisible(False)

            lb_error = QLabel("")
            lb_error.setStyleSheet("color: red")

            def show_bool_combo():
                if cb_type.currentText() == "bool":
                    unique_values = self.data[col_name].dropna().unique()

                    if len(unique_values) > 2:
                        lb_error.setText("Erro: A coluna tem mais de 2 valores únicos")
                        cb_bool.setVisible(False)
                        lb_bool.setVisible(False)
                        return

                    cb_bool.clear()
                    cb_bool.addItems([str(v) for v in unique_values]) 
                    cb_bool.setVisible(True)
                    lb_bool.setVisible(True)
                    lb_error.clear()
                else:   
                    cb_bool.setVisible(False)
                    lb_bool.setVisible(False)
                    lb_error.clear()

            cb_type.currentTextChanged.connect(show_bool_combo)

            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")

            def apply_change():
                try:
                    new_type = cb_type.currentText()

                    if new_type == "bool":
                        unique_values = self.data[col_name].dropna().unique()
                        if len(unique_values) != 2:
                            raise ValueError("Coluna não pode ser convertida para booleano.")

                        true_value = cb_bool.currentText()
                        self.data[col_name] = self.data[col_name].map(lambda x: x == true_value)

                    else:
                        self.data[col_name] = self.data[col_name].astype(new_type)

                    self.lb_4.setText(f"Coluna '{col_name}' convertida para {new_type}")
                    self.update_defaut_table()
                    self.updateDrawerInfo()
                    dialog.accept()

                except Exception as e:
                    lb_error.setText(f"Erro: {e}")

            save_button.clicked.connect(apply_change)
            cancel_button.clicked.connect(dialog.reject)

            layout.addRow("Novo tipo:", cb_type)
            layout.addRow(lb_bool, cb_bool)
            layout.addRow(lb_error)
            layout.addRow(save_button, cancel_button)

            dialog.setLayout(layout)
            dialog.exec()

        else:
            self.lb_4.setText("Erro ao converter a coluna")
  
    def handle_null(self):
        column = self.sender()
        if self.data is not None and column:
            col_name = column.text()
            # current_type = str(self.data[col_name].dtype)
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"change type of the column {col_name}")
            dialog.setMinimumSize(300, 100)
            layout = QFormLayout()
            def show_method_combo():
                if null_handle_combo.currentText() == "interpolation":
                    cb_interpolate_method.setVisible(True)
                    lb_interpolate_method.setVisible(True)
                else:
                    cb_interpolate_method.setVisible(False)
                    lb_interpolate_method.setVisible(False)
                    
            lb_interpolate_method = QLabel("Interpolate Method:")
            cb_interpolate_method = QComboBox()
            cb_interpolate_method.addItems([
                'linear','time','pad','nearest','zero','slinear',
                'quadratic','cubic','barycentric','krogh','polynomial',
                'spline','piecewise_polynomial','pchip','akima','cubicspline'
            ])
            
            null_handle_combo = QComboBox()
            null_handle_combo.addItems(["fill whith mean value",
                                        "fill whith median value",
                                        "fill with 0",
                                        "delete null rows",
                                        "interpolation"
                                        ])
            null_handle_combo.currentIndexChanged.connect(show_method_combo)
            save_button = QPushButton("save")
            cancel_button = QPushButton("Cancel")
            show_method_combo()
            
            def apply_change():
                try:
                    cb_index = null_handle_combo.currentIndex()
                    if cb_index == 0:
                        self.data[col_name] = self.data[col_name].fillna(self.data[col_name].mean())
                    elif cb_index == 1:
                        self.data[col_name] = self.data[col_name].fillna(self.data[col_name].median())
                    elif cb_index == 2:
                        self.data[col_name] = self.data[col_name].fillna(0)
                    elif cb_index == 3:
                        self.data = self.data.dropna(subset=[col_name])
                    elif cb_index == 4:
                        self.data[col_name] = self.data[col_name].interpolate(method=cb_interpolate_method.currentText())
                        print(col_name,cb_interpolate_method.currentText())
                    self.lb_4.setText(f"Coluna '{col_name}' tratada")
                    self.update_defaut_table()
                    self.updateDrawerInfo()
                    dialog.accept()
                except Exception as e:
                    self.lb_4.setText(f"Um erro ocorreu durante a mudança: {e}")
                    dialog.reject()
            
            save_button.clicked.connect(apply_change)
            cancel_button.clicked.connect(dialog.reject)
            
            layout.addRow("Novo tipo:", null_handle_combo)
            layout.addRow(lb_interpolate_method, cb_interpolate_method)
            layout.addRow(save_button, cancel_button)
            dialog.setLayout(layout)
            dialog.exec()
        else:
            self.lb_4.setText("Erro ao converter a coluna")
    
    def filter_data(self):
        if self.data is not None:
            dialog = FilterDialog(self, self.data)
            if dialog.exec():
                self.filtered_data = dialog.filtered_data
                self.update_filtered_table()   
                self.lb_4.setText(f'The data filtered have {self.filtered_data.shape[0]} rows and {self.filtered_data.shape[1]} columns') 
        else:
            self.lb_4.setText("No dataframe loaded")
             
    def initDrawer(self):
        self.drawer = QDockWidget("Details", self)
        self.drawer.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        container = QWidget()
        layout = QVBoxLayout()

        self.drawer_text = QTextEdit()
        self.drawer_text.setReadOnly(True)

        self.btn_duplicate_show = QPushButton("Show Duplicates")
        self.btn_duplicate_show.clicked.connect(self.show_duplicate_rows)
        self.btn_duplicate_drop = QPushButton("Drop Duplicates")
        self.btn_duplicate_drop.clicked.connect(self.drop_duplicate_rows)

        layout.addWidget(self.drawer_text)
        layout.addWidget(self.btn_duplicate_show)
        layout.addWidget(self.btn_duplicate_drop)

        container.setLayout(layout)
        self.drawer.setWidget(container)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.drawer)
        self.drawer.hide()  

    def toggleDrawer(self):

        if self.drawer.isVisible():
            self.drawer.hide()
        else:
            self.updateDrawerInfo()
            self.drawer.show()

    def updateDrawerInfo(self):
        if self.data is not None:
            info_text = []

            buffer = io.StringIO()
            sys.stdout = buffer  
            self.data.info(verbose=True)
            sys.stdout = sys.__stdout__ 
            info_output = buffer.getvalue().split("\n") 

            filtered_info = []
            start_collecting = False  

            for line in info_output:
                if "---" in line:  
                    start_collecting = True
                if start_collecting:  
                    filtered_info.append(line)

            info_text.append("📌 DataFrame Info:\n")
            info_text.append("\n".join(filtered_info))

            info_text.append("\n Null Values:\n")
            info_text.append(str(self.data.isna().sum()))

            info_text.append("\n Duplicated Values:\n")
            info_text.append(str(self.data.duplicated().sum()))

            self.drawer_text.setPlainText("\n".join(info_text))
            if self.data.duplicated().sum() > 0:
                self.btn_duplicate_show.setVisible(True)
                self.btn_duplicate_drop.setVisible(True)
            else:
                self.btn_duplicate_show.setVisible(False)
                self.btn_duplicate_drop.setVisible(False)
            
        else:
            self.drawer_text.setPlainText("No Dataframe Loaded")
            self.btn_duplicate_show.setVisible(False)
            self.btn_duplicate_drop.setVisible(False)
            
    def open_graph_window(self):
       
        if self.data is not None:
            # self.graph_window = GraphView(self, self.data)  
            self.graph_window = DashboardView(self, self.data)
            self.graph_window.show()
        else:
            self.lb_4.setText("No data loaded")
            
    def show_duplicate_rows(self):
        if self.data is not None:
            try: 
                duplicated = self.data[self.data.duplicated(keep=False)].sort_values(by=self.data.columns.to_list()[0])
                self.filtered_data =  duplicated
                self.update_filtered_table()
                self.lb_4.setText(f'The data have {duplicated.shape[0]} rows')
            except Exception as e:
                self.lb_4.setText(f'error{e}') 
                
    def drop_duplicate_rows(self):
        if self.data is not None:
            try:
                self.data = self.data.drop_duplicates()
                self.lb_4.setText(f'Duplicated rows deleted')
                self.update_defaut_table() 
            except Exception as e:
                self.lb_4.setText(f'error{e}') 
                
    def show_numeric_describe(self):
        if self.data is not None:
            dialog = QDialog(self)
            table_describe = QTableWidget()
            layout = QHBoxLayout()
            dialog.setMinimumSize(800,300)
            
            def update_describe_table():
                if self.filtered_data is not None:
                    table_describe.setRowCount(self.filtered_data.shape[0])
                    table_describe.setColumnCount(self.filtered_data.shape[1])
                    table_describe.setHorizontalHeaderLabels(self.filtered_data.columns)

                    for row in range(self.filtered_data.shape[0]):
                        for col in range(self.filtered_data.shape[1]):
                            item = QTableWidgetItem(str(self.filtered_data.iat[row, col]))
                            table_describe.setItem(row, col, item)
                            
                else:
                    table_describe.setRowCount(0)
                    table_describe.setColumnCount(0)
            
            layout.addWidget(table_describe)
            dialog.setLayout(layout)
            self.filtered_data = self.data.describe().reset_index().rename(columns={"index": "Feature"})  
            update_describe_table()
            dialog.exec()
            self.lb_4.setText(f'Description')
        
    def show_numeric_describe(self):
        if self.data is not None:
            dialog = QDialog(self)
            table_describe = QTableWidget()
            cb_columns = QComboBox()
            list_unique = QListWidget()
            main_layout = QHBoxLayout()
            side_layout = QVBoxLayout()
            dialog.setMinimumSize(800,300)
            
            def update_describe_table():
                if self.filtered_data is not None:
                    table_describe.setRowCount(self.filtered_data.shape[0])
                    table_describe.setColumnCount(self.filtered_data.shape[1])
                    table_describe.setHorizontalHeaderLabels(self.filtered_data.columns)

                    for row in range(self.filtered_data.shape[0]):
                        for col in range(self.filtered_data.shape[1]):
                            item = QTableWidgetItem(str(self.filtered_data.iat[row, col]))
                            table_describe.setItem(row, col, item)
                            
                else:
                    table_describe.setRowCount(0)
                    table_describe.setColumnCount(0)
                    
            def updata_cb_column():
                cb_columns.clear()
                for col in self.data.select_dtypes(include=['object']).columns:
                    cb_columns.addItem(col)
            
            def list_unique_values():
                list_unique.clear()
                for value in self.data[cb_columns.currentText()].unique():
                    list_unique.addItem(value)
                
            updata_cb_column()
            list_unique_values()    
            cb_columns.currentIndexChanged.connect(list_unique_values)
            side_layout.addWidget(cb_columns)   
            side_layout.addWidget(list_unique)  
            main_layout.addWidget(table_describe,4)
            main_layout.addLayout(side_layout,1)
            dialog.setLayout(main_layout)
            self.filtered_data = self.data.describe(include=[object]).reset_index().rename(columns={"index": "Feature"})  
            update_describe_table()
            dialog.exec()
            self.lb_4.setText(f'Description')
            
    def groupby_dialog(self):
        if self.data is not None:
            dialog = GroupByDialog(self.filtered_data, self)
            dialog.exec()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = Main_window()
    sys.exit(app.exec())