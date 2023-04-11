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

# Define the PID controller
class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.error = 0
        self.error_integral = 0
        self.error_derivative = 0
        self.last_error = 0
        self.last_time = time.time()

    def update(self, measured_value):
        current_time = time.time()
        elapsed_time = current_time - self.last_time

        self.error = self.setpoint - measured_value
        self.error_integral += self.error * elapsed_time
        self.error_derivative = (self.error - self.last_error) / elapsed_time

        output = self.kp * self.error + self.ki * self.error_integral + self.kd * self.error_derivative

        self.last_error = self.error
        self.last_time = current_time

        return output

# Define the control algorithm
def control_algorithm(wp):
    pid = PIDController(0.1, 0.05, 0.01, wp.alt)

    while True:
        altitude = vehicle.location.global_relative_frame.alt
        output = pid.update(altitude)

        vehicle.simple_goto(LocationGlobalRelative(wp.lat, wp.lon, output))
        time.sleep(1)

        if abs(altitude - wp.alt) <= 0.5:  # target altitude - 0.5 meters
            break

# Test PID control

waypoints = [
    LocationGlobalRelative(-35.36032097, 149.16862764, 20),
    LocationGlobalRelative(-35.35892779, 149.16504410, 20),
    LocationGlobalRelative(-35.36079177, 149.16149177, 20),
    LocationGlobalRelative(-35.36374487, 149.16259327, 20)
]

for wp in waypoints:
    control_algorithm(wp)

# Land the drone
vehicle.mode = VehicleMode("LAND")

# Close the connection
vehicle.close()
