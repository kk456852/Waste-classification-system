import numpy as np
from keras.models import load_model
from .load_data import load_pic


def ProcessAPI(pic_path,
               model_path="C:\\Users\chali\Desktop\Waste-classification-system\WCS\classification_AI\model.h5"):
    model = load_model(model_path)
    data = load_pic("C:\\Users\chali\Desktop\Waste-classification-system\WCS"+pic_path)
    test_result = model.predict([[data]])
    return test_result
