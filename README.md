# network-device-test-automation

IPX5455 Device Test Automation Tool
A Python-based desktop application built to automate the testing and configuration of IPX5455 network devices in a production or QA environment.

Overview
This tool provides a GUI interface to manage and monitor up to 40 network devices simultaneously over a local network. It was developed to reduce manual effort during device testing by automating IP configuration, connection monitoring, and paging system validation.

Features:
Change IP Mode - Automatically authenticates and reconfigures the IP address of each device unit via HTTP API calls, with real-time visual feedback on success or failure.
Burn Test Mode - Continuously monitors up to 40 devices by polling their connection status every 500ms. Disconnected units are highlighted in red with a running fail count, and an audio alert is triggered when a disconnection is detected.
Paging Trigger - Integrates with a paging server to send start/end paging commands at scheduled intervals, with a live paging count displayed on screen.
Timer - Tracks total burn test duration in days, hours, minutes, and seconds.

Tech Stack:
Python
requests - HTTP API communication with devices
tkinter - Desktop GUI
pygame - Audio alert on device disconnection
threading - Non-blocking background polling and timers

Setup:
Install dependencies:
bashpip install -r requirements.txt
tkinter, threading, and json come built-in with Python, no installation needed.
Ensure your PC is connected to the same local network (192.168.0.x) as the devices, then run:
hwg.py
