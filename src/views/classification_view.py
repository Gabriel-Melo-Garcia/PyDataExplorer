from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QCheckBox, QPushButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QLineEdit, QWidget, QMenuBar, QApplication
)
from PyQt6.QtCore import pyqtSignal

class ClassificationView(QDialog):
    
    train_models_signal = pyqtSignal(list, str, str)  
    predict_signal = pyqtSignal(dict)  
    save_model_signal = pyqtSignal()
    load_model_signal = pyqtSignal()

    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.columns = columns 
        self.setWindowTitle("Classification Model Explorer")
        self.setMinimumSize(600, 400)
        self.init_ui()

    def init_ui(self):
        
        main_layout = QVBoxLayout()

        # Menubar
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("File")
        save_action = file_menu.addAction("Save Model")
        load_action = file_menu.addAction("Load Model")
        save_action.triggered.connect(self.save_model_signal.emit)
        load_action.triggered.connect(self.load_model_signal.emit)
        main_layout.addWidget(menubar)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # tab 1: model configuration
        self.setup_tab = QWidget()
        setup_layout = QVBoxLayout()

        # Combobox for target column
        target_layout = QHBoxLayout()
        target_label = QLabel("Target Column:")
        self.target_combobox = QComboBox()
        self.target_combobox.addItems(self.columns)
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_combobox)
        setup_layout.addLayout(target_layout)

        # List fot features
        features_label = QLabel("Select Features:")
        setup_layout.addWidget(features_label)
        self.feature_checkboxes = {}
        for column in self.columns:
            checkbox = QCheckBox(column)
            self.feature_checkboxes[column] = checkbox
            setup_layout.addWidget(checkbox)

        # Combobox for model
        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_combobox = QComboBox()
        self.model_combobox.addItems(["All", "Logistic Regression", "Random Forest", "SVM", "XGBoost", "KNN"])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combobox)
        setup_layout.addLayout(model_layout)

        # btn training
        self.btn_train = QPushButton("Train Model(s)")
        self.btn_train.clicked.connect(self.train_models)
        setup_layout.addWidget(self.btn_train)
        setup_layout.addStretch()

        self.setup_tab.setLayout(setup_layout)
        self.tabs.addTab(self.setup_tab, "Model Setup")

        # Aba 2: Resultados
        self.results_tab = QWidget()
        results_layout = QVBoxLayout()
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Model", "Accuracy", "Training Time (s)"])
        results_layout.addWidget(self.results_table)
        self.results_tab.setLayout(results_layout)
        self.tabs.addTab(self.results_tab, "Results")

        # Aba 3: Predição
        self.predict_tab = QWidget()
        predict_layout = QVBoxLayout()
        
        # Campos para entrada de valores
        self.predict_inputs = {}
        predict_label = QLabel("Enter Feature Values:")
        predict_layout.addWidget(predict_label)
        for column in self.columns:
            input_layout = QHBoxLayout()
            label = QLabel(column + ":")
            line_edit = QLineEdit()
            self.predict_inputs[column] = line_edit
            input_layout.addWidget(label)
            input_layout.addWidget(line_edit)
            predict_layout.addLayout(input_layout)

        # Botão para predizer
        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.make_prediction)
        predict_layout.addWidget(self.predict_button)

        # Resultado da predição
        self.predict_result = QLabel("Prediction: N/A")
        predict_layout.addWidget(self.predict_result)
        predict_layout.addStretch()

        self.predict_tab.setLayout(predict_layout)
        self.tabs.addTab(self.predict_tab, "Prediction")

        # Definir layout principal
        self.setLayout(main_layout)

    def train_models(self):
        """Emite sinal para treinar os modelos selecionados."""
        selected_features = [col for col, cb in self.feature_checkboxes.items() if cb.isChecked()]
        target = self.target_combobox.currentText()
        model = self.model_combobox.currentText()
        
        if not selected_features or not target:
            return  # Pode adicionar um aviso na UI se desejar
        
        self.train_models_signal.emit(selected_features, target, model)

    def update_results(self, results):
        """Atualiza a aba de resultados com os dados dos modelos."""
        self.results_table.setRowCount(len(results))
        for row, (model_name, metrics) in enumerate(results.items()):
            self.results_table.setItem(row, 0, QTableWidgetItem(model_name))
            self.results_table.setItem(row, 1, QTableWidgetItem(f"{metrics['accuracy']:.4f}"))
            self.results_table.setItem(row, 2, QTableWidgetItem(f"{metrics['time']:.2f}"))

    def make_prediction(self):
        """Emite sinal para fazer uma predição com os valores inseridos."""
        input_values = {}
        for column, line_edit in self.predict_inputs.items():
            value = line_edit.text().strip()
            if value:  # Só inclui se o campo não estiver vazio
                input_values[column] = value
        if input_values:
            self.predict_signal.emit(input_values)

    def update_prediction(self, prediction):
        """Atualiza o resultado da predição na aba correspondente."""
        self.predict_result.setText(f"Prediction: {prediction}")
    
if __name__ == '__main__':
    
    app = QApplication([])
    columns = ['abc','def','ghi','jkl','xyz']
    classification = ClassificationView(columns)
    classification.show()
    app.exec()
    
