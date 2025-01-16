**Computer Vision Rock Paper Scissors Game**

A interactive Rock Paper Scissors game that uses your computer's webcam to detect hand gestures and play against the computer in real-time.

**Description**

This project implements a computer vision-based Rock Paper Scissors game where players can use actual hand gestures to play against the computer. Using advanced hand tracking technology through MediaPipe, the game captures and interprets the player's hand gestures in real-time, creating an immersive and interactive gaming experience.
The game features a split-screen interface where players can see both their own webcam feed and the computer's move. The computer's moves are randomly generated, ensuring fair gameplay. The system accurately detects hand landmarks to interpret whether the player is showing rock (closed fist), paper (open palm), or scissors (victory sign).

**Key features of the implementation include:**

- Real-time hand gesture processing with minimal latency
- Automatic scoring system that keeps track of both player and computer points
- Visual feedback system showing the detected gesture and game outcome
- Smooth game flow with automatic round progression when the player removes their hand
- Clear visual instructions and game state indicators
- Clean, intuitive interface with a custom background

The game combines elements of classic Rock Paper Scissors with modern computer vision technology, making it an excellent example of how traditional games can be enhanced with artificial intelligence and machine learning techniques.

**Features**

- Real-time hand gesture recognition
- Interactive gameplay with computer opponent
- Score tracking system
- Visual feedback with gesture recognition
- Clean user interface with game background

**Prerequisites**
The following Python packages are required to run the game:

- OpenCV (cv2)
- MediaPipe (mediapipe)
- Python's built-in random module
