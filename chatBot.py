import re
import tkinter as tk
from tkinter.font import Font


#Fontion pour valide l'email
def valide_email(email):
    #Le Regex de l'email
    pattern = r"^[A-Za-z0-9._%+-]+@(gmail\.com|edu\.umi\.ac\.ma)$"
    return re.match(pattern, email) is not None

# Function pour valide le CNE
def valide_code_massar(cne):
    #Le Regex de CNE
    pattern = r"^[A-Z]\d{9}$"
    return re.match(pattern, cne) is not None

# Function d'affichage pour l'interface
def affiche(message):
    chat_fenetre.config(state=tk.NORMAL)
    chat_fenetre.insert(tk.END, message + "\n")
    chat_fenetre.config(state=tk.DISABLED)
    chat_fenetre.see(tk.END)

# Main chatbot logic wrapped for the interface
def process_input(user_input):
    global greeting_done, step
    user_input = user_input.strip()
    
    if not greeting_done:
        if user_input in ["bonjour", "bonsoir", "hey", "salut", "salam", "coucou", "hello", "yo", "allô", "salut tout le monde", "bienvenue",
                          "hi", "what's up", "welcome"]:
            affiche("CHATBOT: " + user_input + ", bienvenue sur le chatbot de la FST. Comment puis-je vous aider?\nvoici notre services: attestation ,compensation ,orientation ,rachtage")
            greeting_done = True
            step = "main_menu"
        else:
            affiche("CHATBOT: SVP, reformulez votre salutation.")
        return

    
    if step == "main_menu":
        if user_input == "rachtage":
            affiche("CHATBOT: Entrez vos notes de ce semestre (6 notes).")
            step = "rachtage"
            notes.clear()
        elif user_input == "compensation":
            affiche("CHATBOT: Entrez vos notes de ce semestre (6 notes).")
            step = "compensation"
            notes.clear()
        elif user_input == "orientation":
            affiche("CHATBOT: Entrez les moyennes des 4 semestres.")
            step = "orientation"
            sem_notes.clear()
        elif user_input == "attestation":
            affiche("CHATBOT: Entrez votre code Massar.")
            step = "attestation"
        else:
            affiche("CHATBOT: SVP, reformulez votre question.")

    # Process rachtage and compensation steps
    elif step == "rachtage" or step == "compensation":
        try:
            note = float(user_input)
            if note < 0 or note > 20:
                affiche("CHATBOT: Note invalide, Tu peux retaper")
                return 
            notes.append(note)
            if len(notes) < 6:     
                affiche(f"CHATBOT: Note {len(notes) + 1}: ")
            else:
                moy = sum(notes) / 6
                count_below_5 = sum(1 for note in notes if note < 5)
                if step == "rachtage":
                    result = "sera racheté." if count_below_5 <= 1 and moy >= 10 else "n'est pas racheté."
                    affiche("CHATBOT: Merci de votre vesite.")
                else:
                    count_below_7 = sum(1 for note in notes if note < 7)
                    result = "sera compensé." if count_below_7 <= 3 and moy >= 10 else "n'est pas compensé."
                affiche(f"CHATBOT: Ce semestre {result}")
                affiche("CHATBOT: Merci de votre vesite.")
                reset_chatbot()
                fenetre.after(3500, fenetre.destroy)  

                
        except ValueError:
            affiche("CHATBOT: Entrez une note valide.")

    # Process orientation step
    elif step == "orientation":
        try:
            note = float(user_input)
            if note < 0 or note > 20:
                affiche("CHATBOT: Note invalide, Tu peux retaper")
                return 
            sem_notes.append(note)
            if len(sem_notes) < 4:
                affiche(f"CHATBOT: Moyenne du semestre {len(sem_notes) + 1}: ")
            else:
                moy = sum(sem_notes) / 4
                if moy >= 10:
                    affiche(f"CHATBOT: Vous serez orienté vers votre premier choix et votre note du DEUST est : {moy:.2f}")
                    fenetre.after(3500, fenetre.destroy)  

                else:
                    affiche("CHATBOT: Entrez les notes des semestres qui n'est pas validé")
                    step = "orientation_extra"
                    extra_notes.clear()
        except ValueError:
            affiche("CHATBOT: Entrez une moyenne valide")

    elif step == "orientation_extra":
        try:
            note = float(user_input)
            extra_notes.append(note)
            if len(extra_notes) < len([s for s in sem_notes if s < 10]) * 6:
                affiche("CHATBOT: Note suivante: ")
            else:
                NV = sum(1 for note in extra_notes if note < 5)
                if NV >= 4:
                    affiche("CHATBOT: Vous devez ajouter une année de réserve.")
                    fenetre.after(3500, fenetre.destroy)  
                else:
                    affiche("CHATBOT: Vous serez orienté vers votre second choix.") 
                reset_chatbot()
                fenetre.after(3500, fenetre.destroy)  

        except ValueError:
            affiche("CHATBOT: Entrez une note valide.")

    elif step == "attestation":
        # Check if the Massar code is valid
        if valide_code_massar(user_input):
            affiche("CHATBOT: Entrez votre email.")
            step = "attestation_email"
        else:
            affiche("CHATBOT: Code Massar invalide. Il doit commencer par une lettre majuscule suivie de 9 chiffres.")

    elif step == "attestation_email":
        if valide_email(user_input):
            affiche("CHATBOT: Votre attestation sera envoyée sur votre boîte mail\nChatbot: Merci de votre vesite.")
            fenetre.after(3500, fenetre.destroy)  
        else:
            affiche("CHATBOT: Format de l'email invalide. Utilisez un email se terminant par @gmail.com ou @edu.umi.ac.ma.")

def reset_chatbot():
    global greeting_done, step, notes, sem_notes, extra_notes
    greeting_done = False
    step = ""
    notes = []
    sem_notes = []
    extra_notes = []
    

def on_enter(event):
    user_input = entre.get()
    entre.delete(0, tk.END)
    affiche("VOUS: " + user_input)
    process_input(user_input)

# Initialize main Tkinter window
fenetre = tk.Tk()
fenetre.title("Chatbot de la FST")
fenetre.geometry("500x600")

# Chat window (display area)
chat_fenetre = tk.Text(fenetre, state="disabled", width=60, height=30, wrap="word")
chat_fenetre.pack(pady=10)
chatbot_font = Font(family="Helvetica", size=12, weight="bold")
vous_font = Font(family="Arial", size=12, slant="italic")


# Entry box for user input
entre = tk.Entry(fenetre, width=50)
entre.pack(pady=10)
entre.bind("<Return>", on_enter)

# Variables to keep track of chatbot state
greeting_done = False
step = ""
notes = []
sem_notes = []
extra_notes = []

affiche("CHATBOT: Bienvenue au chatbot de la FSTE")

# Run the Tkinter main loop
fenetre.mainloop()
