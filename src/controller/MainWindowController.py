from src.views.DialogChangeTypeView import ChangeTypeView
from src.views.HandleNullView import HandleNullView
from src.views.FilterView import FilterView
from src.views.GraphView import GraphView

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.filter_view = None
        self.graph_view = None  
        self.connect_signals()

    def connect_signals(self):
        self.view.load_data_signal.connect(self.load_data)
        self.view.clean_filter_signal.connect(self.clean_filter)
        self.view.filter_data_signal.connect(self.open_filter_dialog)
        self.view.open_graph_view_signal.connect(self.open_graph_view)
        self.view.show_duplicates_signal.connect(self.show_duplicates)
        self.view.drop_duplicates_signal.connect(self.drop_duplicates)
        self.view.describe_numeric_signal.connect(self.describe_numeric)
        self.view.describe_categorical_signal.connect(self.describe_categorical)
        self.view.open_change_type_dialog_signal.connect(self.open_change_type_dialog)
        self.view.open_handle_null_dialog_signal.connect(self.open_handle_null_dialog)

    def load_data(self, file_path):
        success, message = self.model.load_data(file_path)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.view.update_menus(self.model.get_columns())
            self.update_drawer()

    def open_change_type_dialog(self, column):
        self.dialog = ChangeTypeView(column, self.view)
        self.dialog.bool_value_selector_signal.connect(self.update_cb_bool_type)
        self.dialog.apply_change_signal.connect(self.change_type)
        self.dialog.exec()

    def change_type(self, column, new_type, true_value):
        success, message = self.model.change_type(column, new_type, true_value)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.update_drawer()
    
    def update_cb_bool_type(self):
        if self.model.data is not None:
            values = self.model.get_unique_values(self.dialog.column)
            self.dialog.set_unique_values(values)

    def open_handle_null_dialog(self, column):
        dialog = HandleNullView(column, self.view)
        dialog.apply_null_handling_signal.connect(self.handle_null)
        dialog.exec()

    def handle_null(self, column, method, interpolate_method):
        success, message = self.model.handle_null(column, method, interpolate_method)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.update_drawer()

    def open_filter_dialog(self):
        if self.model.data is not None:
            self.filter_view = FilterView(self.model.get_columns(), self.view)  # Armazena a instância
            self.filter_view.add_condition_signal.connect(self.handle_add_condition)
            self.filter_view.apply_filter_signal.connect(self.apply_filter)
            self.filter_view.select_columns_signal.connect(self.show_column_selection)
            self.filter_view.column_changed_signal.connect(self.update_filter_actions)
            self.update_filter_actions(self.filter_view.cb_column.currentText())  # Atualiza ações iniciais
            self.filter_view.exec()
            self.filter_view = None  # Limpa a referência após fechar o diálogo
        else:
            self.view.update_status("No dataframe loaded")

    def handle_add_condition(self, column, action, value):
        data_type = self.model.get_dtype(column)
        if data_type in ['int64', 'float64']:
            try:
                value = float(value) if '.' in value else int(value)
                condition_text = f"{column} {action} {value}"
            except ValueError:
                return  # Pode adicionar feedback de erro na View se desejar
        else:
            condition_text = f"{column} {action} '{value}'"
        if self.filter_view:
            self.filter_view.add_condition_to_list(condition_text)

    def apply_filter(self, conditions, selected_columns):
        query_string = " and ".join(conditions) if conditions else ""
        success, message = self.model.apply_filter(query_string, selected_columns)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.filtered_data)

    def show_column_selection(self):
        if self.filter_view:
            self.filter_view.show_column_selection(self.model.get_columns(), self.filter_view.selected_columns)
            
    def update_filter_actions(self, column):
        if self.filter_view:  # Usa a instância armazenada
            data_type = self.model.get_dtype(column)
            if data_type in ['int64', 'float64']:
                actions = ['==', '!=', '<', '>', '<=', '>=']
            else:
                actions = ['==', '!=']
            self.filter_view.set_action_items(actions)

    def clean_filter(self):
        self.model.filtered_data = self.model.data.copy()
        self.model.selected_columns = self.model.get_columns()
        self.view.update_table(self.model.data)
        self.view.update_status(f"Filter cleared: {self.model.get_shape()[0]} rows, {self.model.get_shape()[1]} columns")

    def show_duplicates(self):
        duplicates = self.model.get_duplicates()
        if duplicates is not None:
            self.view.update_table(duplicates)
            self.view.update_status(f"Showing {duplicates.shape[0]} duplicate rows")

    def drop_duplicates(self):
        success, message = self.model.drop_duplicates()
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.update_drawer()

    def describe_numeric(self):
        desc = self.model.describe_numeric()
        if desc is not None:
            self.view.update_table(desc)
            self.view.update_status("Numeric description")

    def describe_categorical(self):
        desc = self.model.describe_categorical()
        if desc is not None:
            self.view.update_table(desc)
            self.view.update_status("Categorical description")

    def update_drawer(self):
        info = self.model.get_info()
        has_duplicates = self.model.data.duplicated().sum() > 0 if self.model.data is not None else False
        self.view.update_drawer(info, has_duplicates)
        
    def open_graph_view(self):
        if self.model.data is not None:
            self.graph = GraphView(self.model.get_columns(), self.view)
            self.graph.show()   
        else:
            self.view.update_status("No data loaded")