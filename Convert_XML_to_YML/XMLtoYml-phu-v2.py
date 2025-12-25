#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertisseur XML vers yml pour les patches de jeux PS4/PS5
Avec interface graphique tkinter
"""

import xml.etree.ElementTree as ET
import yaml
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import glob
import re
from typing import Dict, List, Any

def sanitize_filename(text: str) -> str:
    """Nettoie un texte pour en faire un nom de fichier valide"""
    if not text:
        return "Unknown"
    
    # Garder seulement les lettres, chiffres, espaces, tirets et underscores
    clean_text = re.sub(r'[^\w\s\-]', '', text)
    # Remplacer les espaces par des underscores
    clean_text = re.sub(r'\s+', '_', clean_text.strip())
    # Supprimer les underscores multiples
    clean_text = re.sub(r'_+', '_', clean_text)
    # Supprimer les underscores en début/fin
    clean_text = clean_text.strip('_')
    
    return clean_text.upper() if clean_text else "UNKNOWN"

def generate_output_filename(xml_content: str, base_name: str = None) -> str:
    """Génère un nom de fichier basé sur le titre et l'ID du XML"""
    try:
        root = ET.fromstring(xml_content)
        
        # Récupérer le premier ID
        title_id = "UNKNOWN_ID"
        title_id_elem = root.find('TitleID')
        if title_id_elem is not None:
            id_elem = title_id_elem.find('ID')
            if id_elem is not None and id_elem.text:
                title_id = id_elem.text.strip()
        
        # Récupérer le titre du premier Metadata
        title = "Unknown_Game"
        metadata = root.find('Metadata')
        if metadata is not None and metadata.get('Title'):
            title = sanitize_filename(metadata.get('Title'))
        
        # Construire le nom de fichier
        filename = f"{title}-{title_id}.yml"
        return filename
        
    except Exception:
        # En cas d'erreur, utiliser le nom de base ou un nom par défaut
        if base_name:
            return f"{base_name}.yml"
        return "converted_patch.yml"

def convert_hex_to_decimal(hex_string: str) -> int:
    """Convertit une adresse hexadécimale en décimal"""
    if hex_string.startswith('0x') or hex_string.startswith('0X'):
        return int(hex_string, 16)
    else:
        return int(hex_string, 16)

def parse_xml_to_yaml(xml_content: str) -> List[Dict[str, Any]]:
    """Parse le XML et retourne la structure yml (liste de patches)"""
    
    # Parser le XML
    root = ET.fromstring(xml_content)
    
    # Récupérer les TitleID (communs à tous les patches)
    title_ids = []
    title_id_elem = root.find('TitleID')
    if title_id_elem is not None:
        for id_elem in title_id_elem.findall('ID'):
            title_ids.append(id_elem.text)
    
    # Liste pour stocker tous les patches
    patches_list = []
    
    # Récupérer toutes les métadonnées (peut y en avoir plusieurs)
    metadata_elements = root.findall('Metadata')
    if not metadata_elements:
        raise ValueError("Pas de métadonnées trouvées dans le XML")
    
    # Traiter chaque section Metadata
    for metadata in metadata_elements:
        # Construire la structure YAML pour ce patch
        patch_entry = {
            "title": metadata.get('Title', 'Unknown Game'),
            "app_ver": metadata.get('AppVer', '01.00'),
            "patch_ver": metadata.get('PatchVer', '1.0'),
            "name": metadata.get('Name', 'Unknown Patch'),
            "author": metadata.get('Author', 'Unknown'),
            "note": metadata.get('Note', ''),
            "enabled": True,  # Valeur par défaut
            "arch": "orbis",  # Architecture par défaut pour PS4/PS5
            "patch_list": []
        }
        
        # Parser les patches pour cette section
        patch_list = metadata.find('PatchList')
        if patch_list is not None:
            for line in patch_list.findall('Line'):
                patch_type = line.get('Type', 'bytes')
                address_hex = line.get('Address', '0x0')
                value = line.get('Value', '')
                
                # Convertir l'adresse hex en format hex avec 0x
                if address_hex.startswith('00'):
                    # Convertir d'abord en int puis reformater
                    address_int = convert_hex_to_decimal(address_hex)
                    address_formatted = f"0x{address_int:x}"
                else:
                    address_formatted = f"0x{address_hex}" if not address_hex.startswith('0x') else address_hex
                
                # Ajouter à la liste des patches
                patch_entry["patch_list"].append([
                    patch_type, 
                    address_formatted, 
                    value
                ])
        
        # Ajouter ce patch à la liste générale
        patches_list.append(patch_entry)
    
    return patches_list

