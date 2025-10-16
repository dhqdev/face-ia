import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

DATA_DIR = 'data'
CLASSES = ['sorrindo', 'neutro']
MODEL_FILENAME = 'smile_detector.pkl'

data = []
labels = []

# Carrega os dados dos arquivos CSV
for cls in CLASSES:
    path = os.path.join(DATA_DIR, cls)
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        df = pd.read_csv(filepath, header=None)
        data.append(df.values.flatten())
        labels.append(cls)

# Converte para DataFrame do Pandas
df = pd.DataFrame(data)
df['label'] = labels

# Separa os dados (X) e os rótulos (y)
X = df.drop('label', axis=1)
y = df['label']

# Divide os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Inicializa e treina o modelo
# RandomForest é um modelo robusto e bom para começar
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("Treinando o modelo...")
model.fit(X_train, y_train)
print("Treinamento concluído.")

# Avalia o modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo no conjunto de teste: {accuracy * 100:.2f}%")

# Salva o modelo treinado
joblib.dump(model, MODEL_FILENAME)
print(f"Modelo salvo como '{MODEL_FILENAME}'")