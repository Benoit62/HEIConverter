import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener
import os
import shutil
import sys
from ctypes import windll
from pathlib import Path

register_heif_opener()

def get_resource_path(relative_path):
    """Obtient le chemin vers une ressource, que ce soit en mode dev ou exe"""
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # En mode développement, utilise le répertoire du script
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class ModernHEICConverter:
    def __init__(self):
        self.root = tk.Tk()
        # Après self.root = tk.Tk()
        self.root.after(100, lambda: self.root.iconbitmap(get_resource_path('logo.ico')))
        self.setup_window()
        self.create_variables()
        self.create_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configuration de la fenêtre principale avec un design moderne"""

        try:
            # Définit un ID unique pour l'application
            myappid = 'benoitwattinne.heicconverter.version1.0'
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
            
        self.root.title("HEIC Converter Pro")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Couleurs modernes - thème sombre élégant
        self.colors = {
            'bg_primary': '#1e1e1e',      # Noir moderne
            'bg_secondary': '#2d2d2d',    # Gris foncé
            'bg_tertiary': '#3d3d3d',     # Gris moyen
            'accent': '#0078d4',          # Bleu Microsoft moderne
            'accent_hover': '#106ebe',    # Bleu hover
            'success': '#16c60c',         # Vert moderne
            'warning': '#ff8c00',         # Orange
            'error': '#d83b01',           # Rouge moderne
            'text_primary': '#ffffff',    # Blanc
            'text_secondary': '#cccccc',  # Gris clair
            'text_muted': '#8a8a8a'       # Gris moyen
        }
        
        self.root.configure(bg=self.colors['bg_primary'])

        try:
            self.root.iconbitmap(get_resource_path('logo.ico'))
        except:
            print("Impossible de charger l'icône .ico")
        
    def create_variables(self):
        """Création des variables tkinter"""
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.auto_folder_output = tk.BooleanVar(value=True)
        self.output_location = tk.StringVar(value="parent")  # "parent" ou "custom"
        
    def create_styles(self):
        """Configuration des styles modernes"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Style pour les boutons
        self.style.configure('Modern.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['accent_hover']),
                                ('pressed', self.colors['accent_hover'])])
        
        # Style pour la barre de progression
        self.style.configure('Modern.TProgressbar',
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_tertiary'],
                           borderwidth=0,
                           lightcolor=self.colors['accent'],
                           darkcolor=self.colors['accent'])
        
    def create_widgets(self):
        """Création de l'interface utilisateur moderne"""
        # Container principal avec padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre principal
        title_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        title_frame.pack(fill='x', pady=(0, 30))
        
        title_label = tk.Label(title_frame, 
                              text="🔄 HEIC Converter Pro",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Convertissez vos images HEIC en JPEG facilement",
                                 font=('Segoe UI', 11),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(5, 0))
        
        # Section dossier d'entrée
        self.create_input_section(main_container)
        
        # Section dossier de sortie
        self.create_output_section(main_container)
        
        # Section options
        self.create_options_section(main_container)
        
        # Bouton de conversion
        self.create_conversion_button(main_container)
        
        # Barre de progression
        self.create_progress_section(main_container)
        
        # Zone de logs
        self.create_logs_section(main_container)
        
    def create_input_section(self, parent):
        """Section pour le dossier d'entrée"""
        input_frame = tk.LabelFrame(parent,
                                   text=" 📁 Dossier d'entrée ",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   bd=0,
                                   relief='flat')
        input_frame.pack(fill='x', pady=(0, 20))
        
        entry_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        entry_frame.pack(fill='x', padx=15, pady=15)
        
        self.input_entry = tk.Entry(entry_frame,
                                   textvariable=self.input_folder,
                                   font=('Segoe UI', 11),
                                   bg=self.colors['bg_tertiary'],
                                   fg=self.colors['text_primary'],
                                   bd=0,
                                   relief='flat',
                                   insertbackground=self.colors['text_primary'])
        self.input_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        browse_input_btn = tk.Button(entry_frame,
                                    text="📂 Parcourir",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg=self.colors['accent'],
                                    fg=self.colors['text_primary'],
                                    bd=0,
                                    relief='flat',
                                    cursor='hand2',
                                    command=self.browse_input_folder)
        browse_input_btn.pack(side='right', padx=(10, 0), ipady=8, ipadx=15)
        
    def create_output_section(self, parent):
        """Section pour le dossier de sortie"""
        output_frame = tk.LabelFrame(parent,
                                    text=" 💾 Dossier de sortie ",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    bd=0,
                                    relief='flat')
        output_frame.pack(fill='x', pady=(0, 20))
        
        # Options de choix automatique
        auto_frame = tk.Frame(output_frame, bg=self.colors['bg_secondary'])
        auto_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        auto_check = tk.Checkbutton(auto_frame,
                                   text="Choix automatique du dossier de sortie",
                                   variable=self.auto_folder_output,
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   selectcolor=self.colors['bg_tertiary'],
                                   activebackground=self.colors['bg_secondary'],
                                   activeforeground=self.colors['text_primary'],
                                   command=self.toggle_output_options)
        auto_check.pack(anchor='w')
        
        # Choix de l'emplacement
        location_frame = tk.Frame(output_frame, bg=self.colors['bg_secondary'])
        location_frame.pack(fill='x', padx=30, pady=(0, 10))
        
        tk.Radiobutton(location_frame,
                      text="Dans le dossier parent du dossier d'entrée",
                      variable=self.output_location,
                      value="parent",
                      font=('Segoe UI', 9),
                      bg=self.colors['bg_secondary'],
                      fg=self.colors['text_secondary'],
                      selectcolor=self.colors['bg_tertiary'],
                      activebackground=self.colors['bg_secondary'],
                      activeforeground=self.colors['text_secondary']).pack(anchor='w')
        
        tk.Radiobutton(location_frame,
                      text="Dans le dossier d'entrée",
                      variable=self.output_location,
                      value="current",
                      font=('Segoe UI', 9),
                      bg=self.colors['bg_secondary'],
                      fg=self.colors['text_secondary'],
                      selectcolor=self.colors['bg_tertiary'],
                      activebackground=self.colors['bg_secondary'],
                      activeforeground=self.colors['text_secondary']).pack(anchor='w')
        
        # Champ de saisie du dossier de sortie
        self.output_entry_frame = tk.Frame(output_frame, bg=self.colors['bg_secondary'])
        self.output_entry_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        self.output_entry = tk.Entry(self.output_entry_frame,
                                    textvariable=self.output_folder,
                                    font=('Segoe UI', 11),
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    bd=0,
                                    relief='flat',
                                    insertbackground=self.colors['text_primary'],
                                    state='disabled')
        self.output_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        self.browse_output_btn = tk.Button(self.output_entry_frame,
                                          text="📂 Parcourir",
                                          font=('Segoe UI', 10, 'bold'),
                                          bg=self.colors['bg_tertiary'],
                                          fg=self.colors['text_muted'],
                                          bd=0,
                                          relief='flat',
                                          state='disabled',
                                          command=self.browse_output_folder)
        self.browse_output_btn.pack(side='right', padx=(10, 0), ipady=8, ipadx=15)
        
    def create_options_section(self, parent):
        """Section des options"""
        options_frame = tk.LabelFrame(parent,
                                     text=" ⚙️ Options ",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     bd=0,
                                     relief='flat')
        options_frame.pack(fill='x', pady=(0, 20))
        
        options_content = tk.Frame(options_frame, bg=self.colors['bg_secondary'])
        options_content.pack(fill='x', padx=15, pady=15)
        
        # Placeholder pour futures options
        tk.Label(options_content,
                text="Qualité JPEG : Élevée | Format de sortie : .jpg",
                font=('Segoe UI', 9),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_muted']).pack(anchor='w')
        
    def create_conversion_button(self, parent):
        """Bouton de conversion principal"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        button_frame.pack(fill='x', pady=(0, 20))
        
        self.convert_btn = tk.Button(button_frame,
                                    text="🚀 Démarrer la conversion",
                                    font=('Segoe UI', 14, 'bold'),
                                    bg=self.colors['accent'],
                                    fg=self.colors['text_primary'],
                                    bd=0,
                                    relief='flat',
                                    cursor='hand2',
                                    command=self.start_conversion)
        self.convert_btn.pack(pady=10, ipady=12, ipadx=30)
        
        # Effet hover pour le bouton
        def on_enter(e):
            self.convert_btn.configure(bg=self.colors['accent_hover'])
        def on_leave(e):
            self.convert_btn.configure(bg=self.colors['accent'])
            
        self.convert_btn.bind("<Enter>", on_enter)
        self.convert_btn.bind("<Leave>", on_leave)
        
    def create_progress_section(self, parent):
        """Section de progression"""
        progress_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        progress_frame.pack(fill='x', pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           mode='determinate',
                                           length=400)
        self.progress_bar.pack(pady=(0, 5))
        
        self.progress_label = tk.Label(progress_frame,
                                      text="Prêt à convertir",
                                      font=('Segoe UI', 10),
                                      bg=self.colors['bg_primary'],
                                      fg=self.colors['text_secondary'])
        self.progress_label.pack()
        
        self.stats_label = tk.Label(progress_frame,
                                   text="",
                                   font=('Segoe UI', 9),
                                   bg=self.colors['bg_primary'],
                                   fg=self.colors['text_muted'])
        self.stats_label.pack(pady=(5, 0))
        
    def create_logs_section(self, parent):
        """Section des logs"""
        logs_frame = tk.LabelFrame(parent,
                                  text=" 📋 Journal de conversion ",
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_primary'],
                                  bd=0,
                                  relief='flat')
        logs_frame.pack(fill='both', expand=True)
        
        # Zone de texte avec scrollbar
        text_frame = tk.Frame(logs_frame, bg=self.colors['bg_secondary'])
        text_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.output_text = ScrolledText(text_frame,
                                       wrap='word',
                                       height=12,
                                       font=('Consolas', 9),
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       bd=0,
                                       relief='flat',
                                       insertbackground=self.colors['text_primary'])
        self.output_text.pack(fill='both', expand=True)
        
        # Configuration des tags pour les couleurs
        self.output_text.tag_config('folder', foreground='#ff8c00', font=('Consolas', 9, 'bold'))
        self.output_text.tag_config('convert', foreground='#16c60c', font=('Consolas', 9))
        self.output_text.tag_config('copy', foreground='#0078d4', font=('Consolas', 9))
        self.output_text.tag_config('error', foreground='#d83b01', font=('Consolas', 9, 'bold'))
        self.output_text.tag_config('success', foreground='#16c60c', font=('Consolas', 9, 'bold'))
        
    def toggle_output_options(self):
        """Active/désactive les options de sortie selon le nommage automatique"""
        if self.auto_folder_output.get():
            self.output_entry.configure(state='disabled', bg=self.colors['bg_tertiary'])
            self.browse_output_btn.configure(state='disabled', bg=self.colors['bg_tertiary'], 
                                           fg=self.colors['text_muted'])
        else:
            self.output_entry.configure(state='normal', bg=self.colors['bg_tertiary'])
            self.browse_output_btn.configure(state='normal', bg=self.colors['accent'], 
                                           fg=self.colors['text_primary'])
    
    def browse_input_folder(self):
        """Sélection du dossier d'entrée"""
        folder_path = filedialog.askdirectory(title="Sélectionner le dossier contenant les images HEIC")
        if folder_path:
            self.input_folder.set(folder_path)
            
    def browse_output_folder(self):
        """Sélection du dossier de sortie"""
        folder_path = filedialog.askdirectory(title="Sélectionner le dossier de sortie")
        if folder_path:
            self.output_folder.set(folder_path)
    
    def generate_output_folder_name(self, input_path):
        """Génère un nom intelligent pour le dossier de sortie"""
        input_path = Path(input_path)
        base_name = input_path.name
        
        if self.output_location.get() == "parent":
            parent_dir = input_path.parent
        else:
            parent_dir = input_path
        
        # Noms possibles pour le dossier de sortie
        possible_names = [
            f"{base_name}_converted",
            f"{base_name}_JPEG",
            f"Converted_{base_name}",
            f"JPEG_{base_name}"
        ]
        
        # Trouve un nom disponible
        for name in possible_names:
            output_path = parent_dir / name
            if not output_path.exists():
                return str(output_path)
        
        # Si tous les noms sont pris, ajoute un numéro
        counter = 1
        while True:
            output_path = parent_dir / f"{base_name}_converted_{counter}"
            if not output_path.exists():
                return str(output_path)
            counter += 1
    
    def count_files(self, input_folder):
        """Compte le nombre total de fichiers"""
        count = 0
        for root, dirs, files in os.walk(input_folder):
            count += len(files)
        return count
    
    def log_message(self, message, tag=''):
        """Ajoute un message au journal"""
        self.output_text.insert(tk.END, message + '\n', tag)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_conversion(self):
        """Démarre le processus de conversion"""
        input_path = self.input_folder.get().strip()
        
        if not input_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier d'entrée.")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Erreur", "Le dossier d'entrée n'existe pas.")
            return
        
        # Détermine le dossier de sortie
        if self.auto_folder_output.get():
            output_path = self.generate_output_folder_name(input_path)
        else:
            output_path = self.output_folder.get().strip()
            if not output_path:
                messagebox.showerror("Erreur", "Veuillez sélectionner un dossier de sortie.")
                return
        
        if input_path == output_path:
            messagebox.showerror("Erreur", "Le dossier d'entrée et de sortie ne peuvent pas être identiques.")
            return
        
        # Lance la conversion
        self.convert_heic_to_jpg(input_path, output_path)
    
    def convert_heic_to_jpg(self, input_folder, output_folder):
        """Fonction principale de conversion"""
        # Réinitialise l'interface
        self.output_text.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        self.convert_btn.configure(state='disabled', text="Conversion en cours...")
        
        try:
            # Compte les fichiers
            total_files = self.count_files(input_folder)
            if total_files == 0:
                self.log_message("❌ Aucun fichier trouvé dans le dossier d'entrée.", 'error')
                return
            
            self.log_message(f"📊 {total_files} fichiers détectés pour traitement.", 'folder')
            
            # Crée le dossier de sortie
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                self.log_message(f"📁 Dossier de sortie créé : {os.path.basename(output_folder)}", 'folder')
            
            processed_files = 0
            converted_count = 0
            copied_count = 0
            
            # Parcours des fichiers
            for root, dirs, files in os.walk(input_folder):
                if not files:
                    continue
                
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                
                if relative_path != '.':
                    self.log_message(f"📂 Traitement du dossier : {relative_path}", 'folder')
                
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)
                
                for filename in files:
                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    self.progress_bar['value'] = progress
                    self.progress_label.configure(text=f"Progression : {progress:.1f}% ({processed_files}/{total_files})")
                    
                    filepath = os.path.join(root, filename)
                    
                    if filename.lower().endswith(('.heic', '.heif')):
                        # Conversion HEIC vers JPEG
                        try:
                            output_filepath = os.path.join(output_subfolder, 
                                                         os.path.splitext(filename)[0] + ".jpg")
                            img = Image.open(filepath)
                            img.save(output_filepath, "JPEG", quality=95)
                            self.log_message(f"✅ Converti : {filename}", 'convert')
                            converted_count += 1
                        except Exception as e:
                            self.log_message(f"❌ Erreur conversion {filename}: {str(e)}", 'error')
                    else:
                        # Copie des autres fichiers
                        try:
                            shutil.copy2(filepath, output_subfolder)
                            self.log_message(f"📋 Copié : {filename}", 'copy')
                            copied_count += 1
                        except Exception as e:
                            self.log_message(f"❌ Erreur copie {filename}: {str(e)}", 'error')
            
            # Finalisation
            self.progress_bar['value'] = 100
            self.progress_label.configure(text="✅ Conversion terminée !")
            self.stats_label.configure(text=f"{converted_count} images converties • {copied_count} fichiers copiés")
            
            self.log_message("", '')
            self.log_message("🎉 CONVERSION TERMINÉE AVEC SUCCÈS !", 'success')
            self.log_message(f"📊 Résumé : {converted_count} conversions, {copied_count} copies", 'success')
            self.log_message(f"📁 Résultats disponibles dans : {output_folder}", 'success')
            
            # Ouvre le dossier de sortie
            try:
                os.startfile(output_folder)
            except:
                pass
                
        except Exception as e:
            self.log_message(f"❌ Erreur critique : {str(e)}", 'error')
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        
        finally:
            self.convert_btn.configure(state='normal', text="🚀 Démarrer la conversion")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernHEICConverter()
    app.run()