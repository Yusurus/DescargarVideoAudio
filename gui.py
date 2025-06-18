import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
from datetime import datetime
from logic import VideoDownloader, check_dependencies
import os

# Importar la clase VideoDownloader del archivo anterior
# from video_downloader import VideoDownloader, check_dependencies

class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Videos - YouTube & Más")
        # Tamaño deseado de la ventana
        ancho_ventana = 800
        alto_ventana = 650

        # Obtener tamaño de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Calcular coordenadas para centrar
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)-20

        # Establecer tamaño y posición centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Configurar icono multiplataforma
        try:
            if os.path.exists("icono.ico"):
                self.root.iconbitmap("icono.ico")
            elif os.path.exists("icono.png"):
                # Para Linux/Mac
                icon = tk.PhotoImage(file="icono.png")
                self.root.iconphoto(True, icon)
        except:
            pass  # Si no encuentra el icono, continúa sin error
        
        # Configurar estilo
        self.setup_styles()
        
        # Inicializar el descargador
        self.downloader = VideoDownloader(
            progress_callback=self.on_progress_update,
            log_callback=self.log_message
        )
        
        # Variables de control
        self.current_info = None
        self.download_path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        
        # Crear la interfaz
        self.create_widgets()
        
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        
        # Configurar tema
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Colores personalizados
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Para que el notebook se expanda
        
        # Título
        title_label = ttk.Label(main_frame, text="🎥 Descargador de Videos", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Crear las pestañas
        self.create_main_tab()
        self.create_log_tab()
        
        # Sección de botones inferiores (fuera de las pestañas)
        self.create_bottom_buttons(main_frame)
    
    def create_main_tab(self):
        """Crea la pestaña principal con la funcionalidad de descarga"""
        # Frame para la pestaña principal
        main_tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(main_tab_frame, text="📥 Descargador")
        
        # Configurar grid del frame principal
        main_tab_frame.columnconfigure(1, weight=1)
        main_tab_frame.rowconfigure(2, weight=1)  # Para que la info se expanda
        
        # Sección de URL
        self.create_url_section(main_tab_frame)
        
        # Sección de información del video
        self.create_info_section(main_tab_frame)
        
        # Sección de configuración de descarga
        self.create_download_config_section(main_tab_frame)
        
        # Sección de progreso
        self.create_progress_section(main_tab_frame)
    
    def create_log_tab(self):
        """Crea la pestaña del registro de actividad"""
        # Frame para la pestaña de logs
        log_tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(log_tab_frame, text="📝 Registro")
        
        # Configurar grid
        log_tab_frame.columnconfigure(0, weight=1)
        log_tab_frame.rowconfigure(1, weight=1)
        
        # Título de la pestaña
        ttk.Label(log_tab_frame, text="📝 Registro de Actividad", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10)
        )
        
        # Área de logs
        self.log_text = scrolledtext.ScrolledText(
            log_tab_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            state=tk.DISABLED
        )
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configurar tags para logs
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("timestamp", foreground="gray")
        
        # Frame para botones de control del log
        log_buttons_frame = ttk.Frame(log_tab_frame)
        log_buttons_frame.grid(row=2, column=0, sticky=tk.E, pady=(5, 0))
        
        # Botones de control del log
        ttk.Button(log_buttons_frame, text="🗑️ Limpiar Log", command=self.clear_log).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_buttons_frame, text="💾 Guardar Log", command=self.save_log).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_buttons_frame, text="📋 Copiar Log", command=self.copy_log).pack(side=tk.LEFT)
    
    def create_url_section(self, parent):
        """Crea la sección de entrada de URL"""
        row = 0
        
        # URL Input
        ttk.Label(parent, text="🔗 URL del video o playlist:", style='Header.TLabel').grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 5)
        )
        
        url_frame = ttk.Frame(parent)
        url_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, font=('Arial', 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.analyze_btn = ttk.Button(url_frame, text="🔍 Analizar", command=self.analyze_url)
        self.analyze_btn.grid(row=0, column=1)
        
        self.clear_btn = ttk.Button(url_frame, text="🗑️ Limpiar", command=self.clear_url)
        self.clear_btn.grid(row=0, column=2, padx=(5, 0))
    
    def create_info_section(self, parent):
        """Crea la sección de información del video/playlist"""
        row = 2
        
        # Frame de información
        info_frame = ttk.LabelFrame(parent, text="📋 Información del Video/Playlist", padding="10")
        info_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # Área de texto para mostrar información
        self.info_text = scrolledtext.ScrolledText(
            info_frame, 
            height=12,
            wrap=tk.WORD,
            font=('Consolas', 9),
            state=tk.DISABLED
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para colores
        self.info_text.tag_configure("title", foreground="blue", font=('Consolas', 9, 'bold'))
        self.info_text.tag_configure("header", foreground="green", font=('Consolas', 9, 'bold'))
        self.info_text.tag_configure("warning", foreground="orange")
        self.info_text.tag_configure("error", foreground="red")
    
    def create_download_config_section(self, parent):
        """Crea la sección de configuración de descarga"""
        row = 3
        
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración de Descarga", padding="10")
        config_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        config_frame.columnconfigure(1, weight=1)
        
        # Tipo de descarga
        ttk.Label(config_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.download_type_var = tk.StringVar(value="single")
        type_frame = ttk.Frame(config_frame)
        type_frame.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(type_frame, text="📹 Video o audio individual", 
                       variable=self.download_type_var, value="single").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="📋 Playlist completa", 
                       variable=self.download_type_var, value="playlist").pack(side=tk.LEFT)
        
        # Calidad
        ttk.Label(config_frame, text="Calidad:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="720p")
        self.quality_combo = ttk.Combobox(config_frame, textvariable=self.quality_var, state="readonly", width=20)
        self.quality_combo['values'] = ("480p", "720p", "1080p", "Mejor disponible", "Audio únicamente")
        self.quality_combo.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # Carpeta de descarga
        ttk.Label(config_frame, text="Carpeta:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        
        folder_frame = ttk.Frame(config_frame)
        folder_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.download_path_var)
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_frame, text="📁 Examinar", command=self.browse_folder).grid(row=0, column=1)
        ttk.Button(folder_frame, text="📂 Abrir", command=self.open_folder).grid(row=0, column=2, padx=(5, 0))
    
    def create_progress_section(self, parent):
        """Crea la sección de progreso"""
        row = 4
        
        progress_frame = ttk.LabelFrame(parent, text="📊 Progreso de Descarga", padding="10")
        progress_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        # Etiqueta de estado
        self.status_label = ttk.Label(progress_frame, text="Listo para descargar")
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=400
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Información de progreso
        self.progress_info_label = ttk.Label(progress_frame, text="")
        self.progress_info_label.grid(row=2, column=0, sticky=tk.W)
    
    def create_bottom_buttons(self, parent):
        """Crea los botones inferiores"""
        row = 2
        
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, pady=(10, 0))
        
        # Botón de descarga principal
        self.download_btn = ttk.Button(
        button_frame, 
        text="⬇️ Iniciar Descarga", 
        command=self.start_download,
        style='Accent.TButton',
        state=tk.DISABLED  # Añadir esta línea
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de cancelar
        self.cancel_btn = ttk.Button(
            button_frame, 
            text="⏹️ Cancelar", 
            command=self.cancel_download,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de ayuda
        ttk.Button(
            button_frame, 
            text="❓ Ayuda", 
            command=self.show_help
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de acerca de
        ttk.Button(
            button_frame, 
            text="ℹ️ Acerca de", 
            command=self.show_about
        ).pack(side=tk.LEFT)
    
    def analyze_url(self):
        """Analiza la URL ingresada"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL válida")
            return
        
        # Deshabilitar botón durante análisis
        self.analyze_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(text="Analizando...")
        
        # Ejecutar análisis en hilo separado
        threading.Thread(target=self._analyze_thread, args=(url,), daemon=True).start()
    
    def _analyze_thread(self, url):
        """Hilo para analizar URL"""
        try:
            info = self.downloader.get_video_info(url)
            self.current_info = info
            
            # Actualizar UI en el hilo principal
            self.root.after(0, self._update_info_display, info)
            
        except Exception as e:
            self.root.after(0, self._show_analysis_error, str(e))
        finally:
            self.root.after(0, self._reset_analyze_button)
    
    def _update_info_display(self, info):
        """Actualiza la visualización de información"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if info['type'] == 'video':
            self._display_video_info(info)
        else:
            self._display_playlist_info(info)
        
        self.info_text.config(state=tk.DISABLED)
        
        # Actualizar calidades disponibles
        if info['type'] == 'video' and info['formats']:
            available_qualities = info['formats'] + ["Mejor disponible", "Audio únicamente"]
            self.quality_combo['values'] = available_qualities
            # Seleccionar una calidad por defecto que esté disponible
            if "720p" in available_qualities:
                self.quality_var.set("720p")
            elif available_qualities:
                self.quality_var.set(available_qualities[0])
        else:
            # Para playlists o cuando no hay formatos específicos, usar valores por defecto
            self.quality_combo['values'] = ("480p", "720p", "1080p", "Mejor disponible", "Audio únicamente")
            self.quality_var.set("720p")
        
        # Habilitar descarga
        self.download_btn.config(state=tk.NORMAL)
    
    def _display_video_info(self, info):
        """Muestra información de video individual"""
        self.info_text.insert(tk.END, "📺 INFORMACIÓN DEL VIDEO\n", "header")
        self.info_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.info_text.insert(tk.END, f"🎬 Título: ", "title")
        self.info_text.insert(tk.END, f"{info['title']}\n\n")
        
        self.info_text.insert(tk.END, f"👤 Canal: ", "title")
        self.info_text.insert(tk.END, f"{info['uploader']}\n\n")
        
        self.info_text.insert(tk.END, f"📅 Fecha: ", "title")
        self.info_text.insert(tk.END, f"{info['upload_date']}\n\n")
        
        if info['duration']:
            minutos = info['duration'] // 60
            segundos = info['duration'] % 60
            self.info_text.insert(tk.END, f"⏱️ Duración: ", "title")
            self.info_text.insert(tk.END, f"{minutos}:{segundos:02d}\n\n")
        
        self.info_text.insert(tk.END, f"👀 Visualizaciones: ", "title")
        self.info_text.insert(tk.END, f"{info['view_count']}\n\n")
        
        if info['formats']:
            self.info_text.insert(tk.END, "🎥 Calidades disponibles:\n", "title")
            for quality in info['formats']:
                self.info_text.insert(tk.END, f"   • {quality}\n")
    
    def _display_playlist_info(self, info):
        """Muestra información de playlist"""
        self.info_text.insert(tk.END, "📋 INFORMACIÓN DE LA PLAYLIST\n", "header")
        self.info_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.info_text.insert(tk.END, f"📋 Título: ", "title")
        self.info_text.insert(tk.END, f"{info['title']}\n\n")
        
        self.info_text.insert(tk.END, f"👤 Canal: ", "title")
        self.info_text.insert(tk.END, f"{info['uploader']}\n\n")
        
        self.info_text.insert(tk.END, f"🎥 Total de videos: ", "title")
        self.info_text.insert(tk.END, f"{info['total_videos']}\n\n")
        
        self.info_text.insert(tk.END, "📝 Lista de videos:\n", "title")
        
        for video in info['videos'][:15]:  # Mostrar primeros 15
            duration_str = ""
            if video['duration']:
                minutos = video['duration'] // 60
                segundos = video['duration'] % 60
                duration_str = f" ({minutos}:{segundos:02d})"
            
            self.info_text.insert(tk.END, f"   {video['index']:2d}. {video['title']}{duration_str}\n")
        
        if info['total_videos'] > 15:
            self.info_text.insert(tk.END, f"\n   ... y {info['total_videos'] - 15} videos más\n")
    
    def _show_analysis_error(self, error_msg):
        """Muestra error de análisis"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "❌ ERROR AL ANALIZAR URL\n", "error")
        self.info_text.insert(tk.END, "=" * 50 + "\n\n")
        self.info_text.insert(tk.END, f"{error_msg}\n\n")
        self.info_text.insert(tk.END, "Consejos:\n", "title")
        self.info_text.insert(tk.END, "• Verifica que la URL sea correcta\n")
        self.info_text.insert(tk.END, "• Asegúrate de tener conexión a internet\n")
        self.info_text.insert(tk.END, "• Algunos videos pueden estar restringidos\n")
        self.info_text.config(state=tk.DISABLED)
        
        messagebox.showerror("Error", f"No se pudo analizar la URL:\n{error_msg}")
    
    def _reset_analyze_button(self):
        """Restablece el botón de análisis"""
        self.analyze_btn.config(state=tk.NORMAL)
        self.analyze_btn.config(text="🔍 Analizar")
    
    def start_download(self):
        """Inicia la descarga"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL")
            return
        
        if not self.current_info:
            messagebox.showwarning("Advertencia", "Primero analiza la URL")
            return
        
        # Configurar UI para descarga
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_bar['value'] = 0
        self.status_label.config(text="Preparando descarga...")
        
        # Obtener configuración
        download_type = self.download_type_var.get()
        quality = self.quality_var.get()
        download_path = self.download_path_var.get()
        
        # Iniciar descarga
        success = self.downloader.start_download(
            url=url,
            download_type=download_type,
            quality=quality,
            download_path=download_path
        )
        
        if not success:
            self._reset_download_buttons()
            messagebox.showerror("Error", "No se pudo iniciar la descarga")
    
    def cancel_download(self):
        """Cancela la descarga actual"""
        self.downloader.cancel_download()
        self._reset_download_buttons()
    
    def _reset_download_buttons(self):
        """Restablece los botones de descarga"""
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Listo para descargar")
        self.progress_bar['value'] = 0
        self.progress_info_label.config(text="")
    
    def on_progress_update(self, status, data):
        """Callback para actualizaciones de progreso"""
        self.root.after(0, self._handle_progress_update, status, data)
    
    def _handle_progress_update(self, status, data):
        """Maneja las actualizaciones de progreso en el hilo principal"""
        if status == "progress" and data:
            # Actualizar barra de progreso
            if 'percent' in data:
                self.progress_bar['value'] = data['percent']
                info_text = f"⬇️ {data['filename']} - {data['percent']:.1f}%"
                if 'speed_mbps' in data:
                    info_text += f" - {data['speed_mbps']:.1f} MB/s"
                self.progress_info_label.config(text=info_text)
            else:
                self.progress_info_label.config(text=f"⬇️ {data['filename']} - {data['downloaded_mb']:.1f} MB")
            
            self.status_label.config(text="Descargando...")
            
        elif status == "file_completed":
            self.progress_bar['value'] = 100
            
        elif status == "completed":
            self.status_label.config(text="✅ Descarga completada")
            self.progress_bar['value'] = 100
            self.progress_info_label.config(text="")
            messagebox.showinfo("Éxito", "¡Descarga completada exitosamente!")
            
        elif status == "error":
            self.status_label.config(text="❌ Error en la descarga")
            messagebox.showerror("Error", f"Error durante la descarga:\n{data}")
            
        elif status == "finished":
            self._reset_download_buttons()
    
    def log_message(self, message):
        """Callback para mensajes de log"""
        self.root.after(0, self._add_log_message, message)
    
    def _add_log_message(self, message):
        """Añade un mensaje al log"""
        self.log_text.config(state=tk.NORMAL)
        
        # Añadir timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Determinar el tipo de mensaje y aplicar formato
        if "❌" in message or "Error" in message:
            tag = "error"
        elif "✅" in message or "completada" in message:
            tag = "success"
        elif "⚠️" in message or "Advertencia" in message:
            tag = "warning"
        else:
            tag = "info"
        
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Cambiar automáticamente a la pestaña de registro si hay un error
        if tag == "error":
            self.notebook.select(1)  # Seleccionar la pestaña de registro (índice 1)
    
    def clear_log(self):
        """Limpia el área de logs"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def save_log(self):
        """Guarda el log en un archivo"""
        filename = filedialog.asksaveasfilename(
            title="Guardar registro",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    log_content = self.log_text.get(1.0, tk.END)
                    f.write(log_content)
                messagebox.showinfo("Éxito", "Registro guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el registro:\n{e}")
    
    def copy_log(self):
        """Copia el log al portapapeles"""
        try:
            log_content = self.log_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(log_content)
            messagebox.showinfo("Éxito", "Registro copiado al portapapeles")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar el registro:\n{e}")
    
    def clear_url(self):
        """Limpia la URL y la información"""
        self.url_entry.delete(0, tk.END)
        self.current_info = None
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        # Restablecer calidades por defecto
        self.quality_combo['values'] = ("480p", "720p", "1080p", "Mejor disponible", "Audio únicamente")
        self.quality_var.set("720p")
    
    def browse_folder(self):
        """Abre el diálogo para seleccionar carpeta"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta de descarga",
            initialdir=self.download_path_var.get()
        )
        
        if folder:
            self.download_path_var.set(folder)
    
    def open_folder(self):
        """Abre la carpeta de descargas"""
        success = self.downloader.open_download_folder()
        if not success:
            messagebox.showerror("Error", "No se pudo abrir la carpeta de descargas")
    
    def show_help(self):
        """Muestra la ayuda"""
        help_text = """
🎥 DESCARGADOR DE VIDEOS - AYUDA

CÓMO USAR:
1. Pega una URL de YouTube, Vimeo u otras plataformas compatibles
2. Haz clic en "Analizar" para ver la información del video/playlist
3. Selecciona el tipo de descarga (individual o playlist)
4. Elige la calidad deseada
5. Selecciona la carpeta de destino
6. Haz clic en "Iniciar Descarga"

PESTAÑAS:
• Descargador: Funcionalidad principal para descargar videos
• Registro: Historial detallado de todas las actividades y errores

TIPOS DE DESCARGA:
• Video individual: Descarga solo el video de la URL
• Playlist completa: Descarga todos los videos de la playlist

CALIDADES DISPONIBLES:
• 480p, 720p, 1080p: Resoluciones específicas
• Mejor disponible: La mejor calidad disponible
• Audio únicamente: Solo el audio del video

CONSEJOS:
• Verifica tu conexión a internet antes de descargar
• Las descargas grandes pueden tomar tiempo
• Puedes cancelar descargas en progreso
• Los archivos se guardan con nombres descriptivos

FORMATOS COMPATIBLES:
YouTube, Vimeo, Dailymotion, SoundCloud y muchas más
plataformas compatibles con yt-dlp.
        """
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Cerrar", command=help_window.destroy).pack(pady=10)
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """
🎥 DESCARGADOR DE VIDEOS
Versión 1.0

Una aplicación simple y poderosa para descargar videos
y playlists de múltiples plataformas de internet.

CARACTERÍSTICAS:
• Descarga videos individuales o playlists completas
• Múltiples calidades disponibles
• Interfaz intuitiva y moderna
• Soporte para múltiples plataformas
• Progreso de descarga en tiempo real
• Gestión de carpetas de descarga

TECNOLOGÍA:
• Python 3.x
• tkinter (interfaz gráfica)
• yt-dlp (motor de descarga)

DESARROLLADO CON ❤️ POR:
>>Yusurus<<
     correo: yjru_at@hotmail.com
        """        
        messagebox.showinfo("Acerca de", about_text)
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.downloader.is_downloading:
            if messagebox.askokcancel("Cerrar aplicación", 
                                    "Hay una descarga en progreso. ¿Deseas cancelarla y cerrar la aplicación?"):
                self.downloader.cancel_download()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Función principal"""
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Crear aplicación
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    
    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()