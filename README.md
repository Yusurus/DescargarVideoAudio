# 🎥 Descargador de Videos

Una aplicación de escritorio moderna y fácil de usar para descargar videos y playlists de YouTube, Vimeo y muchas otras plataformas de video.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 📋 Características

- ✅ **Múltiples plataformas**: YouTube, Vimeo, Dailymotion, SoundCloud y más
- ✅ **Videos individuales y playlists**: Descarga un solo video o toda una playlist
- ✅ **Múltiples calidades**: 480p, 720p, 1080p, mejor disponible, solo audio
- ✅ **Interfaz gráfica intuitiva**: Diseño moderno con pestañas organizadas
- ✅ **Progreso en tiempo real**: Visualiza el progreso de descarga con detalles
- ✅ **Registro detallado**: Historial completo de todas las operaciones
- ✅ **Gestión de carpetas**: Selecciona donde guardar tus descargas
- ✅ **Análisis previo**: Ve información del video antes de descargarlo

## 🖼️ Capturas de Pantalla

### Pestaña Principal - Descargador
- Entrada de URL con análisis automático
- Información detallada del video/playlist
- Configuración de calidad y tipo de descarga
- Barra de progreso en tiempo real

### Pestaña de Registro
- Historial completo de actividades
- Mensajes con códigos de color
- Opciones para guardar y copiar logs

## 🚀 Instalación

### Requisitos del Sistema
- Python 3.7 o superior
- Sistema operativo: Windows, macOS o Linux

### Instalación Rápida

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/descargador-videos.git
   cd descargador-videos
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**:
   ```bash
   python gui.py
   ```

### Instalación con Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python gui.py
```

## 📖 Cómo Usar

### Pasos Básicos

1. **Pega la URL**: Copia y pega la URL del video o playlist en el campo correspondiente
2. **Analiza**: Haz clic en "🔍 Analizar" para obtener información del contenido
3. **Configura**: Selecciona el tipo de descarga, calidad y carpeta de destino
4. **Descarga**: Haz clic en "⬇️ Iniciar Descarga" y espera a que termine

### Tipos de Descarga

- **📹 Video individual**: Descarga solo el video de la URL proporcionada
- **📋 Playlist completa**: Descarga todos los videos de la playlist

### Calidades Disponibles

- **480p**: Resolución estándar, archivos más pequeños
- **720p**: Alta definición, balance entre calidad y tamaño
- **1080p**: Full HD, mejor calidad visual
- **Mejor disponible**: La mayor calidad que ofrezca el video
- **Audio únicamente**: Solo descarga el audio (MP3/M4A)

### Funciones Adicionales

- **📁 Examinar**: Selecciona una carpeta personalizada para las descargas
- **📂 Abrir**: Abre la carpeta de descargas actual
- **⏹️ Cancelar**: Cancela la descarga en progreso
- **🗑️ Limpiar**: Limpia la URL y reinicia la interfaz

## 🏗️ Estructura del Proyecto

```
descargador-videos/
├── gui.py              # Interfaz gráfica principal
├── logic.py            # Lógica de descarga y procesamiento
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Este archivo
└── descargas/         # Carpeta por defecto para descargas
```

### Descripción de Archivos

- **`gui.py`**: Contiene toda la interfaz gráfica usando tkinter, maneja eventos de usuario y actualiza la UI
- **`logic.py`**: Implementa la clase `VideoDownloader` con toda la lógica de descarga usando yt-dlp
- **`requirements.txt`**: Lista las dependencias necesarias (yt-dlp)

## ⚙️ Configuración Avanzada

### Personalizar Rutas de Descarga

Por defecto, los archivos se guardan en la carpeta `./descargas`. Puedes cambiar esto:

1. Usando la interfaz: Botón "📁 Examinar"
2. Modificando la variable `download_path_var` en el código

### Formatos de Archivo

La aplicación guarda los archivos con nombres descriptivos:
- **Videos individuales**: `Título del video.extensión`
- **Playlists**: `Nombre de Playlist/01 - Título del video.extensión`

## 🔧 Solución de Problemas

### Problemas Comunes

**Error: "yt-dlp no está instalado"**
```bash
pip install yt-dlp
```

**Error: "No se pudo analizar la URL"**
- Verifica que la URL sea correcta y esté completa
- Comprueba tu conexión a internet
- Algunos videos pueden tener restricciones geográficas

**Descarga lenta**
- La velocidad depende de tu conexión a internet
- Servidores de video pueden limitar la velocidad
- Prueba en horarios de menor tráfico

**Error de permisos en carpeta**
- Asegúrate de tener permisos de escritura en la carpeta seleccionada
- Ejecuta como administrador si es necesario (Windows)

### Registro de Errores

La aplicación incluye un sistema de logging detallado:
- Ve a la pestaña "📝 Registro" para ver todos los mensajes
- Los errores aparecen en rojo
- Puedes guardar o copiar los logs para soporte técnico

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar el proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Ideas para Contribuir

- [ ] Soporte para más plataformas de video
- [ ] Descarga de subtítulos automáticos
- [ ] Conversión de formatos de video
- [ ] Interfaz en múltiples idiomas
- [ ] Modo oscuro/claro
- [ ] Descarga programada
- [ ] Integración con gestores de descargas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Descargo de Responsabilidad

Esta aplicación es solo para uso educativo y personal. Respeta los términos de servicio de las plataformas de video y los derechos de autor del contenido. El desarrollador no se hace responsable del uso indebido de esta herramienta.

## 🙏 Reconocimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - El motor de descarga que hace posible todo esto
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Para la interfaz gráfica
- Comunidad de Python por las librerías y recursos

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
- 📧 Contacto: yjru_at@hotmail.com

---

**¡Disfruta descargando tus videos favoritos! 🎬**