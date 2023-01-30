from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import random

# Fenêtre Lecteur MP3
lecteur = Tk()
lecteur.geometry("300x450")
lecteur.title("Lecteur MP3")
lecteur.resizable(height=False, width=False)
pygame.mixer.init()


# Fonction pour ajouter un ou plusieurs fichiers MP3 au lecteur
def ajouter_musique():
    # Permet d'ouvrir la pop up qui demande quels fichiers sélectionner
    musique = filedialog.askopenfilenames(initialdir="musique/", title="Sélectionner vos musique", filetypes=(("mp3 Files", "*.mp3"),))
    # Permet d'ajouter plusieurs fichiers MP3
    for musique in musique:
        musique = musique.replace(".mp3", "")
        liste_musique.insert(END, musique)


# Fonction pour supprimer un fichier MP3 du lecteur
def retirer_musique():
    stop_musique()
    liste_musique.delete(ANCHOR)
    pygame.mixer.music.stop()


# Fonction pour afficher le temps total et le temps de la musique qui défile tout en se synchronisant à la barre de progression
def temps_musique():
    if musique_stoper == True:
        return
    # Affiche le temps passé de la musique
    temps_actuel = pygame.mixer.music.get_pos() / 1000
    musique = liste_musique.get(ACTIVE)
    musique = f'{musique}.mp3'
    song_mut = MP3(musique)
    global temps_total_musique
    # Prends le temps total de la musique
    temps_total_musique = song_mut.info.length
    # Convertie le temps en Minute : Seconde 00:00
    convertir_temps_total = time.strftime("%M:%S", time.gmtime(temps_total_musique))
    temps_actuel += 1
    if int(barre_progression_musique.get()) == int(temps_total_musique):
        # Affiche le temps passé et le temps total de la musique par exemple 00:30/01:24
        progression_musique.config(text=f"{convertir_temps_total}/{convertir_temps_total}")
    elif pausee:
        pass
    elif int(barre_progression_musique.get()) == int(temps_actuel):
        # Met à jour la barre de progression selon le temps de la musique
        barre_position = int(temps_total_musique)
        barre_progression_musique.config(to=barre_position, value=int(temps_actuel))
    else:
        # Met à jour la barre de progression selon le temps de la musique
        barre_position = int(temps_total_musique)
        barre_progression_musique.config(to=barre_position, value=int(barre_progression_musique.get()))
        convertir_temps_musique = time.strftime("%M:%S", time.gmtime(int(barre_progression_musique.get())))
        progression_musique.config(text=f"{convertir_temps_musique}/{convertir_temps_total}")

        # Synchronisation de la barre de progression et du temps de la musique
        barre_prog = int(barre_progression_musique.get()) + 1
        barre_progression_musique.config(value=barre_prog)

    # Met à jour le temps de la musique
    progression_musique.after(1000, temps_musique)

    # Vérifie si la musique est finie pour passer la suivante
    musique_suivante_auto()


# Fonction pour la barre de progression de la musique
def bar_progression(x):
    musique = liste_musique.get(ACTIVE)
    musique = f'{musique}.mp3'
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0, start=int(barre_progression_musique.get()))


# Fonction pour jouer une musique avec le bouton play
def jouer_musique():
    global musique_stoper
    # Remise à zéro de la barre de progression de la musique
    progression_musique.config(text="")
    barre_progression_musique.config(value=0)
    musique_stoper = False
    # Joue la musique qui est sélectionnée (en surbrillance)
    musique = liste_musique.get(ACTIVE)
    musique = f'{musique}.mp3'
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    temps_musique()


# Fonction pour jouer la prochaine musique quand la précédente se termine
def musique_suivante_auto():
    # Vérifie si la musique est en pause ou si elle est finie
    if pausee or pygame.mixer.music.get_busy():
        pass
    # Si la musique est finie joue la musique suivante
    else:
        musique_suivante()


musique_stoper = False


# Fonction pour stopper la musique avec le bouton stop
def stop_musique():
    # Remise à zéro de la barre de progression de la musique
    progression_musique.config(text="")
    barre_progression_musique.config(value=0)
    # Stop la musique
    pygame.mixer.music.stop()
    liste_musique.selection_clear(ACTIVE)
    progression_musique.config(text="")
    global musique_stoper
    musique_stoper = True


pausee = False


