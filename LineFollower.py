import cv2
import numpy as np


# Captura el frame de entrada de la camara
def get_frame(cap, scaling_factor):
    # Captura el frame del objeto de captura de video
    ret, frame = cap.read()
    
    # Redimensiona el frame de entrada 
    frame = cv2.resize(frame, None, fx=scaling_factor,
        fy=scaling_factor, interpolation=cv2.INTER_AREA)
    
    return frame

# Define el color en formato hexadecimal
hex_color = '#23705e'

# Convierte el color hexadecimal a HSV
rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
hsv_color = cv2.cvtColor(np.array([[rgb_color]], dtype=np.uint8), cv2.COLOR_RGB2HSV)[0][0]

# Define el rango de valores en el espacio de color HSV correspondiente al color turquesa
hue_tolerance = 10 # margen de tolerancia en el valor de matiz
saturation_threshold = 50 # valor mínimo de saturación
value_threshold = 50 # valor mínimo de brillo


if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.5
    
    # Itera hasta que se presione ESC
    while True:
            frame = get_frame(cap, scaling_factor)
            
            # Convierte el color a HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Aquí se define el color azul rn el espacio de HSV
            # lower = np.array([60,100,100])
            # upper = np.array([180,255,255])
                    
            lower = np.array([hsv_color[0] - hue_tolerance, saturation_threshold, value_threshold])
            upper = np.array([hsv_color[0] + hue_tolerance, 255, 255])      

            # LIMITA la imagen para solo mostrar el azul
            mask = cv2.inRange(hsv, lower, upper)

            
            # Bitwise-AND la mascara y la imagen original
            res = cv2.bitwise_and(frame, frame, mask=mask)
            res = cv2.medianBlur(res, 5)
            
            # Encuentra los contornos en la máscara
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                # Encuentra el contorno más grande
                contour = max(contours, key=cv2.contourArea)

                # Encuentra las coordenadas del rectángulo delimitador del contorno
                x, y, w, h = cv2.boundingRect(contour)

                # Dibuja un rectángulo alrededor del contorno
                cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)

                centro_x=x+w/2
                centro_y=y+h/2
                # Muestra las coordenadas del objeto azul en la ventana
                print(f"Coordenadas (x, y) del centro del objeto azul: ({centro_x}, {centro_y})")

            cv2.imshow('Imagen Original', frame)
            cv2.imshow('Detección de color azul', res)
            
            # Revisa si se ha presionado ESC
            c = cv2.waitKey(5)
            if c == 27:
                break

    cv2.destroyAllWindows()