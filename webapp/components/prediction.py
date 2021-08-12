from keras.models import load_model 
from tensorflow.keras.preprocessing import image
import numpy as np

select='static/model/Valid.h5'
valid = load_model(select)
select = 'static/model/NvC.h5'
model = load_model(select)

def get_img_array(img_path):
  path = img_path
  img = image.load_img(path, target_size=(224,224,3))
  img = image.img_to_array(img)
  img = np.expand_dims(img , axis= 0 )
  
  return img



def predict_output():
  img=get_img_array('static/temp/temp.png')

  result ={
    "status":False,
    "covid":None,
    "normal":None,
    "result":"The Given Image is not a Chest X-ray"
  }

  validXray= np.argmax(valid.predict(img))

  if(validXray):
    class_type={0: "Covid-19 Positive", 1: "Covid-19 Negative"}
    prediction=model.predict(img)
    result["covid"] = round(prediction[0][0]*100, 4)
    result["normal"] = round(prediction[0][1]*100, 4)
    if(abs(result["covid"] - result["normal"]) < 40):
      result["result"] = "Unable to Predict"
    else:
      result["status"] = True
      result["result"] = class_type[np.argmax(prediction)]
  
  return result


