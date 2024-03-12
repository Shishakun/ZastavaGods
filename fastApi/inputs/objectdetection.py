import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import preprocess_input

# Load the pre-trained model
model = load_model('path/to/model.h5')

# Define the class names
class_names = ['class1', 'class2', 'class3']

# Load the input image
input_image = cv2.imread('path/to/input/image.jpg')
input_image = cv2.resize(input_image, (224, 224))

# Prepare the image for the model
image = img_to_array(input_image)
image = np.expand_dims(image, axis=0)
image = preprocess_input(image)

# Predict the objects in the image
preds = model.predict(image)

# Find the index of the highest confidence class
class_index = np.argmax(preds[0])

# Display the prediction result
print('Detected Object:', class_names[class_index])

# Visualize the result on the input image
cv2.putText(
    input_image,
    'Detected Object: ' + class_names[class_index],
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 255, 0),
    2
)

cv2.imshow('Input Image', input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()