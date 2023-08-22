# Self Driving Car ([Demo Link](https://clipchamp.com/watch/GywOsHEL7n1))
Train a 2D Car to optimally navigate a track using **Evolutionary Neural Networks**. Built with NumPy for computation and pyglet for the simulation.

![DemoGif](https://github.com/evansandoval/SelfDrivingCar/blob/TwoPhaseTraining/images/SelfDrivingCar.gif?raw=true)

## Introduction

This repository contains a simulation of a car navigating through a 2D track using an AI trained with the genetic algorithm. Essentially, the program mimics evolution to gradually improve performance of a population of cars over generations.

The goal of this project is to gain an understanding of Evolutionary Neural Networks by implementing them without the use of any machine learning libraries. Additionally, the project is meant to demonstrate the capabilities of machine learning algorithms under limited input environments.

## Features

- **Genetic Algorithm**: The genetic algorithm selects the best-performing cars from each generation and uses crossover and mutation operations to create the next generation. (Implemented in Generations.py)
  
- **Neural Network**: The neural network determines the behavior of the vehicle based on whether a wall is detected near the car. It takes a vector of boolean inputs (e.g. `wall_detected_left`, `wall_detected_right`) and performs matrix multiplication to output a vector of controls (e.g. `up`, `left`). (Implemented in Brain.py)

- **Fitness Function**: A fitness function evaluates the performance of each car based on how many checkpoints it successfully passes and how quickly it completes the track. (Implemented in CarGame.py, Line 241)

- **Modular Design**: The project was built with modular design in mind, allowing the simulation to optimize for other parameters, such as number of hidden layers, number of neurons in each layer, number and angle of inputs, car speed, car turn radius, etc. Additionally, tools are in place for rapid imports of new tracks.

## Installation

1. Clone the repository:
   ```bash
   $ git clone https://github.com/evansandoval/SelfDrivingCar.git

2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [pyglet](https://pyglet.readthedocs.io/en/latest/programming_guide/installation.html).

     ```bash
    pip install --upgrade --user pyglet

## Sources
This project was heavily inspired by Code Bullet's [A.I. Learns to DRIVE](https://www.youtube.com/watch?v=r428O_CMcpI) Project, which uses TensorFlow for the Machine Learning, and ray casting to measure distance from walls. The main changes made in this project were implementing the Machine Algorithm from scratch and using boolean inputs for wall detection (as opposed to a numeric distance).

Additionally, a great deal of the mathematic implementation for the neural network was inspired by 3Blue1Brown's [Neural Network Series](https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
