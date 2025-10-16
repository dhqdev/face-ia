import cv2
import mediapipe as mp
import csv
import os

# Define os nomes das classes (pastas e labels)
CLASS_NAME_1 = "sorrindo"
CLASS_NAME_2 = "neutro"

# Cria as pastas se não existirem
os.makedirs(f"data/{CLASS_NAME_1}", exist_ok=True)
os.makedirs(f"data/{CLASS_NAME_2}", exist_ok=True)

# Inicializa MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Contadores para os arquivos
count_smile = 0
count_neutral = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    # Desenha anotações e mostra instruções na tela
    image = cv2.flip(image, 1) # Flip para efeito espelho
    cv2.putText(image, "Pressione 's' para salvar 'sorrindo'", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(image, "Pressione 'n' para salvar 'neutro'", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(image, f"Sorrindo: {count_smile} | Neutro: {count_neutral}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    key = cv2.waitKey(5) & 0xFF

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        landmarks = []
        for lm in face_landmarks.landmark:
            # Apenas x e y são suficientes para começar
            landmarks.extend([lm.x, lm.y])

        # Se uma tecla for pressionada, salva os dados
        if key == ord('s'):
            with open(f"data/{CLASS_NAME_1}/{count_smile}.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(landmarks)
            count_smile += 1
            print(f"Salvo {CLASS_NAME_1} amostra {count_smile}")

        if key == ord('n'):
            with open(f"data/{CLASS_NAME_2}/{count_neutral}.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(landmarks)
            count_neutral += 1
            print(f"Salvo {CLASS_NAME_2} amostra {count_neutral}")

    cv2.imshow('Coleta de Dados', image)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()