import pygame
import sys
import serial
import matplotlib
import csv
import time
import requests
from collections import deque

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

SHEET_URL = 'https://script.google.com/macros/s/AKfycbyebmLPcKBItV3CZJ8uB_bDldhB2X_beb3rpHTVFiTLoz31uadYXNW4J2jMXBDqB1Wx/exec'


pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Graph + Arduino Circle")
clock = pygame.time.Clock()

plt.ion()
x, y = deque(maxlen=100), deque(maxlen=100)
fig, ax = plt.subplots()
line, = ax.plot(x, y, 'r-')
ax.set_xlim(0, 100)
ax.set_ylim(0, 500)
avg_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, color='blue')

try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
except serial.SerialException:
    sys.exit("Error: Could not open COM5")

distance = 30
run = True

with open('distance_logger.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Timestamp", "Distance"])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((0, 0, 0))

        try:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode().strip()
                if data:
                    distance = int(data)
                    x.append(len(x))
                    y.append(distance)
                    line.set_xdata(x)
                    line.set_ydata(y)
                    ax.set_xlim(0, max(100, len(x)))
                    ax.set_ylim(min(y, default=0) - 10, max(y, default=500) + 10)

                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([timestamp, distance])

                    try:
                        response =requests.post(SHEET_URL, json={"distance": distance})
                        print(response.text)
                    except:
                        pass

                    average_distance = sum(y) / len(y) if len(y) > 0 else 0
                    avg_text.set_text(f'Avg Distance: {average_distance:.2f} cm')
                    fig.canvas.draw()
                    fig.canvas.flush_events()
        except ValueError:
            pass

        color = (0, 255, 0) if distance >= 50 else (255, 255, 0) if distance >= 20 else (255, 0, 0)
        pygame.draw.circle(screen, color, [300, 300], min(distance + 50, 300), 0)

        pygame.display.flip()
        clock.tick(60)

arduino.close()
pygame.quit()
sys.exit()
