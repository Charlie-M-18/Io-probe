from flask import Flask, render_template
import bme280
import smbus2
import os
from datetime import datetime

app = Flask(__name__)

# Sensor Setup
address = 0x76
bus = smbus2.SMBus(1)
bme280.load_calibration_params(bus, address)

temp_history = []

@app.route('/')
def index():
    # 1. Get Temperature
    sample = bme280.sample(bus, address)
    current_temp = round(sample.temperature, 1)
    
    # Update history for graph (max 20 points)
    temp_history.append(current_temp)
    if len(temp_history) > 20:
        temp_history.pop(0)
    
    # 2. Capture Visual Feed
    timestamp = datetime.now().strftime("%H:%M:%S")
    os.system(f"rpicam-still -o static/io_image.jpg --immediate")
    
    return render_template('index.html', 
                           temp=current_temp, 
                           history=temp_history, 
                           time=timestamp)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=5000, debug=True)