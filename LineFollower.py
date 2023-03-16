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

################################ Esto es para la cuestión de color ############################

# Define el color en formato hexadecimal
hex_color = '#23705e'

# Convierte el color hexadecimal a HSV
rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
hsv_color = cv2.cvtColor(np.array([[rgb_color]], dtype=np.uint8), cv2.COLOR_RGB2HSV)[0][0]

# Define el rango de valores en el espacio de color HSV correspondiente al color turquesa
hue_tolerance = 10 # margen de tolerancia en el valor de matiz
saturation_threshold = 50 # valor mínimo de saturación
value_threshold = 50 # valor mínimo de brillo


################################### Esto es para la cuestión del cambio de coordenadas##########

# Definir las coordenadas del rectángulo (en terminos de la pantalla)
x1, y1 = 10, 10  # esquina superior izquierda
x2, y2 = 310, 230  # esquina inferior derecha

# Definir las coordenadas del rectángulo fijo (en terminos de la grafica)
rect_top_left = (0, 2)
rect_bottom_right = (10, -2)

# Tamaño del rectangulo 
rect_top_left_coord_originales = (0,0)
rect_bottom_right_coord_originales = (300,220)

#Definir la relación entre las coordenadas originales y las de la gráfica
a = (rect_bottom_right[0] - rect_top_left[0]) / (rect_bottom_right_coord_originales[0] - rect_top_left_coord_originales[0])
b = rect_top_left_coord_originales[1]

c1 = (rect_bottom_right[1] - rect_top_left[1]) / (rect_bottom_right_coord_originales[1]-rect_top_left_coord_originales[1]) 
d = rect_top_left[1]
#print(c)

################################# Esto es para leer la cámara #################################


if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.5

    # Establecer el tamaño de la ventana
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Itera hasta que se presione ESC
    while True:
            frame = get_frame(cap, scaling_factor)
            
            # Convierte el color a HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Aquí se define el color azul rn el espacio de HSV (es util para hacer pruebas
            # ya que es más fácil conseguir un objeto de color azul y manipularlo)
            lower = np.array([60,100,100])
            upper = np.array([180,255,255])
                    
            # Aquí se define el color que se estableció en formato hexadecimal
            # lower = np.array([hsv_color[0] - hue_tolerance, saturation_threshold, value_threshold])
            # upper = np.array([hsv_color[0] + hue_tolerance, 255, 255])      

            # LIMITA la imagen para solo mostrar el azul
            mask = cv2.inRange(hsv, lower, upper)

            
            # Bitwise-AND la mascara y la imagen original
            res = cv2.bitwise_and(frame, frame, mask=mask)
            res = cv2.medianBlur(res, 5)
            
            # Encuentra los contornos en la máscara
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Dibuja un rectangulo para poder enmarcar allí lo que deseo
            cv2.rectangle(res, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Dibuja un rectangulo en la línea que quiero monitorear
            if len(contours) > 0:
                # Encuentra el contorno más grande
                contour = max(contours, key=cv2.contourArea)

                # Encuentra las coordenadas del rectángulo delimitador del contorno
                x, y, w, h = cv2.boundingRect(contour)

                # Dibuja un rectángulo alrededor del contorno
                cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Encuentra el centro
                centro_x=x+w/2
                centro_y=y+h/2

                # Restar las coordenadas del rectángulo fijo para obtener las coordenadas relativas
                rec_x = centro_x - x1
                rec_y = centro_y - y1

                # Cálculo para las nuevas coordenadas en relación a la gráfica
                x_g = a*rec_x+b
                y_g = (c1*rec_y)+d

                # Muestra las coordenadas del objeto azul en la ventana
                print(f"Coordenadas (x, y) del centro del objeto azul: ({x_g}, {y_g})")

            cv2.imshow('Imagen Original', frame)
            cv2.imshow('Detección de color azul', res)
            
            # Revisa si se ha presionado ESC
            c = cv2.waitKey(5)
            if c == 27:
                break

    cv2.destroyAllWindows()