# Fonction pour mettre en pause la musique et la rependre au même moment avec le bouton pause
def pause_musique(en_pause):
    global pausee
    pausee = en_pause
    if musique_stoper == True:
        return

    if pausee == True:
        pygame.mixer.music.unpause()
        pausee = False
    else:
        pygame.mixer.music.pause()
        pausee = True


boucle = False


# Fonction pour jouer la même musique en boucle avec le bouton boucle
def boucle_musique():
    global boucle
    boucle = not boucle
    if boucle:
        musique = liste_musique.get(ACTIVE)
        musique = f'{musique}.mp3'
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(loops=-1)
        progression_musique.config(text="")
        barre_progression_musique.config(value=0)
    else:
        musique = liste_musique.get(ACTIVE)
        musique = f'{musique}.mp3'
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(loops=0)
        progression_musique.config(text="")
        barre_progression_musique.config(value=0)


# Fonction pour passer à la musique suivante avec le bouton suivant
def musique_suivante():
    global boucle
    # Remise à zéro de la barre de progression de la musique
    progression_musique.config(text="")
    barre_progression_musique.config(value=0)
    boucle = False
    # Sélectionne la musique suivante par rapport à l'ancienne sélectionner
    suivante = liste_musique.curselection()
    # S'il n'y a plus de musique suivante revient au début de la liste
    suivante = (suivante[0] + 1) % liste_musique.size()
    musique = liste_musique.get(suivante)
    musique = f'{musique}.mp3'
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    liste_musique.selection_clear(0, END)
    liste_musique.activate(suivante)
    liste_musique.select_set(suivante, last=None)


# Fonction pour passer à la musique suivant avec le bouton précédent
def musique_precedent():
    global boucle
    # Remise à zéro de la barre de progression de la musique
    progression_musique.config(text="")
    barre_progression_musique.config(value=0)
    boucle = False
    # Sélectionne la musique précédente par rapport à l'ancienne sélectionné
    precedente = liste_musique.curselection()
    # S'il n'y a plus de musique précédente revient au début de la liste
    precedente = (precedente[0] - 1 + liste_musique.size()) % liste_musique.size()
    musique = liste_musique.get(precedente)
    musique = f'{musique}.mp3'
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    liste_musique.selection_clear(0, END)
    liste_musique.activate(precedente)
    liste_musique.select_set(precedente, last=None)


# Fonction pour lancer une musique aléatoire de la liste avec le bouton aléatoire
def musique_aleatoire():
    # Remise à zéro de la barre de progression de la musique
    progression_musique.config(text="")
    barre_progression_musique.config(value=0)
    # Sélectionne une musique aléatoire de la liste de musique et la joue
    aleatoire = random.randint(0, liste_musique.size() - 1)
    musique = liste_musique.get(aleatoire)
    musique = f'{musique}.mp3'
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    liste_musique.selection_clear(0, END)
    liste_musique.activate(aleatoire)
    liste_musique.select_set(aleatoire, last=None)


# Fonction pour monter le son avec le bouton volume haut
def volume_haut():
    volume = pygame.mixer.music.get_volume()
    # Augmente le volume de 0.1 à chaque fois que l'on appuie sur le bouton. Volume max =1.0
    if volume < 1.0:
        pygame.mixer.music.set_volume(min(volume + 0.1, 1.0))


# Fonction pour baisser le son avec le bouton volume bas
def volume_bas():
    # Diminue le volume de 0.1 à chaque fois que l'on appuie sur le bouton. Volume min = 0

    volume = pygame.mixer.music.get_volume()
    if volume > 0:
        pygame.mixer.music.set_volume(max(volume - 0.1, 0))


# Fonction pour rendre muet la musique avec le bouton mute
def volume_mute():
    global mute
    mute = not mute
    pygame.mixer.music.set_volume(0 if mute else 1)


mute = False

# Menu déroulant
menu_option = Menu(lecteur)
option = Menu(menu_option, tearoff=0)
# Bouton ajouter des musiques
option.add_command(label="Ajouter des musiques", command=ajouter_musique)
# Bouton retirer des musiques
option.add_command(label="Retirer des musiques", command=retirer_musique)
# Titre menu déroulant
menu_option.add_cascade(label="Options", menu=option)
lecteur.config(menu=menu_option)

