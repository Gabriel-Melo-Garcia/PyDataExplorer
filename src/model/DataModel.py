import pandas as pd
import io
import sys

class DataModel:
    def __init__(self):
        self.data = None
        self.filtered_data = None
        self.selected_columns = []

    def load_data(self, file_path):
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
        return self.data.columns.tolist() if self.data is not None else []
    
    def get_dtype(self, column):
        return str(self.data[column].dtype) if self.data is not None else None

    def get_shape(self):
        return self.data.shape if self.data is not None else (0, 0)

    def get_info(self):
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
        if self.data is not None:
            self.data = self.data.drop_duplicates()
            self.filtered_data = self.data.copy()
            return True, "Duplicated rows deleted"
        return False, "No data loaded"

    def get_duplicates(self):
        if self.data is not None:
            return self.data[self.data.duplicated(keep=False)].sort_values(by=self.data.columns[0])
        return None

    def describe_numeric(self):
        if self.data is not None:
            return self.data.describe().reset_index().rename(columns={"index": "Feature"})
        return None

    def describe_categorical(self):
        if self.data is not None:
            return self.data.describe(include=[object]).reset_index().rename(columns={"index": "Feature"})
        return None

    def get_categorical_columns(self):
        if self.data is not None:
            return self.data.select_dtypes(include=['object']).columns.tolist()
        return []

    def get_unique_values(self, column):
        if self.data is not None:
            return self.data[column].unique().tolist()
        return []
    
    def group_df(self,group_column, x_column, agg_func):
        
        if agg_func == 'sum':
            return self.filtered_data.groupby(group_column)[x_column].sum().reset_index()
        elif agg_func == 'mean':
            return self.filtered_data.groupby(group_column)[x_column].mean().reset_index()
        elif agg_func == 'min':
            return self.filtered_data.groupby(group_column)[x_column].sum().reset_index()
        elif agg_func == 'max':
            return self.filtered_data.groupby(group_column)[x_column].mean().reset_index()
       
       