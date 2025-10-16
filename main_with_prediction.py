import cv2
import mediapipe as mp
import numpy as np
import joblib

# Carrega o modelo treinado
MODEL_FILENAME = 'smile_detector.pkl'
try:
    model = joblib.load(MODEL_FILENAME)
except FileNotFoundError:
    print(f"Erro: Arquivo do modelo '{MODEL_FILENAME}' não encontrado.")
    print("Por favor, execute o script 'train_model.py' primeiro.")
    exit()


# Inicializa MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Flip e converte a imagem
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Processa para encontrar os landmarks
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Desenha a malha
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
            
            # --- PREPARA OS DADOS PARA O MODELO ---
            landmarks = []
            for lm in face_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])
            
            # Converte para o formato que o modelo espera (array 2D)
            landmarks_for_prediction = np.array(landmarks).reshape(1, -1)
            
            # --- FAZ A PREVISÃO ---
            prediction = model.predict(landmarks_for_prediction)
            probability = model.predict_proba(landmarks_for_prediction)
            
            # Pega o nome da classe prevista e a sua confiança
            predicted_class = prediction[0]
            confidence = np.max(probability)

            # --- MOSTRA O RESULTADO NA TELA ---
            text = f"{predicted_class} ({confidence:.2f})"
            position = (50, 50)
            cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
            
    cv2.imshow('Detector de Sorriso', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()