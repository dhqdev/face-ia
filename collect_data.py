import cv2
import mediapipe as mp
import csv
import os

# --- MUDANÇA AQUI: Adicionamos as novas classes ---
CLASSES = {
    's': "sorrindo",
    'n': "neutro",
    'u': "surpreso",
    't': "triste"
}

# Cria as pastas para todas as classes se não existirem
for class_name in CLASSES.values():
    os.makedirs(f"data/{class_name}", exist_ok=True)

# Inicializa MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Verifica se já existe uma instância rodando
lock_file = '/tmp/collect_data.lock'
if os.path.exists(lock_file):
    print("Outra instância já está rodando. Feche a anterior antes de iniciar uma nova.")
    cap.release()
    exit()

# Cria o arquivo de lock
with open(lock_file, 'w') as f:
    f.write(str(os.getpid()))

# Cria a janela uma vez
cv2.namedWindow('Coleta de Dados - Múltiplas Emoções')

# Contadores para os arquivos
counts = {class_name: 0 for class_name in CLASSES.values()}

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    # Flip para efeito espelho
    image = cv2.flip(image, 1)

    # --- MUDANÇA AQUI: Novas instruções na tela ---
    cv2.putText(image, "Pressione a tecla correspondente para salvar:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, "'s' -> sorrindo", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(image, "'n' -> neutro", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(image, "'u' -> surpreso", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(image, "'t' -> triste", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    status_text = f"Sorrindo: {counts['sorrindo']} | Neutro: {counts['neutro']} | Surpreso: {counts['surpreso']} | Triste: {counts['triste']}"
    cv2.putText(image, status_text, (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    key = cv2.waitKey(5) & 0xFF

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        landmarks = []
        for lm in face_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])

        # --- MUDANÇA AQUI: Lógica para salvar qualquer uma das classes ---
        key_char = chr(key)
        if key_char in CLASSES:
            class_name = CLASSES[key_char]
            
            # Salva os dados
            file_path = f"data/{class_name}/{counts[class_name]}.csv"
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(landmarks)
            
            counts[class_name] += 1
            print(f"Salvo amostra para '{class_name}' (Total: {counts[class_name]})")

    cv2.imshow('Coleta de Dados - Múltiplas Emoções', image)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Remove o arquivo de lock
os.remove(lock_file)