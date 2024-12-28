# BirdRepel: Automated Bird Deterrent System 🐦🚫

## Table of Contents 📚

- [📖 About](#-about)
- [🚀 Features](#-features)
- [🧠 Training Process](#-training-process)
- [🛠️ Installation](#️-installation)
- [⚙️ Usage](#️-usage)
- [📷 Demo](#-demo)
- [🧰 Technologies](#-technologies)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📫 Contact](#-contact)

## 📖 About

**BirdRepel** is an automated bird deterrent system designed to protect balcony plants from birds that damage them. Leveraging advanced computer vision with a custom-trained YOLOv11 model, BirdRepel detects the presence of birds in real-time. Upon detection, the system activates a water gun via a relay module connected to a Raspberry Pi, effectively discouraging birds from approaching and harming your balcony.

## 🚀 Features

- **Real-Time Bird Detection 🕒:** Utilizes a YOLOv11 model trained on a custom bird dataset for accurate detection.
- **Automated Deterrent Activation 💧:** Triggers a water gun to scare away birds upon detection.
- **Edge Computing 🖥️:** Runs entirely on a Raspberry Pi, ensuring low latency and independence from external servers.
- **Customizable Detection Parameters 🎛️:** Adjust sensitivity and detection thresholds to suit specific environments.
- **Energy Efficient 🔋:** Optimized for low power consumption, making it ideal for continuous outdoor use.

## 🧠 Training Process

Training the YOLOv11 model involved several key steps to ensure high accuracy in bird detection:

1. **Dataset Collection 📸:**
   - Created a comprehensive bird datasets of the birds that harm the balcony.
   - Ensured diversity by including different bird species and backgrounds to enhance model robustness.

2. **Data Annotation 📝:**
   - Used annotation tool to mark bounding boxes around birds.
   - Organized data into training and validation sets to monitor performance.

3. **Model Training 🏋️‍♂️:**
   - Utilized the YOLOv11 architecture for its balance between speed and accuracy.
   - Configured hyperparameters such as learning rate, batch size, and epochs to optimize training.
   - Employed transfer learning by initializing with pre-trained weights to accelerate convergence.

   ```bash
   # Clone YOLOv11 repository
   git clone https://github.com/yourusername/yolov11.git
   cd yolov11

   # Install dependencies
   pip install -r requirements.txt

   # Start training
   python train.py --data data/bird_dataset.yaml --cfg cfg/yolov11.cfg --weights yolov5s.pt --epochs 100
