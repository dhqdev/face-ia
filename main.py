import cv2
import mediapipe as mp

# Inicializa os módulos do MediaPipe que vamos usar
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Configurações para o desenho da malha
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Inicializa a captura de vídeo (webcam). O '0' geralmente se refere à webcam padrão.
cap = cv2.VideoCapture(0)

# Inicia o detector de malha facial do MediaPipe
with mp_face_mesh.FaceMesh(
    max_num_faces=1, # Detectar no máximo 1 rosto
    refine_landmarks=True, # Melhora a precisão dos landmarks dos lábios, olhos e íris
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

  while cap.isOpened():
    # Lê um frame da webcam
    success, image = cap.read()
    if not success:
      print("Ignorando frame vazio da câmera.")
      continue

    # Para melhorar a performance, marcamos a imagem como não-gravável
    # --- LINHA CORRIGIDA ---
    image.flags.writeable = False 
    
    # Converte a imagem de BGR (padrão do OpenCV) para RGB (padrão do MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Processa a imagem e detecta a malha facial
    results = face_mesh.process(image_rgb)

    # Torna a imagem gravável novamente para podermos desenhar sobre ela
    # --- LINHA CORRIGIDA ---
    image.flags.writeable = True 
    
    # Desenha a malha facial na imagem original
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        # Desenha a tesselação (a malha principal)
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
            
        # Desenha os contornos do rosto, lábios, olhos e sobrancelhas
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())

        # Desenha os landmarks da íris (se refine_landmarks=True)
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())

    # Mostra a imagem resultante em uma janela
    # Flip a imagem horizontalmente para um efeito de espelho
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))

    # Para o programa se a tecla 'q' for pressionada
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break

# Libera a webcam e fecha as janelas
cap.release()
cv2.destroyAllWindows()