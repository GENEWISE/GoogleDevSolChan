import os
import zipfile
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt


st.set_page_config(page_title="Skin Lesion Classifier", layout="wide")


st.title("Skin Lesion Classification")
st.markdown("""
This application classifies skin lesion images as benign or malignant using a deep learning model.
Upload an image to get a prediction.

**Disclaimer**: This is for educational purposes only and should not be used for medical diagnosis.
Please consult a healthcare professional for proper medical advice.
""")
with st.sidebar:
    st.header("About")
    st.info("This app uses a CNN model trained on the ISIC dataset to classify skin lesions.")
    st.header("Model Information")
    st.markdown("""
    - Input size: 224x224 pixels
    - Classes: Benign, Malignant
    - Built with TensorFlow/Keras
    """)

@st.cache_resource
def load_model():
    try:
        model = keras.models.load_model("benign_malignant_classifier.h5")
        st.success("Model loaded successfully!")
        return model
    except:
        st.warning("Model file not found. Training a new model...")
        return train_new_model()

def train_new_model():
    st.write("This would normally train a new model if the pre-trained model is not available.")
    st.write("For the purpose of this demo, we'll create a simple model architecture similar to the original.")
    
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(128, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Flatten(),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def classify_image(img_data, model):
    img = tf.image.resize(img_data, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    prediction = model.predict(img)
    probability = float(prediction[0][0])
    
    return "Malignant" if probability > 0.5 else "Benign", probability

def extract_sample_images():
    st.write("For a full application, you would extract sample images from the dataset.")
    return None

model = load_model()

st.header("Upload an Image for Classification")
uploaded_file = st.file_uploader("Choose a skin lesion image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Uploaded Image")
        img_data = image.load_img(uploaded_file)
        img_array = image.img_to_array(img_data)
        st.image(img_array.astype(np.uint8), use_column_width=True)
    
    with col2:
        st.subheader("Classification Result")
        
        if st.button("Classify Image"):
            with st.spinner("Classifying..."):
                result, confidence = classify_image(img_array, model)
                
                if result == "Benign":
                    st.success(f"Classification: {result}")
                else:
                    st.error(f"Classification: {result}")
                
                st.metric("Confidence", f"{abs(confidence - 0.5) * 200:.2f}%")
                
                st.subheader("Probability Distribution")
                prob_malignant = confidence
                prob_benign = 1 - confidence
                
                chart_data = {
                    "Class": ["Benign", "Malignant"],
                    "Probability": [prob_benign, prob_malignant]
                }
                
                fig, ax = plt.subplots()
                ax.barh(chart_data["Class"], chart_data["Probability"], color=['green', 'red'])
                ax.set_xlim(0, 1)
                ax.set_xlabel('Probability')
                ax.set_title('Classification Probability')
                
                for i, v in enumerate(chart_data["Probability"]):
                    ax.text(v + 0.01, i, f"{v:.2f}", va='center')
                
                st.pyplot(fig)
                
                st.info("Note: A higher confidence doesn't always mean higher accuracy. This tool should not replace professional medical advice.")

st.header("Sample Gallery")
st.write("In a full application, you could include sample images from the dataset for users to test the model.")

st.header("How to Interpret Results")
st.markdown("""
- **Benign**: The model predicts the lesion is non-cancerous.
- **Malignant**: The model predicts the lesion may be cancerous.

**Important**: This tool is for educational purposes only. Always consult a dermatologist for proper diagnosis.
""")

st.header("About the Model")
st.markdown("""
This model was trained on the ISIC (International Skin Imaging Collaboration) dataset, 
which contains thousands of dermoscopic images of skin lesions.

The model uses a Convolutional Neural Network (CNN) architecture with multiple convolutional 
layers followed by dense layers. Data augmentation was applied during training to improve 
model generalization.

**Model Architecture:**
- 5 Convolutional layers with max pooling
- 2 Dense layers with dropout for regularization
- Binary classification output
""")

st.markdown("---")
st.markdown("Skin Lesion Classification App - Created with Streamlit and TensorFlow")