import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Simulación de acciones de música
def perform_action(action):
    if action == "Pausa/Reproducir":
        print("Pausar/Reproducir música")
    elif action == "Siguiente":
        print("Siguiente canción")
    elif action == "Anterior":
        print("Canción anterior")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Calcular gestos
            landmarks = hand_landmarks.landmark
            fingers_up = sum(landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20])  # Dedos levantados

            # Mapear gestos a acciones
            if fingers_up == 0:
                action = "Pausa/Reproducir"
            elif fingers_up == 1:
                action = "Siguiente"
            elif fingers_up == 2:
                action = "Anterior"
            else:
                action = None
            if action:
                perform_action(action)
                cv2.putText(image, f"Accion: {action}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Controlador de Musica", image)
    if cv2.waitKey(1) & 0xFF == 27:  # Salir con ESC
        break

cap.release()
cv2.destroyAllWindows() 