def xml_to_yaml_converter(xml_file_path: str = None, xml_content: str = None, output_file: str = None) -> str:
    """
    Convertit un fichier XML en YAML au format de patch complet
    
    Args:
        xml_file_path: Chemin vers le fichier XML (optionnel si xml_content fourni)
        xml_content: Contenu XML direct (optionnel si xml_file_path fourni)
        output_file: Fichier de sortie (optionnel, sinon retourne le string)
    
    Returns:
        String YAML formaté selon le nouveau format
    """
    
    # Lire le contenu XML
    if xml_content:
        content = xml_content
    elif xml_file_path:
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        raise ValueError("Il faut fournir soit xml_file_path soit xml_content")
    
    # Convertir
    yaml_data_list = parse_xml_to_yaml(content)
    
    # Créer le YAML formaté manuellement pour avoir le bon style
    yaml_lines = []
    
    for i, patch_data in enumerate(yaml_data_list):
        # Ajouter une ligne vide entre les patches (sauf pour le premier)
        if i > 0:
            yaml_lines.append("")
        
        yaml_lines.append(f"- title: \"{patch_data['title']}\"")
        yaml_lines.append(f"  app_ver: \"{patch_data['app_ver']}\"")
        yaml_lines.append(f"  patch_ver: \"{patch_data['patch_ver']}\"")
        yaml_lines.append(f"  name: \"{patch_data['name']}\"")
        yaml_lines.append(f"  author: \"{patch_data['author']}\"")
        yaml_lines.append(f"  note: \"{patch_data['note']}\"")
        yaml_lines.append(f"  enabled: {str(patch_data['enabled']).lower()}")
        yaml_lines.append(f"  arch: {patch_data['arch']}")
        yaml_lines.append("  patch_list:")
        
        # Ajouter les commentaires d'aide seulement pour le premier patch
        if i == 0:
            yaml_lines.append("      # Patch format:")
            yaml_lines.append("      # - [ patch_type, address, value ]")
            yaml_lines.append("      # Types: bytes, utf8, utf16, byte, bytes16, bytes32, bytes64, float32, float64")
            yaml_lines.append("      # - [ Generic Base   : 0x0      ] # beginning of file")
            yaml_lines.append("      # - [ Cell Elf Base  : 0x10000  ] # elf base")
            yaml_lines.append("      # - [ Orbis Elf Base : 0x400000 ] # disabled aslr base")
            yaml_lines.append("")
        
        # Ajouter les patches
        for patch in patch_data['patch_list']:
            patch_type, address, value = patch
            yaml_lines.append(f"       - [ {patch_type}, {address}, \"{value}\" ]")
    
    yaml_output = "\n".join(yaml_lines)
    
    # Sauvegarder si un fichier de sortie est spécifié
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(yaml_output)
        print(f"Fichier yml généré : {output_file}")
    
    return yaml_output

