import yt_dlp
import threading
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, Dict, Any

class VideoDownloader:
    """
    Clase que maneja toda la lógica de descarga de videos y playlists
    """
    
    def __init__(self, progress_callback: Optional[Callable] = None, 
                 log_callback: Optional[Callable] = None):
        """
        Constructor del descargador
        
        Args:
            progress_callback: Función que se llama durante el progreso de descarga
            log_callback: Función que se llama para registrar mensajes
        """
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.is_downloading = False
        self.download_thread = None
        self.current_download_path = "./descargas"
        
        # Crear carpeta de descargas por defecto
        Path(self.current_download_path).mkdir(exist_ok=True)
    
    def log_message(self, message: str):
        """
        Registra un mensaje usando el callback si está disponible
        """
        if self.log_callback:
            self.log_callback(message)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def set_download_path(self, path: str):
        """
        Establece la carpeta de descarga
        """
        self.current_download_path = path
        Path(path).mkdir(exist_ok=True)
        self.log_message(f"📁 Carpeta de descarga cambiada a: {path}")
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Obtiene información de un video o playlist sin descargarlo
        
        Args:
            url: URL del video o playlist
            
        Returns:
            Dict con la información extraída
        """
        try:
            self.log_message("🔍 Obteniendo información...")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:  # Es una playlist
                    return self._process_playlist_info(info)
                else:  # Es un video individual
                    return self._process_video_info(info)
                    
        except Exception as e:
            error_msg = f"❌ Error al obtener información: {str(e)}"
            self.log_message(error_msg)
            raise Exception(error_msg)
    
    def _process_video_info(self, info: Dict) -> Dict[str, Any]:
        """
        Procesa información de un video individual
        """
        processed_info = {
            'type': 'video',
            'title': info.get('title', 'Sin título'),
            'uploader': info.get('uploader', 'Desconocido'),
            'duration': info.get('duration', 0),
            'view_count': info.get('view_count', 'N/A'),
            'upload_date': info.get('upload_date', 'Desconocida'),
            'formats': []
        }
        
        # Extraer formatos disponibles
        if 'formats' in info:
            formats_seen = set()
            for fmt in info['formats']:
                if fmt.get('height'):
                    quality = f"{fmt['height']}p"
                    if quality not in formats_seen:
                        processed_info['formats'].append(quality)
                        formats_seen.add(quality)
        
        self._log_video_info(processed_info)
        return processed_info
    
    def _process_playlist_info(self, info: Dict) -> Dict[str, Any]:
        """
        Procesa información de una playlist
        """
        entries = info.get('entries', [])
        videos = []
        
        for i, entry in enumerate(entries, 1):
            if entry:
                video_info = {
                    'index': i,
                    'title': entry.get('title', f'Video {i}'),
                    'duration': entry.get('duration', 0)
                }
                videos.append(video_info)
        
        processed_info = {
            'type': 'playlist',
            'title': info.get('title', 'Sin título'),
            'uploader': info.get('uploader', 'Desconocido'),
            'total_videos': len(videos),
            'videos': videos
        }
        
        self._log_playlist_info(processed_info)
        return processed_info
    
    def _log_video_info(self, info: Dict):
        """
        Registra información de un video
        """
        self.log_message("=" * 50)
        self.log_message("📺 INFORMACIÓN DEL VIDEO")
        self.log_message("=" * 50)
        
        self.log_message(f"🎬 Título: {info['title']}")
        self.log_message(f"👤 Canal: {info['uploader']}")
        self.log_message(f"📅 Fecha de subida: {info['upload_date']}")
        
        if info['duration']:
            minutos = info['duration'] // 60
            segundos = info['duration'] % 60
            self.log_message(f"⏱️ Duración: {minutos}:{segundos:02d}")
        
        self.log_message(f"👀 Visualizaciones: {info['view_count']}")
        
        if info['formats']:
            self.log_message("🎥 Calidades disponibles:")
            for quality in info['formats']:
                self.log_message(f"   • {quality}")
    
    def _log_playlist_info(self, info: Dict):
        """
        Registra información de una playlist
        """
        self.log_message("=" * 50)
        self.log_message("📋 INFORMACIÓN DE LA PLAYLIST")
        self.log_message("=" * 50)
        
        self.log_message(f"📋 Título de la playlist: {info['title']}")
        self.log_message(f"👤 Canal: {info['uploader']}")
        self.log_message(f"🎥 Total de videos: {info['total_videos']}")
        self.log_message("")
        
        self.log_message("📝 Lista de videos:")
        for video in info['videos'][:10]:  # Solo primeros 10
            duration_str = ""
            if video['duration']:
                minutos = video['duration'] // 60
                segundos = video['duration'] % 60
                duration_str = f" ({minutos}:{segundos:02d})"
            
            self.log_message(f"   {video['index']:2d}. {video['title']}{duration_str}")
        
        if info['total_videos'] > 10:
            self.log_message(f"   ... y {info['total_videos'] - 10} videos más")
    
    def start_download(self, url: str, download_type: str = "single", 
                      quality: str = "720p", download_path: Optional[str] = None) -> bool:
        """
        Inicia una descarga
        
        Args:
            url: URL del video o playlist
            download_type: "single" o "playlist"
            quality: Calidad deseada
            download_path: Carpeta de descarga (opcional)
            
        Returns:
            True si la descarga se inició correctamente
        """
        if self.is_downloading:
            self.log_message("⚠️ Ya hay una descarga en progreso")
            return False
        
        if not url.strip():
            self.log_message("❌ URL vacía")
            return False
        
        if download_path:
            self.set_download_path(download_path)
        
        self.is_downloading = True
        
        # Iniciar descarga en hilo separado
        self.download_thread = threading.Thread(
            target=self._download_thread,
            args=(url, download_type, quality),
            daemon=True
        )
        self.download_thread.start()
        return True
    
    def _download_thread(self, url: str, download_type: str, quality: str):
        """
        Hilo de descarga
        """
        try:
            self.log_message("🚀 Iniciando descarga...")
            self.log_message(f"📎 URL: {url}")
            self.log_message(f"📥 Tipo: {'Playlist completa' if download_type == 'playlist' else 'Video individual'}")
            self.log_message(f"🎥 Calidad: {quality}")
            self.log_message(f"📁 Guardando en: {self.current_download_path}")
            self.log_message("-" * 50)
            
            ydl_opts = self._get_ydl_options(quality, download_type)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.log_message("✅ ¡Descarga completada exitosamente!")
            self.log_message(f"📁 Archivos guardados en: {self.current_download_path}")
            
            if self.progress_callback:
                self.progress_callback("completed", None)
                
        except Exception as e:
            error_msg = f"❌ Error durante la descarga: {str(e)}"
            self.log_message(error_msg)
            
            if self.progress_callback:
                self.progress_callback("error", error_msg)
        
        finally:
            self.is_downloading = False
            if self.progress_callback:
                self.progress_callback("finished", None)
    
    def _get_ydl_options(self, quality: str, download_type: str) -> Dict:
        """
        Configura las opciones de yt-dlp
        """
        ydl_opts = {
            'outtmpl': str(Path(self.current_download_path) / '%(title)s.%(ext)s'),
            'writeinfojson': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
        }
        
        # Configurar formato según calidad
        format_mapping = {
            "480p": 'best[height<=480]',
            "720p": 'best[height<=720]',
            "1080p": 'best[height<=1080]',
            "Mejor disponible": 'best',
            "Audio únicamente": 'bestaudio/best'
        }
        
        ydl_opts['format'] = format_mapping.get(quality, 'best[height<=720]')
        
        # Configurar para playlist
        if download_type == "playlist":
            ydl_opts['noplaylist'] = False
            ydl_opts['outtmpl'] = str(Path(self.current_download_path) / 
                                    '%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s')
        else:
            ydl_opts['noplaylist'] = True
        
        # Hook de progreso
        ydl_opts['progress_hooks'] = [self._progress_hook]
        
        return ydl_opts
    
    def _progress_hook(self, d: Dict):
        """
        Hook de progreso de yt-dlp
        """
        if d['status'] == 'downloading':
            filename = Path(d.get('filename', 'Archivo desconocido')).name
            
            progress_info = {
                'filename': filename,
                'status': 'downloading'
            }
            
            if 'total_bytes' in d and d['total_bytes']:
                downloaded = d.get('downloaded_bytes', 0)
                total = d['total_bytes']
                percent = (downloaded / total) * 100
                
                progress_info.update({
                    'percent': percent,
                    'downloaded_mb': downloaded / (1024 * 1024),
                    'total_mb': total / (1024 * 1024),
                    'speed_mbps': d.get('speed', 0) / (1024 * 1024) if d.get('speed') else 0
                })
                
                progress_msg = f"⬇️ {filename}: {percent:.1f}% ({progress_info['downloaded_mb']:.1f}/{progress_info['total_mb']:.1f} MB) - {progress_info['speed_mbps']:.1f} MB/s"
            else:
                downloaded_mb = d.get('downloaded_bytes', 0) / (1024 * 1024)
                progress_info['downloaded_mb'] = downloaded_mb
                progress_msg = f"⬇️ {filename}: {downloaded_mb:.1f} MB descargados"
            
            if self.progress_callback:
                self.progress_callback("progress", progress_info)
            else:
                # Fallback si no hay callback
                print(f"\r{progress_msg}", end="", flush=True)
                
        elif d['status'] == 'finished':
            filename = Path(d['filename']).name
            self.log_message(f"✅ Completado: {filename}")
            
            if self.progress_callback:
                self.progress_callback("file_completed", {'filename': filename})
    
    def cancel_download(self):
        """
        Cancela la descarga actual
        """
        if self.is_downloading:
            self.log_message("⚠️ Cancelando descarga...")
            self.log_message("ℹ️ La descarga actual se completará, pero no se iniciarán nuevas descargas")
            self.is_downloading = False
    
    def open_download_folder(self):
        """
        Abre la carpeta de descargas
        """
        try:
            download_path = Path(self.current_download_path)
            download_path.mkdir(exist_ok=True)
            
            if sys.platform.startswith('win'):
                os.startfile(download_path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{download_path}"')
            else:
                os.system(f'xdg-open "{download_path}"')
                
            self.log_message(f"📂 Abriendo carpeta: {download_path}")
            return True
            
        except Exception as e:
            error_msg = f"❌ Error al abrir carpeta: {str(e)}"
            self.log_message(error_msg)
            return False

def check_dependencies() -> bool:
    """
    Verifica que yt-dlp esté instalado
    """
    try:
        import yt_dlp
        return True
    except ImportError:
        print("❌ Error: yt-dlp no está instalado")
        print("Instala con: pip install yt-dlp")
        return False