# Liste des musiques
liste_musique = Listbox(lecteur, bg="#a90404", fg="White", width=250, height=13, selectbackground="Gray")
liste_musique.pack(padx=25)
# Scrollbar vertical
scrollbar_vertical = Scrollbar(lecteur)
scrollbar_vertical.pack(side=RIGHT, fill=Y)
liste_musique.config(yscrollcommand=scrollbar_vertical.set)
scrollbar_vertical.config(command=liste_musique.yview)
# Scrollbar horizontale
scrollbar_horizontale = Scrollbar(lecteur, orient='horizontal')
scrollbar_horizontale.pack(side=BOTTOM, fill=X)
liste_musique.config(xscrollcommand=scrollbar_horizontale.set)
scrollbar_horizontale.config(command=liste_musique.xview)
liste_musique.bind("<Double-Button-1>", jouer_musique)

# Progression de la musique
progression_musique = Label(lecteur, text="", bd=1, relief=GROOVE, anchor=E)
progression_musique.pack(fill=X, side=BOTTOM, ipady=2)
# Barre de progression de la musique
barre_progression_musique = ttk.Scale(lecteur, from_=0, to=100, orient=HORIZONTAL, value=0, length=250,
                                      command=bar_progression)
barre_progression_musique.pack(pady=5)

# Fenêtre contrôle audio 1
control_audio_1 = Frame(lecteur)
control_audio_1.pack()
# Bouton musique précédente
bouton_precedent_image = PhotoImage(file="images/precedent.png")
bouton_precedent = Button(control_audio_1, image=bouton_precedent_image, borderwidth=0, command=musique_precedent)
bouton_precedent.grid(row=0, column=0, padx=10, pady=5)
# Bouton stop musique
bouton_stop_image = PhotoImage(file="images/stop.png")
bouton_stop = Button(control_audio_1, image=bouton_stop_image, borderwidth=0, command=stop_musique)
bouton_stop.grid(row=0, column=1, padx=10, pady=5)
# Bouton jouer musique
bouton_jouer_image = PhotoImage(file="images/jouer.png")
bouton_jouer = Button(control_audio_1, image=bouton_jouer_image, borderwidth=0, command=jouer_musique)
bouton_jouer.grid(row=0, column=2, padx=10, pady=5)
# Bouton pause musique
bouton_pause_image = PhotoImage(file="images/pause.png")
bouton_pause = Button(control_audio_1, image=bouton_pause_image, borderwidth=0, command=lambda: pause_musique(pausee))
bouton_pause.grid(row=0, column=3, padx=10, pady=5)
# Bouton musique suivante
bouton_suivant_image = PhotoImage(file="images/suivant.png")
bouton_suivant = Button(control_audio_1, image=bouton_suivant_image, borderwidth=0, command=musique_suivante)
bouton_suivant.grid(row=0, column=4, padx=10, pady=5)

# Fenêtre contrôle audio 2
control_audio_2 = Frame(lecteur)
control_audio_2.pack()
# Bouton musique aléatoire
bouton_aleatoire_image = PhotoImage(file="images/aleatoire.png")
bouton_aleatoire = Button(control_audio_2, image=bouton_aleatoire_image, borderwidth=0, command=musique_aleatoire)
bouton_aleatoire.grid(row=0, column=0, padx=12, pady=5)
# Bouton baisser volume
bouton_volume_bas_image = PhotoImage(file="images/volume_bas.png")
bouton_volume_bas = Button(control_audio_2, image=bouton_volume_bas_image, borderwidth=0, command=volume_bas)
bouton_volume_bas.grid(row=0, column=1, padx=12, pady=5)
# Bouton monter volume
bouton_volume_haut_image = PhotoImage(file="images/volume_haut.png")
bouton_volume_haut = Button(control_audio_2, image=bouton_volume_haut_image, borderwidth=0, command=volume_haut)
bouton_volume_haut.grid(row=0, column=2, padx=12, pady=5)
# Bouton volume mute
bouton_volume_mute_image = PhotoImage(file="images/volume_mute.png")
bouton_volume_mute = Button(control_audio_2, image=bouton_volume_mute_image, borderwidth=0, command=volume_mute)
bouton_volume_mute.grid(row=0, column=3, padx=12, pady=5)
# Bouton répéter la musique
bouton_boucle_image = PhotoImage(file="images/boucle.png")
bouton_boucle = Button(control_audio_2, image=bouton_boucle_image, borderwidth=0, command=boucle_musique)
bouton_boucle.grid(row=0, column=4, padx=12, pady=5)

lecteur.mainloop()
