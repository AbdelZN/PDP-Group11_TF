# my_script.py

import argparse
from azureml.core import Workspace, Experiment, Dataset, Run
from azureml.core.model import Model
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
args = parser.parse_args()

# Load dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate model
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy}")

# Save model
model_file = 'model11.pkl'
joblib.dump(value=model, filename=model_file)

# Get the current run
run = Run.get_context()

# Log metrics
run.log('accuracy', accuracy)

# Upload the model file explicitly into artifacts 
run.upload_file(name=model_file, path_or_stream=model_file)

# Complete the run
run.complete()

# Register the model
workspace = run.experiment.workspace
model = Model.register(workspace=workspace,
                       model_name='group11_model',
                       model_path=model_file)
