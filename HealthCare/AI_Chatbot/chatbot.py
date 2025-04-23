import pyttsx3
import matplotlib.pyplot as plt
from model import HealthcareChatbot

class ChatbotInterface:
    def __init__(self):
        self.chatbot = HealthcareChatbot()
        self.engine = pyttsx3.init()
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def plot_diagnosis(self, diseases, mean_probs, std_probs):
        plt.bar(diseases, mean_probs, yerr=std_probs, capsize=5, color='skyblue')
        plt.ylabel("Probability")
        plt.title("Diagnosis Confidence")
        plt.show()
        
    def run(self):
        print("Hello! I am your virtual health assistant robot.")
        print("Please answer the following questions with Y/N:")
        
        # Get symptoms from user
        symptoms = []
        for name in self.chatbot.symptom_names:
            ans = input(f"Do you have {name}? (Y/N): ").strip().lower()
            symptoms.append(1 if ans == 'y' else 0)
            
        # Get diagnosis
        diagnosis, mean_probs, std_probs = self.chatbot.get_diagnosis(symptoms)
        if diagnosis is None:
            print("Sorry, there was an error processing your symptoms.")
            return
            
        # Get recommendations
        test, medicine = self.chatbot.get_recommendations(diagnosis)
        
        # Display results
        print("\nDiagnosis with Probabilities and Uncertainty:")
        for i, dis in enumerate(self.chatbot.diseases):
            print(f"{dis}: P={mean_probs[i]:.3f}, Uncertainty={std_probs[i]:.3f}")
            
        self.speak(f"You may have {diagnosis}.")
        print(f"\nDiagnosis: {diagnosis} (±{std_probs[self.chatbot.diseases.index(diagnosis)]:.3f})")
        
        if test and medicine:
            self.speak(f"I recommend you take a {test} and consider taking {medicine}")
            print(f"Test: {test}")
            print(f"Medicine: {medicine}")
            
        # Plot results
        self.plot_diagnosis(self.chatbot.diseases, mean_probs, std_probs)

if __name__ == "__main__":
    interface = ChatbotInterface()
    interface.run() 