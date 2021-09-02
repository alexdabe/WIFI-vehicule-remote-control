# -*- coding:Utf-8 -*-
'''Commande centralisee des vehicules'''

import socket
import sys
import threading
import tkinter
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

host = "192.168.0.20"
port = 40000
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''
z = ["defaut", "omega", "0", "m", "'"]
   z[0] defaut: nom du thread fourni par le serveur
   z[1]  omega: nom de la locomotive
   z[2]      0: vitesse de la locomotive
   z[3]      m: pour marche (connectee) et s: pour stop (deconnectee)
   z[4]      ': apostrophe de fin du message'''

a = ["defaut", "alfa", "0", "m", "'"]
b = ["defaut", "beta", "0", "m", "'"]

x = 0


def message_alfa():
    message = ","+a[1]+","+a[2]+","+a[3]+","
    message_emis = message.encode()
    connexion.send(message_emis)


def message_beta():
    message = ","+b[1]+","+b[2]+","+b[3]+","
    message_emis = message.encode()
    connexion.send(message_emis)


def marche_alfa(val):
    a[2] = val
    a[3] = "m"
    message_a = ","+a[1]+","+a[2]+","+a[3]+","
    etiquette_alfa_qg['text'] = a[1]+","+a[2]+","+a[3]
    message = message_a.encode()
    connexion.send(message)


def marche_beta(val):
    b[2] = val
    b[3] = "m"
    message_b = ","+b[1]+","+b[2]+","+b[3]+","
    etiquette_beta_qg['text'] = b[1]+","+b[2]+","+b[3]
    message = message_b.encode()
    connexion.send(message)


def sousprogrec():  # Sous programme execute par th2 (thread 2)
    while 1:
        message_recu = connexion.recv(1024)
        message_recu = message_recu.decode('utf-8')
        m = message_recu.split(",")  # Liste recue avant identification de la loco
        if m[1] == "alfa":  # Identification de la loco alfa
            ar = m  # Affectation de la liste recue à la liste ar de la loco alfa
            etiquette_alfa.config(text=ar[1]+","+ar[2]+","+ar[3])
        if m[1] == "beta":  # Identification de la loco alfa
            br = m  # Affectation de la liste recue à la liste br de la loco br
            etiquette_beta.config(text=br[1]+","+br[2]+","+br[3])
        if m[1] == "qg" and m[3] == "s":
            break
    print("Client arrêté. Connexion interrompue.")
    connexion.close()
    print("Le qg est deconnecte")

def stop_alfa():
    print("deconnecte alfa")
    a[2] = "0"
    a[3] = "s"
    message_a = ","+a[1]+","+a[2]+","+a[3]+","
    etiquette_alfa_qg['text'] = message_a
    message_emis = message_a.encode()
    connexion.send(message_emis)
    btdeconnecte_alfa.configure(bg="red")

def stop_beta():
    print("deconnecte beta")
    b[2] = "0"
    b[3] = "s"
    message_b = ","+b[1]+","+b[2]+","+b[3]+","
    etiquette_beta_qg['text'] = message_b
    message_emis = message_b.encode()
    connexion.send(message_emis)
    btdeconnecte_beta.configure(bg="red")


def envoifin():
    ''' Deconnecte le qg'''
    message_emis = ",qg,0,s,"
    message_emis = message_emis.encode()
    connexion.send(message_emis)
    btdeconnecte_qg['state']= tkinter.DISABLED
    btconnecte_qg['state'] = tkinter.NORMAL
    global x
    x = x+1
def quitter():
    fenetre.quit()


def connecte_qg():
    global th2
    if th2.is_alive():
        print('Still running')
    else:
        print("th2 est mort")
    global x
    # global a
    # a = ["defaut", "omega", "0", "m", "'"]
    global connexion
    if x > 0:
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")
    th2.start()
    btdeconnecte_qg['state']= tkinter.NORMAL
    btconnecte_qg['state'] = tkinter.DISABLED
