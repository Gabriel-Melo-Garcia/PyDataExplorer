from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier 
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pandas as pd
import time

class ClassificationModel:
    def __init__(self):
        
        # classification_names = ["Logistic Regression","Random Forest","SVM","XGBoost","KNN","All"]
        self.data = None
        self.models = {}  
        self.scaler = StandardScaler()  
        
    def pre_process_features(self,features):
        
        if self.data is not None:
        
            x = self.data[features]

            numeric_cols = x.select_dtypes(include=['int64', 'float64']).columns
            categorical_cols = x.select_dtypes(include=['object']).columns

            if numeric_cols.any():
                x_numeric = pd.DataFrame(self.scaler.fit_transform(x[numeric_cols]), columns=numeric_cols)
            else:
                x_numeric = pd.DataFrame()

            if categorical_cols.any():
                x_categorical = pd.get_dummies(x[categorical_cols], drop_first=True)
            else:
                x_categorical = pd.DataFrame()

            x_processed = pd.concat([x_numeric, x_categorical], axis=1)
            
            
            return True, x_processed
        
        else:
            return False, None
    
    def train_model(self, data, features, target, model_name):
        
        self.data = data
        
        if self.data is None:
            
            return False , "No data loaded"
        
        process_status, x_processed = self.pre_process_features(features)
        y = self.data[target]
        
        if not process_status :
            return False , "faild to process features"
        
        try:
            x_train, x_test, y_train, y_test = train_test_split(x_processed, y, test_size=0.2, random_state=42)
        except Exception as e:
            return False , f"error{e}"
        
        model_dict = {
            "Logistic Regression": LogisticRegression(),
            "Random Forest": RandomForestClassifier(),
            "SVM": SVC(),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
            "KNN": KNeighborsClassifier()
        }
        
        models_to_run = model_dict.keys() if model_name == "All" else [model_name]

        for name in models_to_run:
            model = model_dict[name]
            start_time = time.time()
            model.fit(x_train, y_train)
            train_time = time.time() - start_time
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)

            self.models[name] = {
                "model": model,
                "features": features,
                "target": target,
                "scaler": self.scaler,
                "accuracy": accuracy,
                "time": train_time
            }
        
        # print('modelos sendo processado', self.models)
        # print('-'*10)

        return True, "Models trained successfully"
    
        