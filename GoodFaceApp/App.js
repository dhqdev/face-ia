import React, { useState, useEffect } from 'react';
import {
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Button,
} from 'react-native';
// 1. IMPORT CORRETO for SafeAreaView
import { SafeAreaView } from 'react-native-safe-area-context'; 
import { CameraView, useCameraPermissions } from 'expo-camera'; // 2. IMPORT CORRETO for CameraView

export default function App() {
  const [isFilterActive, setIsFilterActive] = useState(false);
  const [permission, requestPermission] = useCameraPermissions();

  useEffect(() => {
    requestPermission();
  }, []);

  const handleFilterToggle = () => {
    setIsFilterActive(previousState => !previousState);
  };

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.permissionContainer}>
        <Text style={styles.permissionText}>Precisamos da sua permissão para usar a câmera</Text>
        <Button onPress={requestPermission} title="Conceder Permissão" />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle={'light-content'} />
      <View style={styles.header}>
        <Text style={styles.title}>Good-Face</Text>
        <Text style={styles.subtitle}>Seu estúdio de AR pessoal</Text>
      </View>

      <View style={styles.cameraContainer}>
        {/* 3. USO CORRETO do componente CameraView e da prop 'facing' */}
        <CameraView style={styles.camera} facing="front">
          {isFilterActive && (
            <View style={styles.filterOverlay}>
              <Text style={styles.filterText}>FILTRO ATIVO</Text>
            </View>
          )}
        </CameraView>
      </View>

      <View style={styles.controls}>
        <TouchableOpacity style={styles.button} onPress={handleFilterToggle}>
          <Text style={styles.buttonText}>
            {isFilterActive ? 'Remover Filtro' : 'Aplicar Filtro'}
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  header: {
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  subtitle: {
    fontSize: 16,
    color: '#AAAAAA',
  },
  cameraContainer: {
    flex: 1,
    marginHorizontal: 20,
    borderRadius: 15,
    overflow: 'hidden',
    marginBottom: 10,
  },
  camera: {
    flex: 1,
  },
  controls: {
    padding: 20,
  },
  button: {
    backgroundColor: '#1E90FF',
    paddingVertical: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#121212',
    padding: 20,
  },
  permissionText: {
    color: 'white',
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  filterOverlay: {
    position: 'absolute',
    top: 20,
    left: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    padding: 10,
    borderRadius: 5,
  },
  filterText: {
    color: 'white',
    fontWeight: 'bold',
  }
});