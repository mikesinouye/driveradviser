# DriverAdviser

Hack Arizona 2020 submission, uses geolocation data of vehicles to provide safety updates, trend analysis, and live event presentation to the user. Data is used from several sources, and is available via a mobile app for increased safety.

Instructions for self-deployment:

Google Drive Link: https://drive.google.com/drive/folders/1to6_IomXK14IzFqfoJ_Bd7371cI9ROzV

# Critical Path / To-Do List:

Backend:
 Get the data from the NATS
 Read/interpret the NATS data
 Predict the path using the NATS data position/velocity
 Decide whether there will be collisions, close, near collision
 Send alert back to NATS (or wherever)
 Tunnel any Python data or outputs into the Node backend
 Alternative dataset that can be used for crashes
 
Frontend:
 Routinely pull live data from backend server (Ajax?)
 Update frontend display with live data
 Python script Execution based on routine or intialization
 Earth map overlay
 Static overlay of crash sites
 Popup modals or listing in page of scenarios (live)
 Popup modals or listing in page of suggestions (live)
 Dynamic/live view of vehicle position
 Dynamic/live line of prior path
 Dynamic/live line of predicted path
 Heatmat of crashes

Dependencies:
Python 3.6.5 or later
pip install:
- asyncio-nats-client
- nkeys
- protobuf
- python3-protobuf