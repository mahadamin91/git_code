import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import tkinter.simpledialog as simpledialog
import random

# Stockage des sommets et des arêtes
sommets_positions = {}
adjacency_list = {}

######################################## Fonction ###############################

# Fonction quitter
def quit():
    quit = tk.messagebox.askyesno("Menu Principal", "Etes vous sur de vouloir quitter?")
    if quit > 0:
        app.destroy()
        return

# Fonction nouveau fichier
def newfile():
    messagebox.showinfo("Nouveau Fichier", "Création d'un nouveau fichier")

# Fonction nouveau dossier
def newfolder():
    fichier = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=[("Fichiers texte", "*.py"), ("Tous les fichiers", "*,*")])
    if fichier: 
        messagebox.showinfo("Fichier ouvert", f"Fichier selectionné: {fichier}")

# Fonction pour créer les sommets et les afficher dans le canvas
def creer_sommets():
    nombre_sommets = simpledialog.askinteger("Nombre de sommets", "Combien de sommets voulez-vous créer?", minvalue=0)
    
    if nombre_sommets is not None:  # Vérifier que l'utilisateur a entré une valeur
        sommets = []
        for i in range(nombre_sommets):
            nom_sommet = simpledialog.askstring("Nommer le sommet", f"Nommez le sommet numéro {i + 1}")
            if nom_sommet:
                sommets.append(nom_sommet)

                # Générer des coordonnées aléatoires tout en vérifiant les chevauchements
                while True:
                    x = random.randint(50, Canvas_width - 50)
                    y = random.randint(50, Canvas_height - 50)
                    if not any(abs(x - pos[0]) < 50 and abs(y - pos[1]) < 50 for pos in sommets_positions.values()):
                        break

                # Dessiner le cercle pour le sommet
                radius = 20
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white", outline="black", width=2)
                canvas.create_text(x, y, text=nom_sommet, fill="black", font=("Arial", 12))
                
                # Stocker la position du sommet et initialiser la liste d'adjacence
                sommets_positions[nom_sommet] = (x, y)
                adjacency_list[nom_sommet] = []
        
        messagebox.showinfo("Sommets créés", f"Vous avez créé les sommets : {', '.join(sommets)}")

# Fonction pour récupérer la position d'un sommet à partir de son nom
def find_position(nom_sommet):
    return sommets_positions.get(nom_sommet)

# Fonction pour créer une arête non orientée
def creer_arete_non_orientee():
    sommet1 = simpledialog.askstring("Créer arête non orientée", "Nom du premier sommet:")
    sommet2 = simpledialog.askstring("Créer arête non orientée", "Nom du second sommet:")

    if sommet1 and sommet2:
        pos1 = find_position(sommet1)
        pos2 = find_position(sommet2)
        
        if pos1 and pos2:
            canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], arrow=tk.NONE, fill="black", width=4)
            # Ajouter l'arête dans la liste d'adjacence (non orientée)
            adjacency_list[sommet1].append(sommet2)
            adjacency_list[sommet2].append(sommet1)
            messagebox.showinfo("Arête non orientée", f"Arête non orientée créée entre {sommet1} et {sommet2}")
        else:
            messagebox.showwarning("Erreur", "Un ou plusieurs sommets spécifiés n'existent pas.")
    else:
        messagebox.showwarning("Erreur", "Vous devez entrer deux noms de sommets valides.")

# Fonction pour créer une arête orientée
def creer_arete_orientee():
    sommet1 = simpledialog.askstring("Créer arête orientée", "Nom du sommet de départ:")
    sommet2 = simpledialog.askstring("Créer arête orientée", "Nom du sommet d'arrivée:")

    if sommet1 and sommet2:
        pos1 = find_position(sommet1)
        pos2 = find_position(sommet2)
        
        if pos1 and pos2:
            canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], arrow=tk.LAST, fill="black", width=4)
            # Ajouter l'arête dans la liste d'adjacence (orientée)
            adjacency_list[sommet1].append(sommet2)
            messagebox.showinfo("Arête orientée", f"Arête orientée créée de {sommet1} à {sommet2}")
        else:
            messagebox.showwarning("Erreur", "Un ou plusieurs sommets spécifiés n'existent pas.")
    else:
        messagebox.showwarning("Erreur", "Vous devez entrer deux noms de sommets valides.")

# Fonction pour afficher la liste d'adjacence
def afficher_liste_adjacence():
    result_canvas.delete("all")  # Effacer le contenu actuel du canvas de résultats
    
    y_offset = 20
    for sommet, voisins in adjacency_list.items():
        texte = f"{sommet} -> {', '.join(voisins) if voisins else 'Aucun voisin'}"
        result_canvas.create_text(10, y_offset, anchor=tk.W, text=texte, font=("Arial", 12))
        y_offset += 20

    messagebox.showinfo("Liste d'adjacence", "Liste d'adjacence affichée sur le panneau de droite.")

######################################## Fonction ###############################

app = tk.Tk()
app.geometry("800x600")
app.title("Menu principal")

mainmenu = tk.Menu(app)

first = tk.Menu(mainmenu, tearoff=0)
first.add_command(label="Nouveau fichier", command=newfile)
first.add_command(label="Nouveau dossier", command=newfolder)
first.add_command(label="Sauvegarder le graphe")
first.add_command(label="Quitter", command=quit)

second = tk.Menu(mainmenu, tearoff=0)
second.add_command(label="Créer des sommets", command=creer_sommets)
second.add_separator()
second.add_command(label="Créer une arête non orientée", command=creer_arete_non_orientee)
second.add_separator()
second.add_command(label="Créer une arête orientée", command=creer_arete_orientee)
second.add_separator()

three = tk.Menu(mainmenu, tearoff=0)
three.add_command(label="Liste d'adjacence", command=afficher_liste_adjacence)
three.add_command(label="Matrice d'adjacence")
three.add_command(label="Matrice d'incidence")
three.add_command(label="Types du graphe")

four = tk.Menu(mainmenu, tearoff=0)
four.add_command(label="Supprimer un sommet")
four.add_command(label="Supprimer une arete non orienté")
four.add_command(label="Supprimer une arete orienté")
four.add_separator()
four.add_command(label="Parcours en largeur")
four.add_command(label="Parcours en profondeur")
four.add_separator()
four.add_command(label="Algorithme de Dijkstra")
four.add_command(label="Algorithme de Bellamand Ford")
four.add_separator()
four.add_command(label="Algorithme de Glouton")
four.add_command(label="Algorithme Dsatur (ou Dasat)")
four.add_separator()
four.add_command(label="Bouger un sommet")

five = tk.Menu(mainmenu, tearoff=0)
five.add_command(label="Options")

mainmenu.add_cascade(label="Fichier", menu=first)
mainmenu.add_cascade(label="Création", menu=second)
mainmenu.add_cascade(label="Affichage", menu=three)
mainmenu.add_cascade(label="Exécution", menu=four)
mainmenu.add_cascade(label="Edition", menu=five)

##################################### CANVAS POUR LE GRAPHE ###############################

Canvas_height = 500
Canvas_width = 450
canvas = tk.Canvas(app, width=Canvas_width, height=Canvas_height, bg="white")
canvas.pack(pady=10, side=tk.LEFT)

result_canvas = tk.Canvas(app, width=300, height=500, bg="lightgray")
result_canvas.pack(pady=20, side=tk.RIGHT)

##################################### CANVAS POUR LE GRAPHE ###############################

app.config(menu=mainmenu)
app.mainloop()
