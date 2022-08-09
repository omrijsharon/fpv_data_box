# FPV Data-Box
The easiest way to copy your blackbox logs and videos from your FPV drone and goggles.
Just take a small raspberry pi (or laptop with linux/windows) to your favorite spot, fly and fill the blackbox with logs, connect the flight controller to the raspberry pi, connect an sd card-reader and put your goggles sd card inside. The app will do the rest!

## Operating system
Linux / Windows

## What is it good for?
* Stabilizing your fpv videos with [GyroFlow](https://github.com/gyroflow/gyroflow).
* Calibrating your PIDs with [Betaflight Blackbox Explorer](https://github.com/betaflight/blackbox-log-viewer).

## What is it actually meant for?
* Creating the largest dataset of FPV flights, meant for:
  * Offline and Inverse Reinforcement Learning.
  * Flight models of FPV drones.
  * Flight characteristics of FPV pilots.
  * FPV Photorealistic Neural-Simulation (Using World Model and Google's Dreamer V2 algorithms).

## Installation
- TBA

## How to configure it?
### First Use:
* Select the folder you want to copy the logs and videos to.
* Add drones and pilots to the list.
* Save.
### Regular Use:
* Click on "Edit Config".
* Repeat the steps above (First Use).


## How to use it?
* Connect the flight controller to the raspberry pi / laptop.
* Connect the sd card-reader (with the goggles sd card) to the raspberry pi / laptop.
* Click on "Copy Log files and Videos" (the largest button in the app).
* Select Drone and Pilot.
* Click on "Copy" (the blue button).
