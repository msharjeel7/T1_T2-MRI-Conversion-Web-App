# Import the os module for interacting with the operating system (like file paths)
import os

# Import Flask and required functions for handling requests and responses
from flask import Flask, request, jsonify, send_from_directory

# Enable Cross-Origin Resource Sharing so frontend (on a different port) can call this API
from flask_cors import CORS

# Import NumPy for numerical operations
import numpy as np

# Import PIL to handle image loading and conversion
from PIL import Image

# Import InstanceNormalization layer used in CycleGAN models
from tensorflow_addons.layers import InstanceNormalization

# Import Keras (used to load and run the model)
from tensorflow import keras


# Import datetime to generate timestamps for unique filenames
from datetime import datetime

# Import re (regular expressions) to sanitize uploaded filenames (remove spaces, symbols, etc.)
import re

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for the Flask app so frontend can talk to backend without CORS errors
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the T1 -> T2 generator model from file
# 'compile = False' because we don't need to train it, just run inference
# 'custom_objects' is used to properly load the InstanceNormalization layer
MODEL_T1 = keras.models.load_model(
    'models/generator_T2_epoch30.h5',
    compile = False,
    custom_objects = {'InstanceNormalization': InstanceNormalization}
)

# Load the T2 -> T1 generator model from file in the same way
MODEL_T2 = keras.models.load_model(
    'models/generator_T1_epoch30.h5',
    compile = False,
    custom_objects = {'InstanceNormalization': InstanceNormalization}
)

# Set the folder where original and converted files will be placed
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

# Create folders if they don't exist
# 'exist_ok = True' prevents errors if the folder already exists
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
os.makedirs(RESULT_FOLDER, exist_ok = True)

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Define a function to preprocess the uploaded image before passing to the model
def preprocess(img):
    # Save the original image size so we can resize the output back later if needed
    original_size = img.size

    # Convert the image to grayscale ('L' mode = luminance)
    img = img.convert("L")

    # Resize the image to 128x128 (the model input size)
    img = img.resize((128, 128))

    # Convert the image to a NumPy array of type float32
    img = np.array(img).astype(np.float32)

    # Normalize pixel values to the range [-1, 1]
    img = (img / 127.5 ) - 1.0

    # Expand dimensions: shape becomes (1, 128, 128, 1)
    # Axis 0 = batch size; axis -1 = channel (grayscale = 1)
    img = np.expand_dims(img, axis = (0, -1))

    # Return the preprocessed image and the original size
    return img, original_size

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Define a function to postprocess the model's output image
def postprocess(img, original_size):
    # Remove batch and channel dimensions: from shape (1, 128, 128, 1) -> (128, 128)
    img = img[0, :, :, 0]

    # Denormalize pixel values: from [-1, 1] → [0, 255]
    img = (img + 1.0) * 127.5

    # Clip values to ensure they stay in valid image range, then convert to uint8
    img = np.clip(img, 0, 255).astype(np.uint8)

    # Convert NumPy array back to PIL Image in grayscale mode ('L')
    img = Image.fromarray(img, mode = 'L')

    # Resize image back to its original size before preprocessing
    img = img.resize(original_size)

    # Return the final image
    return img

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Define a route for handling image conversion requests using POST method
@app.route('/convert', methods=['POST', 'OPTIONS'])
def convert():
    # Get the conversion direction from the form data ('T1_T2' or 'T2_T1')
    direction = request.form['direction']

    # Get the list of uploaded files with the key 'images'
    files = request.files.getlist('images')

    # Initialize an empty list to store the result filenames
    results = []

    # Loop through each uploaded file
    for file in files:
        # Extract the original name of the uploaded file (without its extension)
        original_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', os.path.splitext(file.filename)[0])

        # Get the current date and time in a specific string format: '2025-07-23_214201_123456'
        # 'Year-Month-Day_HourMinutesSeconds_Microseconds'
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S_%f')

        # Combine original name and timestamp to create a unique, readable filename
        filename = f"{original_name}_{timestamp}.png"

        # Save the uploaded image to the 'static/uploads' folder
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)

        # Open the image using PIL and convert it to grayscale ('L' = luminance)
        img = Image.open(file).convert("L")

        # Save the original size to resize the output back after processing
        orig_size = img.size

        # Preprocess the image (resize to 128x128, normalize, add batch and channel dims)
        input_tensor, orig_size = preprocess(img)

        # Use the correct model based on direction
        if direction == 'T1_T2':
            # Run the image through the T1 -> T2 model
            output = MODEL_T1(input_tensor, training = False)
        else:
            # Run the image through the T2 -> T1 model
            output = MODEL_T2(input_tensor, training = False)
        
        # Postprocess the model output (remove batch dim, denormalize, resize back to original)
        out_img = postprocess(output.numpy(), orig_size)

        # Save the converted image to the 'static/results' folder
        result_path = os.path.join(RESULT_FOLDER, filename)
        out_img.save(result_path, format = 'PNG')

        # Add the filename to results list to send back to frontend
        results.append({'filename': filename})

        # DEBUG PRINTS
        print(f"[DEBUG] Converted image saved: {result_path}")
        print(f"[DEBUG] Accessible at: http://127.0.0.1:5000/static/results/{filename}")
        print(f"[DEBUG] Does file exist? {os.path.exists(result_path)}")

    # Return the list of converted filenames as JSON
    return jsonify(results)

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Define a new route to serve static files (like converted images) from the 'static' folder.
#@app.route('/static/uploads/<filename>')
#def serve_file(filename):
    # Use Flask's built-in function to send the file from the 'UPLOAD_FOLDER' directory.
#    return send_from_directory(UPLOAD_FOLDER, filename)

#@app.route('/static/results/<filename>')
#def serve_upload(filename):
#    return send_from_directory(RESULT_FOLDER, filename)

# This block runs the Flask app only if the script is run directly (not imported).
if __name__ == '__main__':
    # Run the Flask development server with debugging enabled (shows errors in the browser).
    app.run(debug = True)

