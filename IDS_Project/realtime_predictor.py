import pandas as pd
import time
import joblib
import os

# Load the trained model
model = joblib.load('decision_tree_model.pkl')

print("Model loaded successfully. Waiting for new data...")

# The absolute path to the file created by the C++ program
filename = r"C:\Users\theer\Documents\Intrusion-Detection-System\PacketSniffer\x64\Release\packet_data.csv"

# Function to make a prediction (this remains the same)
def predict_packet(packet_data):
    num_features = 78
    mock_data = [0.0] * num_features

    if len(packet_data) > 1 and packet_data[1].isdigit():
        mock_data[0] = float(packet_data[1])

    column_names = [f'col_{i}' for i in range(num_features)]
    new_packet_df = pd.DataFrame([mock_data], columns=column_names)

    prediction = model.predict(new_packet_df)

    if prediction[0] == 0:
        return "Normal Traffic"
    else:
        return "Attack"

# Main loop to continuously check for new data
# Wait for the file to be created by the C++ program
while not os.path.exists(filename):
    print("Waiting for packet_data.csv to be created by the C++ program...")
    time.sleep(1)

# Open the file and start processing from the beginning
with open(filename, 'r') as f:
    f.seek(0, os.SEEK_END)  # Go to the end of the file

    while True:
        line = f.readline()
        if not line:
            # Wait for more data to be written
            time.sleep(0.5)
            continue

        try:
            packet_data = line.strip().split(',')
            if len(packet_data) > 1:
                prediction = predict_packet(packet_data)
                print(f"New Packet: Timestamp={packet_data[0]}, Length={packet_data[1]} bytes. -> Prediction: {prediction}")
        except Exception as e:
            print(f"Error processing line: {e}")