import cv2
import numpy as np

# Define el color en formato hexadecimal
hex_color = '#23705e'

# Convierte el color hexadecimal a HSV
rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
hsv_color = cv2.cvtColor(np.array([[rgb_color]], dtype=np.uint8), cv2.COLOR_RGB2HSV)[0][0]

# Define el rango de valores en el espacio de color HSV correspondiente al color turquesa
hue_tolerance = 10 # margen de tolerancia en el valor de matiz
saturation_threshold = 50 # valor mínimo de saturación
value_threshold = 50 # valor mínimo de brillo
lower = np.array([hsv_color[0] - hue_tolerance, saturation_threshold, value_threshold])
upper = np.array([hsv_color[0] + hue_tolerance, 255, 255])

print("Rango de valores en el espacio de color HSV para el color turquesa:")
print("Lower: ", lower)
print("Upper: ", upper)
