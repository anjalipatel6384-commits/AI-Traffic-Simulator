# 🚦 AI Traffic Simulator

An AI-powered traffic simulation system built with **Python and Pygame**, designed to simulate intelligent urban traffic behavior with adaptive traffic signals, vehicle management, and real-time traffic monitoring.

## ✨ Features

- 🚗 Real-time vehicle simulation
- 🚦 Adaptive traffic signal control
- 🛑 Vehicles stop during red signals
- 🟡 Vehicles slow down during yellow signals
- 🚘 Vehicle spacing and collision prevention
- 🧠 Intelligent traffic control logic
- 📊 Real-time traffic density monitoring
- 🌙 Night mode
- 🌧️ Rain mode
- 🚑 Emergency mode
- 🎮 Manual and AI traffic control modes
- ⏱️ Dynamic signal countdown
- 📈 Real-time vehicle statistics

## 🧠 Intelligent Traffic Control

The simulator monitors traffic conditions at the intersection and uses traffic information to control signal timing.

The dashboard provides real-time information such as:

- Traffic signal state
- Current and next phase
- Signal countdown
- Vehicle queues from each direction
- Traffic density
- Green-light duration
- Spawned vehicles
- Passed vehicles
- Active vehicles

## 🚦 Traffic Signal Behavior

The simulator models realistic traffic signal behavior:

- 🔴 **Red:** Vehicles stop before the intersection.
- 🟡 **Yellow:** Vehicles slow down before continuing.
- 🟢 **Green:** Vehicles proceed through the intersection.

Vehicle spacing logic helps prevent vehicles from overlapping while moving through the simulation.

## 🌦️ Simulation Modes

### 🌙 Night Mode

Simulates traffic conditions during nighttime.

### 🌧️ Rain Mode

Simulates traffic during rainy conditions.

### 🚑 Emergency Mode

Provides an emergency traffic simulation mode for handling priority situations.

### 🧠 AI Mode

Enables intelligent traffic-control behavior based on the current simulation conditions.

## 🛠️ Technologies Used

- **Python**
- **Pygame**

## 📂 Project Structure

```text
AI-Traffic-Simulator/
│
├── main.py
├── simulation.py
├── traffic_signal.py
├── vehicles.py
├── config.py
├── screenshots/
│   ├── Screenshot (150).png
│   ├── Screenshot (151).png
│   ├── Screenshot (152).png
│   └── Screenshot (153).png
│
├── .gitignore
└── README.md
