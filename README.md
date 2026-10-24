# Quasar

Aplicación Android de tutoría académica con una experiencia enfocada en matemáticas. Quasar combina formularios de resolución, visualización de ecuaciones, gráficas y motores de cálculo en Python.

## Funciones

- Resolución guiada de ejercicios de matemáticas, probabilidad, física y química.
- Teclado matemático y renderizado de expresiones con KaTeX, sin depender de conexión.
- Graficadora de funciones con vista de ejes y coordenadas.
- Motor de razonamiento y pasos de cálculo basado en Python y SymPy.
- Interfaz nativa Android con temática neón y recursos propios de la app.

## Tecnología

- Kotlin y Android Views
- Gradle y Android SDK 34
- Chaquopy para ejecutar Python en Android
- Python 3.14 y SymPy
- KaTeX para ecuaciones matemáticas

## Abrir el proyecto

1. Abre esta carpeta en Android Studio.
2. Configura un SDK de Android 34 y Java 17.
3. Revisa `app/build.gradle`: Chaquopy necesita un intérprete Python local compatible para el proceso de compilación.
4. Sincroniza Gradle y ejecuta la app en un emulador o dispositivo Android con API 24 o superior.

## Estructura

```
app/src/main/java/     Pantallas y componentes Kotlin
app/src/main/python/   Motores de cálculo y materias
app/src/main/assets/   KaTeX y recursos locales
app/src/main/res/      Diseño, colores, iconos y animaciones
```

## Nota

El repositorio excluye configuración local, resultados de compilación y cachés. Ajusta la ruta de Python en `app/build.gradle` a tu entorno antes de compilar.