def batch_convert_folder(folder_path: str, output_folder: str = None) -> Dict[str, str]:
    """
    Convertit tous les fichiers XML d'un dossier en yml
    
    Args:
        folder_path: Chemin vers le dossier contenant les XML
        output_folder: Dossier de sortie (optionnel, utilise le même dossier par défaut)
    
    Returns:
        Dictionnaire avec les résultats {nom_fichier: status}
    """
    
    if not os.path.exists(folder_path):
        raise ValueError(f"Le dossier '{folder_path}' n'existe pas")
    
    # Utiliser le même dossier par défaut
    if output_folder is None:
        output_folder = folder_path
    
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)
    
    # Chercher tous les fichiers XML
    xml_files = glob.glob(os.path.join(folder_path, "*.xml"))
    xml_files.extend(glob.glob(os.path.join(folder_path, "*.XML")))
    
    if not xml_files:
        raise ValueError("Aucun fichier XML trouvé dans le dossier")
    
    results = {}
    
    for xml_file in xml_files:
        try:
            # Lire le contenu XML pour générer le nom automatiquement
            with open(xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Générer le nom de fichier automatiquement
            output_filename = generate_output_filename(xml_content, 
                                                     os.path.splitext(os.path.basename(xml_file))[0])
            output_file = os.path.join(output_folder, output_filename)
            
            # Convertir
            xml_to_yaml_converter(xml_content=xml_content, output_file=output_file)
            
            results[os.path.basename(xml_file)] = f"✅ Converti → {output_filename}"
            
        except Exception as e:
            results[os.path.basename(xml_file)] = f"❌ Erreur: {str(e)}"
    
    return results

class XMLToYAMLConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Convertisseur XML → YML | Patches PS4 - PS4toPS5 - PHU")
        self.root.geometry("1300x700")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.xml_content = ""
        self.yaml_content = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background='#2b2b2b')
        style.configure('Custom.TLabel', background='#2b2b2b', foreground='#ffffff', font=('Segoe UI', 10))
        style.configure('Title.TLabel', background='#2b2b2b', foreground='#4CAF50', font=('Segoe UI', 16, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🎮 Convertisseur XML vers YML", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Boutons de contrôle
        controls_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Boutons
        btn_style = {'font': ('Segoe UI', 10), 'relief': 'raised', 'bd': 2}
        
        self.btn_load = tk.Button(controls_frame, text="📁 Charger XML", 
                                 command=self.load_xml_file, bg='#4CAF50', fg='white',
                                 **btn_style)
        self.btn_load.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_convert = tk.Button(controls_frame, text="🔄 Convertir", 
                                    command=self.convert_xml_to_yaml, bg='#2196F3', fg='white',
                                    **btn_style)
        self.btn_convert.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_batch = tk.Button(controls_frame, text="📂 Conversion par lot", 
                                  command=self.batch_convert_folder, bg='#9C27B0', fg='white',
                                  **btn_style)
        self.btn_batch.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_save = tk.Button(controls_frame, text="💾 Sauvegarder YML", 
                                 command=self.save_yaml_file, bg='#FF9800', fg='white',
                                 **btn_style)
        self.btn_save.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_clear = tk.Button(controls_frame, text="🧹 Effacer", 
                                  command=self.clear_all, bg='#f44336', fg='white',
                                  **btn_style)
        self.btn_clear.pack(side=tk.RIGHT)
        
        # Panneaux de contenu
        content_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel XML (gauche)
        xml_frame = ttk.LabelFrame(content_frame, text="📄 Contenu XML", style='Custom.TFrame')
        xml_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.xml_text = scrolledtext.ScrolledText(xml_frame, wrap=tk.WORD, 
                                                 bg='#1e1e1e', fg='#ffffff',
                                                 font=('Consolas', 10),
                                                 insertbackground='white')
        self.xml_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel YAML (droite)
        yaml_frame = ttk.LabelFrame(content_frame, text="📋 Résultat YML", style='Custom.TFrame')
        yaml_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.yaml_text = scrolledtext.ScrolledText(yaml_frame, wrap=tk.WORD,
                                                  bg='#1e1e1e', fg='#90EE90',
                                                  font=('Consolas', 10),
                                                  insertbackground='white')
        self.yaml_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barre de status
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt - Chargez un fichier XML ou collez le contenu directement")
        
        status_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                style='Custom.TLabel', font=('Segoe UI', 9))
        status_label.pack(side=tk.LEFT)
        
        # Charger l'exemple par défaut
        self.load_example()
        
    def load_example(self):
        """Charge l'exemple XML par défaut"""
        example_xml = '''<?xml version="1.0" encoding="utf-8"?>
<Patch>
    <TitleID>
        <ID>CUSA00000</ID>
    </TitleID>
    <Metadata Title=""
              Name="60 FPS Unlock"
              Note="For PS4 PRO - PS5"
              Author="Arksama001-PHU"
              PatchVer="1.0"
              AppVer="00.00"
              AppElf="eboot.bin">
        <PatchList>
            <Line Type="bytes" Address="" Value=""/>
            <Line Type="bytes" Address="" Value=""/>        
            <Line Type="bytes" Address="" Value=""/>
        </PatchList>
    </Metadata>  
    <Metadata Title=""
              Name=""
              Note="For PS5"
              Author="Arksama001-PHU"
              PatchVer="1.0"
              AppVer="00.00"
              AppElf="eboot.bin">
        <PatchList>
            <Line Type="bytes" Address="" Value=""/>
            <Line Type="bytes" Address="" Value=""/>
        </PatchList>
    </Metadata>
</Patch>'''
        self.xml_text.delete(1.0, tk.END)
        self.xml_text.insert(1.0, example_xml)
        self.status_var.set("Exemple multi-patches chargé - Prêt pour la conversion")
    
    def load_xml_file(self):
        """Charge un fichier XML depuis le système"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier XML",
            filetypes=[("Fichiers XML", "*.xml"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.xml_text.delete(1.0, tk.END)
                self.xml_text.insert(1.0, content)
                
                filename = os.path.basename(file_path)
                self.status_var.set(f"Fichier chargé: {filename}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le fichier:\n{str(e)}")
                self.status_var.set("Erreur lors du chargement")
    
    def convert_xml_to_yaml(self):
        """Convertit le XML en YML"""
        xml_content = self.xml_text.get(1.0, tk.END).strip()
        
        if not xml_content:
            messagebox.showwarning("Attention", "Aucun contenu XML à convertir!")
            return
        
        try:
            self.status_var.set("Conversion en cours...")
            self.root.update()
            
            # Utiliser la fonction de conversion existante
            yaml_result = xml_to_yaml_converter(xml_content=xml_content)
            
            # Afficher le résultat
            self.yaml_text.delete(1.0, tk.END)
            self.yaml_text.insert(1.0, yaml_result)
            
            self.status_var.set("✅ Conversion réussie!")
            
        except Exception as e:
            messagebox.showerror("Erreur de conversion", f"Erreur lors de la conversion:\n{str(e)}")
            self.status_var.set("❌ Erreur de conversion")
    
    def batch_convert_folder(self):
        """Convertit tous les XML d'un dossier"""
        folder_path = filedialog.askdirectory(
            title="Sélectionner le dossier contenant les fichiers XML"
        )
        
        if not folder_path:
            return
        
        # Demander le dossier de sortie
        output_folder = filedialog.askdirectory(
            title="Sélectionner le dossier de sortie pour les fichiers YML",
            initialdir=folder_path
        )
        
        if not output_folder:
            # Utiliser le même dossier par défaut
            output_folder = folder_path
        
        try:
            self.status_var.set("Conversion par lot en cours...")
            self.root.update()
            
            # Effectuer la conversion par lot
            results = batch_convert_folder(folder_path, output_folder)
            
            # Afficher les résultats dans une nouvelle fenêtre
            self.show_batch_results(results, folder_path, output_folder)
            
            self.status_var.set(f"✅ Conversion par lot terminée - {len(results)} fichiers traités")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la conversion par lot:\n{str(e)}")
            self.status_var.set("❌ Erreur lors de la conversion par lot")
    
    def show_batch_results(self, results: Dict[str, str], input_folder: str, output_folder: str):
        """Affiche les résultats de la conversion par lot dans une nouvelle fenêtre"""
        
        # Créer une nouvelle fenêtre
        result_window = tk.Toplevel(self.root)
        result_window.title("📊 Résultats de la conversion par lot")
        result_window.geometry("600x500")
        result_window.configure(bg='#2b2b2b')
        
        # Frame principal
        main_frame = ttk.Frame(result_window, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(main_frame, 
                               text="📊 Résultats de la conversion par lot", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 15))
        
        # Infos des dossiers
        info_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(info_frame, text=f"📁 Dossier source: {input_folder}", 
                 style='Custom.TLabel', font=('Segoe UI', 9)).pack(anchor='w')
        ttk.Label(info_frame, text=f"📂 Dossier sortie: {output_folder}", 
                 style='Custom.TLabel', font=('Segoe UI', 9)).pack(anchor='w')
        
        # Zone de texte pour les résultats
        text_frame = ttk.LabelFrame(main_frame, text="Détails de la conversion", style='Custom.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        results_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                               bg='#1e1e1e', fg='#ffffff',
                                               font=('Consolas', 10),
                                               insertbackground='white')
        results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Remplir les résultats
        successful = 0
        failed = 0
        
        results_text.insert(tk.END, f"🎯 Conversion de {len(results)} fichiers XML:\n")
        results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for filename, status in results.items():
            results_text.insert(tk.END, f"{filename:<35} → {status}\n")
            if "✅" in status:
                successful += 1
            else:
                failed += 1
        
        results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        results_text.insert(tk.END, f"✅ Réussis: {successful}\n")
        results_text.insert(tk.END, f"❌ Échecs: {failed}\n")
        results_text.insert(tk.END, f"📊 Total: {len(results)}")
        
        # Bouton fermer
        close_button = tk.Button(main_frame, text="Fermer", 
                               command=result_window.destroy,
                               bg='#4CAF50', fg='white',
                               font=('Segoe UI', 10), relief='raised', bd=2)
        close_button.pack(pady=(15, 0))
    
    def save_yaml_file(self):
        """Sauvegarde le YML dans un fichier"""
        yaml_content = self.yaml_text.get(1.0, tk.END).strip()
        
        if not yaml_content:
            messagebox.showwarning("Attention", "Aucun contenu YML à sauvegarder!")
            return
        
        # générer un nom de fichier automatique basé sur le XML
        xml_content = self.xml_text.get(1.0, tk.END).strip()
        suggested_name = "converted_patch.yml"
        
        if xml_content:
            try:
                suggested_name = generate_output_filename(xml_content)
            except:
                pass
        
        file_path = filedialog.asksaveasfilename(
            title="Sauvegarder le fichier YML",
            defaultextension=".yml",
            initialfile=suggested_name,  # Corrected from initialfilename
            filetypes=[("Fichiers YML", "*.yml"), ("Fichiers YAML", "*.yaml"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(yaml_content)
                
                filename = os.path.basename(file_path)
                self.status_var.set(f"💾 Fichier sauvegardé: {filename}")
                messagebox.showinfo("Succès", f"Fichier sauvegardé avec succès:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier:\n{str(e)}")
                self.status_var.set("Erreur lors de la sauvegarde")
    
    def clear_all(self):
        """Efface tout le contenu"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment effacer tout le contenu?"):
            self.xml_text.delete(1.0, tk.END)
            self.yaml_text.delete(1.0, tk.END)
            self.status_var.set("Contenu effacé - Prêt pour un nouveau fichier")

def main():
    """Fonction principale pour lancer l'interface graphique"""
    
    # Vérifier si on lance en mode GUI ou console
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        # Mode console (comme avant)
        sample_xml = '''<?xml version="1.0" encoding="utf-8"?>
<Patch>
    <TitleID>
        <ID>CUSA00000</ID>
    </TitleID>
    <Metadata Title=""
              Name="60 FPS Unlock"
              Note="For PS4 PRO - PS5"
              Author="Arksama001-PHU"
              PatchVer="1.0"
              AppVer="00.00"
              AppElf="eboot.bin">
        <PatchList>
            <Line Type="bytes" Address="" Value=""/>
            <Line Type="bytes" Address="" Value=""/>        
            <Line Type="bytes" Address="" Value=""/>
        </PatchList>
    </Metadata>  
    <Metadata Title=""
              Name=""
              Note="For PS5"
              Author="Arksama001-PHU"
              PatchVer="1.0"
              AppVer="00.00"
              AppElf="eboot.bin">
        <PatchList>
            <Line Type="bytes" Address="" Value=""/>
            <Line Type="bytes" Address="" Value=""/>
        </PatchList>
    </Metadata>
</Patch>'''
        
        print("🎮 Convertisseur XML vers YML pour patches PS4 PS4toPS5 (Multi-patches)")
        print("=" * 65)
        
        try:
            yaml_result = xml_to_yaml_converter(xml_content=sample_xml)
            print("✅ Conversion réussie !")
            print(f"\n📄 {len(sample_xml.count('<Metadata'))} patches convertis :")
            print("-" * 40)
            print(yaml_result)
            
        except Exception as e:
            print(f"❌ Erreur lors de la conversion : {e}")
    
    else:
        # Mode GUI (par défaut)
        root = tk.Tk()
        app = XMLToYAMLConverterGUI(root)
        root.mainloop()

if __name__ == "__main__":
    # Lancement automatique en mode GUI
    # Pour utiliser en mode console, lance avec: python script.py --console
    main()