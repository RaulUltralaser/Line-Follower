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

if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.5
    
    # Itera hasta que se presione ESC
    while True:
            frame = get_frame(cap, scaling_factor)
            
            # Convierte el color a HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # # # Aquí se define el color azul rn el espacio de HSV
            # lower = np.array([60,100,100])
            # upper = np.array([180,255,255])
                    
            # Aquí se define cualquier color en el espacio de HSV
            lower = np.array([73,50,50])        
            upper = np.array([93,255,255])        

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