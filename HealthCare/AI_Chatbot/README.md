# Healthcare Chatbot

A virtual health assistant that helps diagnose diseases based on symptoms and provides recommendations.

## Features

- Diagnose diseases based on user symptoms
- Provide test and medicine recommendations
- Show diagnosis confidence with uncertainty estimates
- Visualize results with bar plots
- Text-to-speech output

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the chatbot:
```bash
python chatbot.py
```

## Usage

1. The chatbot will ask you questions about your symptoms
2. Answer with Y (Yes) or N (No)
3. The chatbot will:
   - Diagnose potential diseases
   - Show probabilities and uncertainty
   - Recommend tests and medicines
   - Display a bar plot of results

## Model Training

The model is pre-trained and saved in the `models` directory. To retrain:

1. Modify training data in `model.py`
2. Run training:
```python
chatbot = HealthcareChatbot()
chatbot.train()
```

## Files

- `model.py`: Contains the neural network model and training logic
- `chatbot.py`: Handles user interaction and displays results
- `requirements.txt`: Lists required Python packages 