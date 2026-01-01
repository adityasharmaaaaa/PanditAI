import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import os


# --- 1. DEFINE THE NEURAL NETWORK ---
class DestinyNet(nn.Module):
    def __init__(self):
        super(DestinyNet, self).__init__()
        # Input: 18 features (9 Planets x 2 values: SignID, HouseID)
        self.fc1 = nn.Linear(18, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 1)  # Output: Single Score (0-1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(0.2)  # Prevents overfitting

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.sigmoid(self.fc4(x))  # Output between 0 and 1
        return x


# --- 2. GENERATE SYNTHETIC TRAINING DATA ---
def prepare_dataset():
    print("🔮 Mining 'planets_data.json' to create training dataset...")

    with open("data/planets_data.json", "r", encoding="utf-8") as f:
        rules = json.load(f)

    # Keywords to automate "labelling"
    positive_words = [
        "wealth",
        "king",
        "famous",
        "strong",
        "excellent",
        "gain",
        "happiness",
        "honor",
    ]
    negative_words = [
        "poor",
        "sick",
        "disease",
        "death",
        "enemy",
        "loss",
        "grief",
        "weak",
        "bad",
    ]

    X = []  # Features
    y = []  # Labels (Scores)

    # We need to simulate full charts based on single rules
    # This is a simplification technique for training without 10,000 real people
    planet_map = {
        "Sun": 0,
        "Moon": 1,
        "Mars": 2,
        "Mercury": 3,
        "Jupiter": 4,
        "Venus": 5,
        "Saturn": 6,
        "Rahu": 7,
        "Ketu": 8,
    }
    zodiac_map = {
        "Aries": 0,
        "Taurus": 1,
        "Gemini": 2,
        "Cancer": 3,
        "Leo": 4,
        "Virgo": 5,
        "Libra": 6,
        "Scorpio": 7,
        "Sagittarius": 8,
        "Capricorn": 9,
        "Aquarius": 10,
        "Pisces": 11,
    }

    for rule in rules:
        p_name = rule.get("planet")
        if p_name not in planet_map:
            continue

        # 1. Create a "Neutral" Chart (all zeros)
        # Vector size 18: [SunSign, SunHouse, MoonSign, MoonHouse...]
        chart_vector = [0] * 18

        # 2. Fill in the specific planet from the rule
        p_idx = planet_map[p_name]

        # Get Sign ID
        sign_name = rule.get("sign")
        sign_id = zodiac_map.get(sign_name, 0)

        # Get House ID
        house_id = rule.get("house", 1)

        # Set values in vector
        chart_vector[p_idx * 2] = sign_id  # Even index = Sign
        chart_vector[p_idx * 2 + 1] = house_id  # Odd index = House

        # 3. Calculate Score based on Text Sentiment
        text = rule.get("prediction", "").lower()
        score = 0.5  # Neutral start

        for w in positive_words:
            if w in text:
                score += 0.15
        for w in negative_words:
            if w in text:
                score -= 0.15

        # Clamp between 0.0 and 1.0
        score = max(0.0, min(1.0, score))

        # Add to dataset
        X.append(chart_vector)
        y.append([score])

        # Data Augmentation: Add some noise to make model robust
        # (Simulating slightly different charts with same outcome)
        for _ in range(5):
            noisy_vector = list(chart_vector)
            # Randomly change a different planet to random sign
            rand_p = np.random.randint(0, 9)
            if rand_p != p_idx:
                noisy_vector[rand_p * 2] = np.random.randint(0, 12)
                noisy_vector[rand_p * 2 + 1] = np.random.randint(1, 13)
            X.append(noisy_vector)
            y.append([score])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


# --- 3. TRAIN LOOP ---
def train_model():
    X, y = prepare_dataset()

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Convert to Tensors
    X_train_t = torch.tensor(X_train)
    y_train_t = torch.tensor(y_train)

    model = DestinyNet()
    criterion = nn.MSELoss()  # Mean Squared Error
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Training Neural Network...")
    for epoch in range(1000):
        optimizer.zero_grad()
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"Epoch {epoch}: Loss {loss.item():.4f}")

    # Save Model
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/destiny_net.pth")
    print("  Model Saved: models/destiny_net.pth")


if __name__ == "__main__":
    train_model()
