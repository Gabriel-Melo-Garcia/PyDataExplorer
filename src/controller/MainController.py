from src.views.ChangeTypeView import ChangeTypeView
from src.views.HandleNullView import HandleNullView
from src.views.FilterView import FilterView
from src.views.GraphView import GraphView
from src.views.MapValuesView import MapValuesView
from src.views.ClassificationView import ClassificationView
from src.workers.ClassificationWorker import ClassificationWorker
from PyQt6.QtWidgets import QFileDialog
import plotly.express as px
import pandas as pd
import joblib

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.filter_view = None
        self.change_type_dialog = None 
        self.handle_null_dialog = None
        self.graph = None  
        self.map_view = None
        self.classification_view = None
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
        self.view.open_map_values_view_signal.connect(self.open_map_values_view)
        self.view.undo_signal.connect(self.undo_action)
        self.view.open_classification_view_signal.connect(self.open_classification_view)
        self.view.save_dataframe_signal.connect(self.save_dataframe)

    def load_data(self, file_path):
        success, message = self.model.load_data(file_path)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.view.update_menus(self.model.get_columns())
            self.update_drawer()

    def open_change_type_dialog(self, column):
        self.change_type_dialog = ChangeTypeView(column, self.view)
        self.change_type_dialog.bool_value_selector_signal.connect(self.update_cb_bool_type)
        self.change_type_dialog.apply_change_signal.connect(self.change_type)
        self.change_type_dialog.finished.connect(self.clear_change_type_dialog)
        self.change_type_dialog.exec()

    def change_type(self, column, new_type, true_value):
        success, message = self.model.change_type(column, new_type, true_value)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.update_drawer()
    
    def update_cb_bool_type(self):
        if self.model.data is not None:
            values = self.model.get_unique_values(self.change_type_dialog.column)
            self.change_type_dialog.set_unique_values(values)

    def clear_change_type_dialog(self):
        self.change_type_dialog = None

    def open_handle_null_dialog(self, column):
        self.handle_null_dialog = HandleNullView(column, self.view)
        self.handle_null_dialog.apply_null_handling_signal.connect(self.handle_null)
        self.handle_null_dialog.finished.connect(self.clear_handle_null_dialog)
        self.handle_null_dialog.exec()

    def handle_null(self, column, method, interpolate_method):
        success, message = self.model.handle_null(column, method, interpolate_method)
        self.view.update_status(message)
        if success:
            self.view.update_table(self.model.data)
            self.update_drawer()
    
    def clear_handle_null_dialog(self):
        self.handle_null_dialog = None

    def open_filter_dialog(self):
        if self.model.data is not None:
            self.filter_view = FilterView(self.model.get_columns(), self.view)  
            self.filter_view.add_condition_signal.connect(self.handle_add_condition)
            self.filter_view.apply_filter_signal.connect(self.apply_filter)
            self.filter_view.select_columns_signal.connect(self.show_column_selection)
            self.filter_view.column_changed_signal.connect(self.update_filter_actions)
            self.update_filter_actions(self.filter_view.cb_column.currentText())  
            self.filter_view.exec()
            self.filter_view = None  
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
            self.graph.standard_graph_signal.connect(self.update_standard_graph)
            self.graph.grouped_graph_signal.connect(self.update_grouped_graph)
            self.graph.show()   
        else:
            self.view.update_status("No data loaded")
    
    def update_standard_graph(self, graph, x_column, y_column):
        
        if self.graph is not None:
            try:
                df = self.model.filtered_data
                if graph == 'Scatter':
                    fig = px.scatter(df, x = x_column , y = y_column)

                elif graph == 'Bar':
                    fig = px.bar(df, x = x_column , y = y_column)

                elif graph == 'Line':
                    fig = px.line(df, x = x_column , y = y_column)

                elif graph == 'Histogram':
                    fig = px.histogram(df, x = x_column)
                
                html_content = fig.to_html(include_plotlyjs='cdn')
                self.graph.display_graph(html_content)

            except Exception as e:
                self.view.update_status(f"Error generating graph: {e}")

    def update_grouped_graph(self,group_column, y_column, agg_func ):
        
        if self.graph is not None:
            try:
                df = self.model.group_df(group_column, y_column, agg_func)
                fig = px.bar(df, x=group_column, y=y_column,)
                html_content = fig.to_html(include_plotlyjs='cdn')
                self.graph.display_graph(html_content)
                
            except Exception as e:

                self.view.update_status(f"Error generating grouped graph: {e}")
    
    def open_map_values_view(self):
        if self.model.data is not None:
            columns = self.model.get_columns()
            self.map_view = MapValuesView(columns)
            self.map_view.create_column_signal.connect(self.creat_column)
            self.map_view.replace_values_signal.connect(self.replace_values)
            self.map_view.update_values_by_condition_signal.connect(self.update_values_by_condition)
            self.map_view.show()
        else:
            self.view.update_status("No data loaded")
            
    def creat_column(self,name):
        if self.model.create_column(name):         
            self.view.update_status('column created')
            self.view.update_table(self.model.data)
            columns = self.model.get_columns()
            self.map_view.update_columns_cb(columns)
            
    def replace_values(self, column, old_value, new_value):
        
        if old_value and new_value:
            old_value = self.normalize_value_type(column,old_value)
            new_value = self.normalize_value_type(column,new_value)

            reponse_status, error = self.model.replace_values(column, old_value, new_value)
            # print(reponse_status)
            if reponse_status:
                self.view.update_status('value replaced')
                self.view.update_table(self.model.data)
            else:
                self.view.update_status(f"error: {error}")
           
    def update_values_by_condition(self,condition_column,target_column,operator,condition_value,new_value):
        
        if condition_value and new_value:
            condition_value = self.normalize_value_type(condition_column,condition_value)
            new_value = self.normalize_value_type(target_column,new_value)

            reponse_status, error = self.model.update_values_by_condition(condition_column,target_column,operator,condition_value,new_value)
            if reponse_status:
                self.view.update_status('value updated')
                self.view.update_table(self.model.data)
            else:
                self.view.update_status(f"error: {error}")
            
    def normalize_value_type(self, column, value):
        column_type = self.model.get_dtype(column)
        try:
            if column_type == 'int64':
                return int(value)
            elif column_type == 'float64':
                return float(value)
            elif column_type == 'object':
                return str(value)
            elif column_type == 'bool':
                return value.lower() in ('true', '1', 'yes')
            elif column_type == 'datetime64[ns]':
                return pd.to_datetime(value)
            else:
                raise ValueError(f"Unsupported column type: {column_type}")
        except Exception as e:
            self.view.update_status(f"Error normalizing value for {column}: {e}")
            return value
        
    def update_ui(self, data=None, message=None):
        if data is not None:
            self.view.update_table(data)
        if message:
            self.view.update_status(message)
        self.update_drawer()
    
    def undo_action(self):
        success, message = self.model.undo()
        self.view.update_status(message)
        if success:
            self.update_ui(self.model.data , message)
            self.update_drawer()
            
    def save_dataframe(self):
        
        """Abre um QFileDialog para salvar o DataFrame e executa a ação."""
        
        if self.model.data is None:
            self.view.update_status("No DataFrame to save")
            return

        # Abre o QFileDialog para salvar
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self.view, 
            "Save DataFrame", 
            "./data", 
            "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                if selected_filter == "CSV Files (*.csv)":
                    if not file_path.endswith(".csv"):
                        file_path += ".csv"
                    self.model.data.to_csv(file_path, index=False)
                elif selected_filter == "Excel Files (*.xlsx)":
                    if not file_path.endswith(".xlsx"):
                        file_path += ".xlsx"
                    self.model.data.to_excel(file_path, index=False)
                self.view.update_status(f"DataFrame saved to {file_path}")
            except Exception as e:
                self.view.update_status(f"Error saving DataFrame: {e}")
    
    def open_classification_view(self):
        if self.model.data is not None:
            self.classification_view = ClassificationView(self.model.get_columns(), self.view)
            self.classification_view.train_models_signal.connect(self.train_classification_models)
            self.classification_view.predict_signal.connect(self.predict_with_model)
            self.classification_view.save_model_signal.connect(self.save_model)
            self.classification_view.load_model_signal.connect(self.load_model)
            self.classification_view.finished.connect(self.clear_classification_view)
            self.classification_view.exec()
        else:
            self.view.update_status("No data loaded")
            
    def train_classification_models(self, features, target, model):
        
        worker = ClassificationWorker(self.model, features, target, model)
        self.classification_view.show_loading()  
        worker.finished.connect(lambda success, message, results: self._on_training_finished(success, message, results, worker))
        worker.start()
    
    def _on_training_finished(self, success, message, results, worker):
        self.classification_view.hide_loading() 
        self.view.update_status(message)
        if success:
            self.classification_view.update_results(results)
        worker.deleteLater()
            

    def predict_with_model(self, input_values):
        # Assume que o último modelo treinado será usado, ou adicione um combobox para escolher
        model_name = list(self.model.models.keys())[0] if self.model.models else None
        if model_name:
            success, message, prediction = self.model.predict_with_model(model_name, input_values)
            self.view.update_status(message)
            if success:
                self.classification_view.update_prediction(prediction)

    def save_model(self):
        if not self.model.models:
            self.view.update_status("No models to save")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Save Model", "./models", "Joblib Files (*.joblib)"
        )
        if file_path:
            if not file_path.endswith(".joblib"):
                file_path += ".joblib"
            try:
                joblib.dump(self.model.models, file_path)
                self.view.update_status(f"Models saved to {file_path}")
            except Exception as e:
                self.view.update_status(f"Error saving models: {e}")

    def load_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Load Model", "./models", "Joblib Files (*.joblib)"
        )
        if file_path:
            try:
                self.model.models = joblib.load(file_path)
                self.view.update_status(f"Models loaded from {file_path}")
                # Atualizar a aba de predição com as colunas do modelo carregado
                if self.model.models:
                    first_model = list(self.model.models.keys())[0]
                    features = self.model.models[first_model]["features"]
                    self.classification_view.update_prediction_fields(features)
            except Exception as e:
                self.view.update_status(f"Error loading models: {e}")

    def clear_classification_view(self):
        self.classification_view = None