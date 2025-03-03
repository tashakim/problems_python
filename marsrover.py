import sys
import math
"""Purpose: Control thrust level to safely land rover.
"""

surface_n = int(input())  # number of points used to draw the surface of Mars.
for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]


    # 2 integers: rotate power. rotate is the desired rotation angle (should be 0 for level 1), power is the desired thrust power (0 to 4).
    if(v_speed <= 0):    
        if(round(abs(v_speed)/10) == 4):
            print("0 4")
        elif(round(abs(v_speed)/10) == 3):
            print("0 3")
        elif(round(abs(v_speed)/10) == 2):
            print("0 2")
        elif(round(abs(v_speed)/10) == 1):
            print("0 1")
        else:
            print("0 0")