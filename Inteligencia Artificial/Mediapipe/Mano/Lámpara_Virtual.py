import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands y otras configuraciones
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar intensidad de la lámpara
lamp_intensity = 0  # Intensidad inicial

def draw_lamp_on_image(image, intensity):
    """Dibuja la lámpara en la imagen en la esquina inferior derecha."""
    lamp_image = np.zeros((200, 200, 3), dtype=np.uint8)  # Tamaño pequeño para la lámpara
    brightness = int(255 * intensity)
    cv2.circle(lamp_image, (100, 100), 80, (brightness, brightness, 0), -1)  # Lámpara en el centro de la imagen pequeña

    # Definir posición de la lámpara en la imagen principal (esquina inferior derecha)
    h, w, _ = image.shape
    x_offset = w - 210  # Espaciado de la lámpara desde el borde derecho
    y_offset = h - 210  # Espaciado de la lámpara desde el borde inferior

    # Superponer la imagen de la lámpara sobre la imagen de la cámara
    image[y_offset:y_offset+200, x_offset:x_offset+200] = lamp_image
    return image

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("No se pudo acceder a la cámara.")
        break

    # Preprocesar la imagen
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para obtener puntos clave de la mano
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar puntos clave y conexiones en la imagen
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtener coordenadas del dedo índice
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_finger_tip.x * image.shape[1]), int(index_finger_tip.y * image.shape[0])

            # Mapear posición vertical del dedo índice a intensidad de luz
            lamp_intensity = max(0, min(1, 1 - index_finger_tip.y))

            # Dibujar la lámpara en la imagen de la cámara
            image = draw_lamp_on_image(image, lamp_intensity)

            # Mostrar coordenadas en pantalla
            cv2.putText(image, f"Intensidad: {lamp_intensity:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar la imagen con los puntos clave de la mano y la lámpara
    cv2.imshow('Detección de Manos y Lámpara', image)

    if cv2.waitKey(1) & 0xFF == 27:  # Presionar ESC para salir
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
