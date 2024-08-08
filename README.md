# Aller! USTH - USTH's Internship / Graduation Project

(For more information of the project, please refer to the [final report](Thesis.pdf).)

**Aller! USTH** is a physical enhancement gaming application developed to merge fitness with gameplay, using advanced pose estimation technology. This project aims to combat sedentary behavior among students and young adults by encouraging regular physical activity through engaging and interactive gameplay.

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Game Modes](#game-modes)

## Introduction

In today’s digital age, video games have become a dominant form of entertainment. However, this has led to increased sedentary behavior among young adults, resulting in various health issues. **Aller! USTH** addresses this problem by merging physical activity with engaging gameplay, utilizing pose estimation models to ensure accurate and responsive movement tracking.

## Key Features

- **Real-time Pose Estimation**: Utilizes the laptop or PC webcam to capture and analyze players' movements using MediaPipe Pose and MoveNet models.
- **Multiple Game Modes**: Includes endless-running, object-slicing, and shape-fitting modes, each requiring distinct physical actions.
- **Accurate Tracking**: Employs advanced landmark detection to ensure precise and responsive gameplay.
- **Accessible Hardware**: Designed to work with standard webcams, eliminating the need for specialized equipment.
- **Health-focused Design**: Encourages physical activity, making it an integral part of the gaming experience.

## Technology Stack

### Pose Estimation Models

- **MediaPipe Pose**: Developed by Google, provides high accuracy and real-time performance, detecting 33 key body landmarks.
- **MoveNet**: A fast and precise model designed for real-time applications, capable of detecting 17 key body landmarks with minimal latency.

### Game Design

- **Unity**: Chosen for its robust features and beginner-friendly interface, Unity supports complex game mechanics and seamless integration with pose estimation models.
- **Blender**: Used for creating detailed 3D models and animations, ensuring high-quality visual elements within the game.

### Programming Languages

- **Python**: Utilized for implementing pose detection models and processing real-time video input.
- **C#**: Employed within Unity for game logic and interaction mechanics.

## System Requirements

### Minimum Requirements

- **GPU**: Graphics card with OpenGL 3.0 or DirectX 9.0c support.
- **RAM**: 4GB or higher.
- **Storage**: 2GB of free disk space.
- **Display**: 1280x720 resolution or higher.

### Recommended Requirements

- **GPU**: Graphics card with support for OpenGL 4.x or DirectX 11.
- **RAM**: 8GB or higher.
- **Storage**: SSD with at least 4GB of free disk space.
- **Display**: 1920x1080 resolution or higher.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Xernnn/Aller-USTH.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd Aller-USTH
   ```
3. **Extract the .exe game file and play!**

## Attention!

1. **Ensure your webcam is connected and working properly.**
2. **Follow the on-screen instructions to start playing and engaging in physical activities.**

## Game Modes

- **(main) Endless-Running Mode:** Navigate through hallways by moving left, right, jumping, and crouching to avoid obstacles and collect coins.
- **Object-Slicing Mode:** Slice through objects using hand movements, inspired by Fruit Ninja game.
- **Shape-Fitting Mode:** Fit through incoming shapes by adjusting your body posture, inspired by Hole in the Wall game.
