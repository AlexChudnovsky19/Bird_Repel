# BirdRepel: Automated Bird Deterrent System 🐦🚫

## Table of Contents 📚

- [📖 About](#-about)
- [📷 Demo](#-demo)
- [🚀 Features](#-features)
- [🧠 Training Process](#-training-process)
- [🛠️ Installation](#️-installation)
  - [Prerequisites](#prerequisites)
  - [Hardware Setup 🔧](#hardware-setup-🔧)
  - [Software Setup 🖥️](#software-setup-🖥️)
- [⚙️ Usage](#-usage)
- [🧰 Technologies](#-technologies)


## 📖 About

**BirdRepel** is an automated bird repellent system designed to protect balcony plants and maintain cleanliness by preventing birds from leaving droppings. Using computer vision with a custom-trained YOLOv11 model, BirdRepel detects the presence of birds in real-time. Upon detection, the system activates a water gun via a relay module connected to a Raspberry Pi, effectively discouraging birds from approaching and harming your plants and the balcony.

## 📷 Demo

Live Demo Video, Turn on the sound to hear the activation of the water gun when the bird detected.

https://github.com/user-attachments/assets/d26f57ec-11eb-4fec-92f1-a3dae460602a

## 🚀 Features

- **Real-Time Bird Detection 🕒:** Utilizes a YOLOv11 model trained on a custom bird dataset for accurate detection.
- **Automated Deterrent Activation 💧:** Triggers a water gun to scare away birds upon detection.
- **Edge Computing 🖥️:** Runs entirely on a Raspberry Pi, ensuring low latency and independence from external servers.
- **Customizable Detection Parameters 🎛️:** Adjust sensitivity and detection thresholds to suit specific environments.
- **Energy Efficient 🔋:** Optimized for low power consumption, making it ideal for continuous outdoor use.
- **Hardware Integration 🔌:** Seamlessly integrates Raspberry Pi with relay modules and external devices like water guns.
- **Voltage Management ⚡:** Ensures safe and effective voltage regulation for connected peripherals.

## 🧠 Training Process

Training the YOLOv11 model involved several key steps to ensure high accuracy in bird detection:

### 1. **Dataset Collection 📸**

- Created a comprehensive bird dataset by capturing and finding online images from various angles and lighting conditions of the birds that damage the balcony plants and cleanliness.
- Ensured diversity by including different bird species and backgrounds to enhance model robustness.

### 2. **Data Annotation 📝**

- annotated images using roboflow to mark bounding boxes around birds.
- Organized data into training and validation sets to monitor performance.

### 3. **Model Training 🏋️‍♂️**

- Utilized the YOLOv11 architecture for its balance between speed and accuracy.
- Configured hyperparameters such as learning rate, batch size, and epochs to optimize training.
- Employed transfer learning by initializing with pre-trained weights to accelerate convergence.

### 4. **Model Evaluation 📊**

- Assessed model performance using metrics like Precision, Recall, and mAP (mean Average Precision).
- Fine-tuned the model based on evaluation results to achieve optimal detection accuracy.

![Model_Training_Track](https://github.com/user-attachments/assets/3d0c44b3-c863-48c2-bd33-4808de3f3c9f)

### 5. **Deployment 🚀**

- Converted the trained model to a format compatible with Raspberry Pi.
- Optimized the model for real-time inference on edge devices.
- Model capture example:

![model_capture_example](https://github.com/user-attachments/assets/133cc5b8-0a69-488a-a704-6facb332c613)
  
![model_capture_example_](https://github.com/user-attachments/assets/89f7e226-c9ef-48d5-ad7c-b1a51436345a)



## 🛠️ Installation

### Prerequisites

#### **Hardware 🖥️**

- **Raspberry Pi 4** (4GB RAM recommended) 🪨
- **Raspberry Pi Camera Module** 📷
- **Relay Module** 🔌
- **Water Gun** 💦 (operating at appropriate voltage)
- **Power Supply** for Raspberry Pi and peripherals 🔋
- **Jumper Wires** 🪛

#### **Software 💻**

- **Raspberry Pi OS** 🐧
- **Python 3.8+** 🐍
- **OpenCV** 📚
- **PyTorch** 🧠
- **YOLOv11** 🔍

### Hardware Setup 🔧

<img src="https://github.com/user-attachments/assets/b034a707-f648-4d06-8267-6044433683c3" alt="Hardware Setup" width="600" height="600"/>

#### **Set Up the Relay Module 🔌**

##### **Wiring Diagram 🛠️**

- **VCC (Relay)** → **5V** (Raspberry Pi)
- **GND (Relay)** → **GND** (Raspberry Pi)
- **IN (Relay)** → **GPIO17** (Pin 11)
- **NO (Normally Open)** → **Water Gun Positive Terminal (+)**
- **COM (Common)** → **Power Supply Positive (+)**
- **Water Gun Negative Terminal (−)** → **Power Supply Negative (−)**

##### **Voltage Integration ⚡**

- **Important:** Ensure that the voltage requirements of the water gun match the relay's specifications.
- Use a separate power supply for the water gun if necessary to prevent overloading the Raspberry Pi.
- Consider using a voltage regulator or a power management module to maintain stable voltage levels.

##### **Safety Precautions 🛡️**

- Double-check all connections before powering up.
- Use appropriate resistors or protective components to prevent short circuits.
- If unsure, consult an electronics professional to verify the setup.

#### **Power Supply 🔋**

- Provide a reliable power source to the Raspberry Pi and peripherals.
- Use high-quality power adapters to ensure consistent voltage and current.

### Software Setup 🖥️

#### **Clone the Repository 📥**

```bash
git clone https://github.com/yourusername/BirdRepel.git
cd BirdRepel
```

#### **Set Up the Environment 🛠️ ** 

```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install -r requirements.txt
```

#### **Configure the YOLOv11 Model 🧩**
Place the trained YOLOv11 weights in the models/ directory.
Update the configuration file config.yaml with the correct paths and parameters.

#### **Set Up Environment Variables ⚙️**
Create a .env file in the root directory and add the necessary configurations:

```env
MODEL_PATH=models/yolov11.pth
CAMERA_INDEX=0
RELAY_PIN=17
DETECTION_THRESHOLD=0.5
WATER_GUN_VOLTAGE=12V
Note: Replace WATER_GUN_VOLTAGE with the actual voltage requirement of your water gun.
```

#### **Enable GPIO Access 🔓**
Ensure that the Raspberry Pi has access to GPIO pins.

```bash
sudo raspi-config
Navigate to Interfacing Options and enable Camera and GPIO.
```

#### **Run the Application 🏃‍♂️**

```bash
python3 bird_tracker.py
```

#### **Deploy on Startup 🔄**

To ensure BirdRepel runs automatically on boot:

Open the crontab editor:

```bash
sudo crontab -e
```
Add the following line:

```bash
@reboot /usr/bin/python3 /home/pi/BirdRepel/main.py &
```

## ⚙️ Usage

Once installed and running, BirdRepel operates seamlessly to protect your balcony plants. Here's how to use and customize the system:

#### **Start the System 🚀**
Ensure all hardware connections are secure.

Run the application:

```bash
python3 main.py
```

#### **Monitoring 👀**

The system will display a live feed from the camera.
Detected birds will be highlighted with bounding boxes.
The console will log detection events and relay activations.

#### **Customization 🎛️**

Detection Sensitivity
Adjust the DETECTION_THRESHOLD in the .env file to make the system more or less sensitive to bird movements.
Relay Configuration
Modify the RELAY_PIN if you're using a different GPIO pin for the relay module.
Water Gun Voltage
Set the WATER_GUN_VOLTAGE in the .env file to match your water gun's specifications.

#### **Logging 📄**

Logs are saved in the logs/ directory for monitoring detections and system performance.
Review logs to analyze detection accuracy and system responsiveness.

## 🧰 Technologies

Programming Languages: Python

Machine Learning: YOLOv11, PyTorch 

Hardware:

Raspberry Pi 4 
Raspberry Pi Camera Module 
Relay Module 
4 Volt Water Gun 

Libraries & Frameworks:

OpenCV, GPIO Zero 


