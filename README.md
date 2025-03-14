PyDataExplorer is an interactive desktop application built with PyQt6 and pandas, designed for data cleaning, exploration, visualization, and predictive modeling. It provides a user-friendly interface for data analysts to preprocess datasets, visualize insights, and train classification models efficiently.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)

## Features
- **Data Cleaning and Preprocessing**: Filter data, handle missing values, convert column types, and remove duplicates with an intuitive GUI.
- **Data Visualization**: Generate interactive graphs and charts using Plotly.
- **Predictive Modeling**: Train multiple classification models (e.g., Logistic Regression, Random Forest, SVM, XGBoost, KNN) with scikit-learn, supporting parallel execution via QThread.
- **Undo Functionality**: Revert changes with a "Ctrl+Z" feature for better user control.
- **Save and Load**: Export processed DataFrames and trained models for future use.
- **Loading Animations**: Visual feedback during data loading and model training for improved UX.

## Technologies Used
- **Python**: Core programming language.
- **PyQt6**: For building the graphical user interface.
- **pandas**: Data manipulation and cleaning.
- **scikit-learn**: Training and evaluating machine learning models.
- **XGBoost**: Advanced gradient boosting for classification.
- **Plotly**: Interactive data visualizations.
- **QThread**: Parallel processing for model training.
- **joblib**: Saving and loading trained models.
- **Poetry**: Dependency management.

## Usage
-Load a Dataset:
-Use the "File > Open Dataframe" menu to load a CSV or Excel file.
-A loading animation will appear while the data is processed.
-Explore and Clean Data:
-Use buttons like "Filter", "Handle Null", and "Change Type" to preprocess your dataset.
-Visualize data with the "Graph" button (powered by Plotly).
-Train Classification Models:
-Open the Classification Explorer via the dedicated button.
-Select features, a target column, and a model (or "All" to train multiple models in parallel).
-View results like accuracy and training time in the "Results" tab.
-Make Predictions:
-In the "Prediction" tab, enter feature values and click "Predict" to get results from the trained model.
-Save Your Work:
-Save the processed DataFrame via "File > Save Dataframe".
-Save trained models in the Classification Explorer for later use.
