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

# Move the drone to a new location
new_location = LocationGlobalRelative(-35.37016109, 149.17269844, 20)
vehicle.simple_goto(new_location)

# Wait for the drone to reach the new location
while True:
    distance = distance_to_current_waypoint(new_location)
    #distance = vehicle.location.global_relative_frame.distance_to(new_location)
    if distance <= 1:  # target radius in meters
        break
    time.sleep(1)

# Land the drone
vehicle.mode = VehicleMode("LAND")
print("Drone has landed")

# Close the connection
vehicle.close()

