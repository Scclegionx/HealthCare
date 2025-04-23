import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
import pickle
import os

class HealthcareChatbot:
    def __init__(self):
        self.model = None
        self.diseases = ["Flu", "Cold", "COVID-19", "Allergy"]
        self.symptom_names = ["Fever", "Cough", "Sneezing", "Fatigue", "Loss of Taste", "Itchy Eyes"]
        self.test_map = {
            "Flu": "Influenza A/B test",
            "Cold": "Nasal swab",
            "COVID-19": "PCR test",
            "Allergy": "Allergy skin test"
        }
        self.medicine_map = {
            "Flu": "Oseltamivir (Tamiflu)",
            "Cold": "Rest, fluids, antihistamines",
            "COVID-19": "Isolation + Paracetamol",
            "Allergy": "Loratadine or Cetirizine"
        }

    def build_model(self):
        model = Sequential([
            Dense(16, activation='relu', input_shape=(6,)),
            Dropout(0.5),
            Dense(16, activation='relu'),
            Dropout(0.5),
            Dense(4, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self):
        # Training data
        X_train = np.array([
            [1, 1, 0, 1, 0, 0],  # Flu
            [0, 1, 1, 0, 0, 0],  # Cold
            [1, 1, 0, 0, 1, 0],  # COVID-19
            [0, 0, 1, 0, 0, 1]   # Allergy
        ], dtype=np.float32)
        
        y_train = tf.keras.utils.to_categorical([0, 1, 2, 3], num_classes=4)
        
        self.model = self.build_model()
        self.model.fit(X_train, y_train, epochs=100, verbose=0)
        
        # Save model and metadata
        self.save_model()

    def save_model(self):
        # Create directory if it doesn't exist
        os.makedirs('HealthCare/AI_Chatbot/models', exist_ok=True)
        
        # Save model
        self.model.save('HealthCare/AI_Chatbot/models/healthcare_model.h5')
        
        # Save metadata
        metadata = {
            'diseases': self.diseases,
            'symptom_names': self.symptom_names,
            'test_map': self.test_map,
            'medicine_map': self.medicine_map
        }
        
        with open('HealthCare/AI_Chatbot/models/metadata.pkl', 'wb') as f:
            pickle.dump(metadata, f)

    def load_model(self):
        try:
            self.model = load_model('HealthCare/AI_Chatbot/models/healthcare_model.h5')
            with open('HealthCare/AI_Chatbot/models/metadata.pkl', 'rb') as f:
                metadata = pickle.load(f)
                self.diseases = metadata['diseases']
                self.symptom_names = metadata['symptom_names']
                self.test_map = metadata['test_map']
                self.medicine_map = metadata['medicine_map']
            return True
        except:
            return False

    def predict_with_uncertainty(self, symptoms, n_iter=100):
        if not self.model:
            if not self.load_model():
                return None, None
        
        input_array = np.array([symptoms], dtype=np.float32)
        preds = np.array([self.model(input_array, training=True).numpy() for _ in range(n_iter)])
        mean = preds.mean(axis=0)
        std = preds.std(axis=0)
        return mean, std

    def get_diagnosis(self, symptoms):
        mean_probs, std_probs = self.predict_with_uncertainty(symptoms)
        if mean_probs is None:
            return None, None, None
        
        most_likely = np.argmax(mean_probs)
        diagnosis = self.diseases[most_likely]
        
        return diagnosis, mean_probs[0], std_probs[0]

    def get_recommendations(self, diagnosis):
        if diagnosis not in self.diseases:
            return None, None
        return self.test_map[diagnosis], self.medicine_map[diagnosis]

if __name__ == "__main__":
    # Train and save model
    chatbot = HealthcareChatbot()
    chatbot.train()
    print("Model trained and saved successfully!") 