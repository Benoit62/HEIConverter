import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image
from pillow_heif import register_heif_opener
import os
import shutil
import sys

register_heif_opener()

# Codes ANSI pour les couleurs du texte dans la console
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def count_files(input_folder):
    count = 0
    for root, dirs, files in os.walk(input_folder):
        count += len(files)
    return count

def convert_heic_to_jpg(input_folder, output_folder):
    output_text.delete(1.0, tk.END)
    pb['value'] = 0
    for widget in frame_stats.winfo_children():
        widget.destroy()
    # Compteurs
    num_files = count_files(input_folder)
    if num_files == 0:
        output_text.insert(tk.END, "Aucun fichier à traiter.\n", 'error')
        return
    
    if input_folder == output_folder:
        output_text.insert(tk.END, "Conflit entre les dossiers\n", 'error')
        return

    print(os.path.dirname(input_folder))
    # Vérifie si le dossier de sortie existe, sinon le crée
    if not os.path.exists(output_folder):
        compt_output_file = 0
        while os.path.exists(os.path.join(os.path.dirname(input_folder), "conversion_result_"+str(compt_output_file))):
            compt_output_file+=1
        os.makedirs(os.path.join(os.path.dirname(input_folder), "conversion_result_"+str(compt_output_file)))
        output_folder=os.path.join(os.path.dirname(input_folder), "conversion_result_"+str(compt_output_file))
    print(output_folder)

    processed_files = 0

    # Parcourt tous les fichiers et dossiers dans le dossier d'entrée
    for root, dirs, files in os.walk(input_folder):
        # Crée le chemin de sortie pour conserver la même structure
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        
        print(f"Conversion du dossier {Color.RED}{relative_path}{Color.END}.")
        msg = f"Conversion du dossier {relative_path}."
        output_text.insert(tk.END, msg + '\n', 'folder')
        output_text.update()

        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        # Parcourt tous les fichiers du dossier actuel
        for filename in files:
            processed_files += 1
            pb['value'] = round((processed_files / num_files) * 100)
            value_label['text'] = f"{pb['value']}%"
            filepath = os.path.join(root, filename)
            output_filepath = os.path.join(output_subfolder, os.path.splitext(filename)[0] + ".jpg")
            if filename.endswith(".HEIC") or filename.endswith(".heic"):
                # Ouvre l'image HEIC et la convertit en JPG
                img = Image.open(filepath)
                img.save(output_filepath, "JPEG")

                print(f"Conversion de {Color.GREEN}{filename}{Color.END}.")
                # Affiche le nom du fichier converti en vert et le chemin en rouge
                msg = f"Conversion de {filename}"
                output_text.insert(tk.END, msg + '\n', 'convert')
                output_text.update()
            else:
                # Copie les fichiers qui ne sont pas des HEIC dans le dossier de sortie
                shutil.copy2(filepath, output_subfolder)
                print(f"Copie de {Color.BLUE}{filename}{Color.END}")
                msg = f"Copie de {filename}"
                output_text.insert(tk.END, msg + '\n', 'copy')
                output_text.update()
                
        print(f"Conversion du dossier {Color.RED}{relative_path}{Color.END} terminée.")
        print()
        msg = f"Conversion du dossier {relative_path} terminée."
        output_text.insert(tk.END, msg + '\n\n', 'folder')
        output_text.update()

    add_stats(num_files, processed_files)
    open_dir(output_folder)

def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_entry.delete(0, 'end')
    input_folder_entry.insert(0, folder_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, 'end')
    output_folder_entry.insert(0, folder_path)

def start_conversion():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    convert_heic_to_jpg(input_folder, output_folder)

def open_dir(output):
    os.system("start "+output)

def add_stats(total_files, procceded_files):
    infos = tk.Label(frame_stats, text=f"{procceded_files} images copiées sur {total_files} images traitées", font=("Courrier", 10), bg="#4065A4", fg="white")
    infos.pack(pady=10)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Convertir les images HEIC en JPG")
root.geometry("720x480")
root.config(background="#4065A4")
# Définir l'icône de l'application dans la barre des tâches
#root.iconbitmap('logo.ico')


frame = tk.Frame(root, bg="#4065A4")
frame.pack(expand="YES")


# Étiquettes et champs de saisie pour les dossiers d'entrée et de sortie
input_folder_label = tk.Label(frame, text="Dossier d'entrée :", font=("Courrier", 10), bg="#4065A4", fg="white")
input_folder_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_folder_entry = tk.Entry(frame, width=50, bg="#849bc3", fg="white")
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
browse_input_button = tk.Button(frame, text="Parcourir", font=("Courrier", 10), bg="#4065A4", fg="white", relief="ridge", command=browse_input_folder)
browse_input_button.grid(row=0, column=2, padx=5, pady=5)

frame2 = tk.Frame(root, bg="#4065A4")
frame2.pack(expand="YES")

output_folder_label = tk.Label(frame2, text="Dossier de sortie :", font=("Courrier", 10), bg="#4065A4", fg="white")
output_folder_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
output_folder_entry = tk.Entry(frame2, width=50, bg="#849bc3", fg="white")
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
browse_output_button = tk.Button(frame2, text="Parcourir", font=("Courrier", 10), bg="#4065A4", fg="white", relief="ridge", command=browse_output_folder)
browse_output_button.grid(row=1, column=2, padx=5, pady=5)


frame3 = tk.Frame(root, bg="#4065A4")
frame3.pack(expand="YES")

# Bouton pour démarrer la conversion
convert_button = tk.Button(frame3, text="Convertir", font=("Courrier", 15), bg="#2a5eb6", fg="white", relief="ridge", command=start_conversion)
convert_button.pack(pady=10)


frame_progress = tk.Frame(root, bg="#4065A4")
frame_progress.pack(expand="YES")

pb = ttk.Progressbar(frame_progress, orient='horizontal', mode='determinate', length=400, value=0)
pb.grid(row=0, column=0, ipady=5)

value_label = ttk.Label(frame_progress, text=f"{pb['value']}%", font=("Courrier", 12), background="#4065A4", foreground="white")
value_label.grid(row=0, column=1, ipady=10)

frame_stats = tk.Frame(root, bg="#4065A4")
frame_stats.pack(expand="YES")

frame4 = tk.Frame(root, bg="#849bc3")
frame4.pack(expand="YES")

output_text = ScrolledText(frame4, wrap='word', height=15, width=70)
output_text.grid(row=5, columnspan=3, padx=10, pady=5)

# Définition des styles de texte pour les différentes couleurs
output_text.tag_config('folder', foreground='red', font="Courrier")
output_text.tag_config('copy', foreground='blue', font="Courrier")
output_text.tag_config('convert', foreground='green', font="Courrier")
output_text.tag_config('error', foreground='black', font="Courrier")

# Rediriger sys.stdout vers le widget de texte
#sys.stdout = output_text

root.mainloop()




# Spécifie le dossier racine d'entrée et de sortie
#dossier_racine_entree = "C:/Users/bebew/Downloads/wetransfer_photos_2023-12-19_0855"
#dossier_racine_sortie = "C:/Users/bebew/Documents/resultat_conversion"

# Demande à l'utilisateur d'entrer les chemins de dossier
#dossier_racine_entree = input("Entrez le chemin du dossier d'entrée : ")
#dossier_racine_sortie = input("Entrez le chemin du dossier de sortie : ")

# Appelle la fonction pour convertir les images
#convert_heic_to_jpg(dossier_racine_entree, dossier_racine_sortie)
