import joblib
from azureml.core.model import Model
import json

def init():
    global model
    model_path = Model.get_model_path('group11_model')
    model = joblib.load(model_path)

def run(data):
    try:
        data = json.loads(data)
        result = model.predict(data['data'])
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error