i = 0
liste = []
def trace():
    '''    fig = Figure(figsize=(4, 3), dpi=96)
    ax = fig.add_subplot(111)'''
    # ax.plot(range(10), [5, 4, 2, 6, 9, 8, 7, 1, 2, 3])
    global i
    global liste
    i = i+1
    liste.append(i)
    print(i,liste)
    graph = FigureCanvasTkAgg(fig, master=fenetre)
    canvas = graph.get_tk_widget()
    ax.plot(range(i),liste)
    canvas.grid(row=4, column=0)
    time.sleep(1)
    fenetre.after(500,trace)

th2 = threading.Thread(target=sousprogrec)



fenetre = tkinter.Tk()
fenetre.title("QG")
fenetre.geometry("600x500")

# Definition du cadre alfa
cadre_alfa = tkinter.LabelFrame(fenetre, text="LOCO ALFA", bd=5, width=280, height=200)
cadre_alfa.grid_propagate(False)
cadre_alfa.grid(column=0, row=0)
btenvoi_alfa = tkinter.Button(cadre_alfa, text="Envoi", command=message_alfa)
btenvoi_alfa.grid(column=0, row=0)
etiquette_alfa_qg = tkinter.Label(cadre_alfa, borderwidth=3, relief="sunken",text="Defaut")
etiquette_alfa_qg.grid(column=0, row=1)
etiquette_alfa = tkinter.Label(cadre_alfa, borderwidth=3, relief="sunken", text="Defaut")
etiquette_alfa.grid(column=1, row=1)
curseur_alfa = tkinter.Scale(cadre_alfa, orient='horizontal', length=250, from_=-100, to=100, resolution=5, tickinterval=25,
label='Allure marche', command=marche_alfa)
curseur_alfa.set(0)
curseur_alfa.grid(row=2, column=0, columnspan=2)
btdeconnecte_alfa = tkinter.Button(cadre_alfa, text="Deconnexion", command=stop_alfa)
btdeconnecte_alfa.grid(column=0, row=3)

# Definition du cadre beta
cadre_beta = tkinter.LabelFrame(fenetre, text="LOCO BETA", bd=5, width=280, height=200)
cadre_beta.grid_propagate(False)
cadre_beta.grid(column=1,row=0)
btenvoi_beta = tkinter.Button(cadre_beta, text="Envoi", command=message_beta)
btenvoi_beta.grid(column=0,row=0)
etiquette_beta_qg = tkinter.Label(cadre_beta, borderwidth=3, relief="sunken", text="Defaut")
etiquette_beta_qg.grid(column=0, row=1)
etiquette_beta = tkinter.Label(cadre_beta, borderwidth=3, relief="sunken", text="Defaut")
etiquette_beta.grid(column=1, row=1)
curseur_beta = tkinter.Scale(cadre_beta, orient='horizontal', length=250, from_=-100, to=100, resolution=5, tickinterval=25,
label='Allure marche', command=marche_beta)
curseur_beta.set(0)
curseur_beta.grid(row=2, column=0, columnspan=2)
btdeconnecte_beta = tkinter.Button(cadre_beta, text="Deconnection", command=stop_beta)
btdeconnecte_beta.grid(column=0, row=3)

# Definition des widgets de la fenetre principale
btconnecte_qg = tkinter.Button(fenetre, text="Connection au serveur", command=connecte_qg)
btconnecte_qg.grid(column=1,row=1)
btdeconnecte_qg = tkinter.Button(fenetre, text="fin de thread", command=envoifin, state=tkinter.DISABLED)  # deconnexion
btdeconnecte_qg.grid(column=0,row=1)
btquitte = tkinter.Button(fenetre, text="Quitter", command=quitter)  # termine le programme
btquitte.grid(column=0,row=2)
btg = tkinter.Button(fenetre,text= "gph", command=trace)
btg.grid(column=0,row=3)

fig = Figure(figsize=(4, 3), dpi=96)
ax = fig.add_subplot(111)
graph = FigureCanvasTkAgg(fig, master=fenetre)
canvas = graph.get_tk_widget()
'''
ax.plot(range(10), [5, 4, 2, 6, 9, 8, 7, 1, 2, 3])
graph = FigureCanvasTkAgg(fig, master=fenetre)
canvas = graph.get_tk_widget()
canvas.grid(row=4, column=0) '''

fenetre.after(500, trace)
fenetre.mainloop()