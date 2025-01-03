import cv2
import mediapipe as mp

# Inicialización de Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Captura de video desde la cámara
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a RGB (Mediapipe funciona con imágenes RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para detectar los puntos clave
    result = pose.process(rgb_frame)

    # Dibujar los puntos clave y las conexiones entre ellos
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Mostrar la imagen con los puntos clave
    cv2.imshow('Body Pose Detection', frame)

    # Salir del loop si se presiona la tecla 'q' o se cierra la ventana
    if cv2.getWindowProperty('Body Pose Detection', cv2.WND_PROP_VISIBLE) < 1:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
