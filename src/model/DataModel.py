from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier 
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

import time
import pandas as pd
import io
import sys

class DataModel:
    """
    A class to manage data operations such as loading,
    filtering, transforming, and maintaining a history of changes.
    """
    def __init__(self):
        """
        Initializes the DataModel with default attributes.
        """
        self.data = None
        self.filtered_data = None
        self.selected_columns = []
        self.history = []  
        self.max_history = 10

    def load_data(self, file_path):
        """
        Loads data from a CSV or Excel file into the DataFrame.

        :param file_path: Path to the file to be loaded.
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        if not file_path:
            return False, "File path is empty."
        if self.data is not None: 
            self._save_diff("load_data", {})
        try:
            if file_path.endswith(".csv"):
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)
            self.filtered_data = self.data.copy()
            self.selected_columns = self.data.columns.tolist()
            return True, f"Data loaded: {self.data.shape[0]} rows, {self.data.shape[1]} columns"
        except Exception as e:
            return False, f"Error: {e}"

    def apply_filter(self, query_string, selected_columns):
        """
        Applies a filter to the data based on a query string and selected columns.

        :param query_string: Query string to filter the data.
        :param selected_columns: List of columns to keep after filtering.
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        try:
            if query_string:
                self.filtered_data = self.data.query(query_string)
            else:
                self.filtered_data = self.data.copy()
            self.filtered_data = self.filtered_data[selected_columns]
            self.selected_columns = selected_columns
            return True, f"Filter applied: {self.filtered_data.shape[0]} rows, {self.filtered_data.shape[1]} columns"
        except Exception as e:
            return False, f"Error applying filter: {e}"

    def change_type(self, column, new_type, true_value=None):
        """
        Changes the data type of a specified column.

        :param column: Name of the column to change.
        :param new_type: New data type (e.g., 'bool', 'date', 'int').
        :param true_value: Value to consider as True (only for boolean conversion).
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        original_values = self.data[column].copy()
        self._save_diff("change_type", {"column": column, "original_values": original_values})
        try:
            if new_type == "bool":
                if len(self.data[column].dropna().unique()) != 2:
                    raise ValueError("Column cannot be converted to boolean.")
                self.data[column] = self.data[column].map(lambda x: x == true_value)
            elif new_type == "date":
                self.data[column] = pd.to_datetime(self.data[column])
            else:
                self.data[column] = self.data[column].astype(new_type)
            self.filtered_data = self.data.copy()
            return True, f"Column '{column}' converted to {new_type}"
        except Exception as e:
            return False, f"Error: {e}"

    def handle_null(self, column, method, interpolate_method=None):
        """
        Handles null values in a specified column using a specified method.

        :param column: Name of the column to process.
        :param method: Method to handle nulls ('mean', 'median', 'zero', 'drop', 'interpolate').
        :param interpolate_method: Interpolation method (only for 'interpolate' method).
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        original_values = self.data[column].copy()
        self._save_diff("handle_null", {"column": column, "original_values": original_values})
        try:
            if method == "mean":
                self.data[column] = self.data[column].fillna(round(self.data[column].mean(),2))
            elif method == "median":
                self.data[column] = self.data[column].fillna(self.data[column].median())
            elif method == "zero":
                self.data[column] = self.data[column].fillna(0)
            elif method == "drop":
                self.data = self.data.dropna(subset=[column])
            elif method == "interpolate":
                self.data[column] = self.data[column].interpolate(method=interpolate_method)
            self.filtered_data = self.data.copy()
            return True, f"Column '{column}' processed"
        except Exception as e:
            return False, f"Error: {e}"

    def get_columns(self):
        """
        Returns a list of columns in the DataFrame.

        :return: List of column names.
        """
        return self.data.columns.tolist() if self.data is not None else []
    
    def get_dtype(self, column):
        """
        Returns the data type of a specified column.

        :param column: Name of the column.
        :return: Data type of the column as a string.
        """
        return str(self.data[column].dtype) if self.data is not None else None

    def get_shape(self):
        """
        Returns the shape of the DataFrame.

        :return: Tuple (rows, columns) representing the shape of the DataFrame.
        """
        return self.data.shape if self.data is not None else (0, 0)

    def get_info(self):
        """
        Returns general information about the DataFrame, including null and duplicate counts.

        :return: String containing DataFrame information.
        """
        if self.data is not None:
            buffer = io.StringIO()
            sys.stdout = buffer
            self.data.info(verbose=True)
            sys.stdout = sys.__stdout__
            info = buffer.getvalue()
            nulls = str(self.data.isna().sum())
            duplicates = str(self.data.duplicated().sum())
            return f"📌 DataFrame Info:\n{info}\nNull Values:\n{nulls}\nDuplicated Values:\n{duplicates}"
        return "No Dataframe Loaded"

    def drop_duplicates(self):
        """
        Removes duplicate rows from the DataFrame.

        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        if self.data is not None:
            duplicates = self.data[self.data.duplicated(keep=False)].copy()
            self._save_diff("drop_duplicates", {"removed_rows": duplicates})
            self.data = self.data.drop_duplicates()
            self.filtered_data = self.data.copy()
            return True, "Duplicated rows deleted"
        return False, "No data loaded"

    def get_duplicates(self):
        """
        Returns a DataFrame containing duplicate rows.

        :return: DataFrame with duplicate rows.
        """
        if self.data is not None:
            return self.data[self.data.duplicated(keep=False)].sort_values(by=self.data.columns[0])
        return None

    def describe_numeric(self):
        """
        Returns descriptive statistics for numeric columns.

        :return: DataFrame with descriptive statistics.
        """
        if self.data is not None:
            return self.data.describe().reset_index().rename(columns={"index": "Feature"})
        return None

    def describe_categorical(self):
        """
        Returns descriptive statistics for categorical columns.

        :return: DataFrame with descriptive statistics.
        """
        if self.data is not None:
            return self.data.describe(include=[object]).reset_index().rename(columns={"index": "Feature"})
        return None

    def get_categorical_columns(self):
        """
        Returns a list of categorical columns.

        :return: List of categorical column names.
        """
        if self.data is not None:
            return self.data.select_dtypes(include=['object']).columns.tolist()
        return []

    def get_unique_values(self, column):
        """
        Returns a list of unique values in a specified column.

        :param column: Name of the column.
        :return: List of unique values.
        """
        if self.data is not None:
            return self.data[column].unique().tolist()
        return []
    
    def group_df(self,group_column, x_column, agg_func):
        """
        Groups the DataFrame by a column and applies an aggregation function.

        :param group_column: Column to group by.
        :param x_column: Column to apply the aggregation function.
        :param agg_func: Aggregation function ('sum', 'mean', 'min', 'max').
        :return: DataFrame with grouped and aggregated data.
        """
        if agg_func == 'sum':
            return self.filtered_data.groupby(group_column)[x_column].sum().reset_index()
        elif agg_func == 'mean':
            return self.filtered_data.groupby(group_column)[x_column].mean().reset_index()
        elif agg_func == 'min':
            return self.filtered_data.groupby(group_column)[x_column].min().reset_index()
        elif agg_func == 'max':
            return self.filtered_data.groupby(group_column)[x_column].max().reset_index()
       
    def create_column(self, name):
        """
        Creates a new column in the DataFrame.

        :param name: Name of the new column.
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        if self.data is not None:
            self._save_diff("create_column",{"column":name})
            try:
                self.data[name] = '0'
                return True
            except Exception as e:
                return False
    
    def replace_values(self, column, old_value, new_value):
        """
        Replaces specific values in a column with new values.

        :param column: Name of the column.
        :param old_value: Value to be replaced.
        :param new_value: New value to replace the old value.
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        if self.data is not None:
            original_values = self.data[column].copy()
            self._save_diff("replace_values", {"column": column, "original_values": original_values})
            try:
                self.data.loc[self.data[column] == old_value, column] = new_value
                return [True ,None]
            except Exception as e:
                return [False ,e]
    
    def update_values_by_condition(self,condition_column,target_column,operator,condition_value,new_value):
        """
        Updates values in a column based on a condition.

        :param condition_column: Column to evaluate the condition.
        :param target_column: Column to update.
        :param operator: Condition operator ('<', '>', '<=', '>=', '==', '!=').
        :param condition_value: Value to compare against.
        :param new_value: New value to set if the condition is met.
        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        if self.data is not None:
            original_values = self.data[target_column].copy()
            self._save_diff("replace_by_condition", {"column": target_column, "original_values": original_values})
            try:
                if operator == '<':
                    self.data.loc[self.data[condition_column] < condition_value, target_column] = new_value
                elif operator == '>':
                    self.data.loc[self.data[condition_column] > condition_value, target_column] = new_value
                elif operator == '<=':
                    self.data.loc[self.data[condition_column] <= condition_value, target_column] = new_value
                elif operator == '>=':
                    self.data.loc[self.data[condition_column] >= condition_value, target_column] = new_value
                elif operator == '==':
                    self.data.loc[self.data[condition_column] == condition_value, target_column] = new_value
                elif operator == '!=':
                    self.data.loc[self.data[condition_column] != condition_value, target_column] = new_value
            
                return [True ,None]
            except Exception as e:
                return [False ,e]  
    
    def _save_diff(self, operation, details):
        """
        Saves a change to the history for undo functionality.

        :param operation: Name of the operation.
        :param details: Details of the operation.
        """
        if len(self.history) >= self.max_history:
            self.history.pop(0)  
        self.history.append({"operation": operation, "details": details})
        
    def undo(self):
        """
        Reverts the last operation performed.

        :return: A tuple (success: bool, message: str) indicating the result of the operation.
        """
        if not self.history:
            return False, "No actions to undo"
        
        last_action = self.history.pop()
        operation = last_action["operation"]
        details = last_action["details"]

        if operation == "load_data":
            self.data = None
            self.filtered_data = None
            self.selected_columns = []
            
        elif (operation == "change_type" or operation == "handle_null" or
            operation == "replace_values" or operation == "replace_by_condition"):
            column = details["column"]
            original_values = details["original_values"]
            self.data[column] = original_values
            self.filtered_data = self.data.copy()
            
        elif operation == "drop_duplicates":
            removed_rows = details["removed_rows"]
            self.data = pd.concat([self.data, removed_rows]).sort_index()
            self.filtered_data = self.data.copy()
            
        elif operation == "create_column":
            column_created = details["column"]
            self.data.drop(columns=column_created,inplace=True)
            self.filtered_data = self.data.copy()
            

        return True, f"Undone {operation}"