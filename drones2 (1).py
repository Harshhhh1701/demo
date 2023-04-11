#!/usr/bin/env python3
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def distance_to_current_waypoint(awp):
    distancetopoint = get_distance_metres(vehicle.location.global_frame, awp)
    return distancetopoint

# Connect to the vehicle
vehicle = connect('udp:127.0.0.1:14550')

# Arm and take off
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True
vehicle.simple_takeoff(10)

# Wait for the drone to reach a certain altitude
while True:
    altitude = vehicle.location.global_relative_frame.alt
    if altitude >= 9.5:  # target altitude - 0.5 meters
        break
    time.sleep(1)

# Define the mission waypoints
waypoints = [
    LocationGlobalRelative(-35.36032097, 149.16862764, 20),
    LocationGlobalRelative(-35.35892779, 149.16504410, 20),
    LocationGlobalRelative(-35.36079177, 149.16149177, 20),
    LocationGlobalRelative(-35.36374487, 149.16259327, 20)
]

# Fly the mission
for wp in waypoints:
    vehicle.simple_goto(wp)
    while True:
        distance = distance_to_current_waypoint(wp)
        #distance = vehicle.location.global_relative_frame.distance_to(wp)
        if distance <= 1:  # target radius in meters
            break
        time.sleep(1)

# Land the drone
vehicle.mode = VehicleMode("LAND")
print("Drone has landed")

# Close the connection
vehicle.close()
