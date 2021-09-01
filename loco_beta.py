'''Version avec retour du message recu'''
import socket
import sys
import threading
import time

host = "192.168.0.20"
port = 40000

b = ["defaut", "beta", "0", "m", "'"]
br = b
message_emis = br
message_recu = b
loco_id = "beta"


def sousprogrec():
    while 1:
        message = connexion.recv(1024)
        message_recu = message.decode('utf-8')
        print(message_recu)
        global b
        b = message_recu.split(",")
        print(b)
        if b[1] == loco_id:
            marche()
            connexion.send(message) # Renvoi du message pour confirmation
        if b[1] == loco_id and b[3] == "s":
            print("La loco,", loco_id, "est deconnectée")
            break
    print("Client arrêté. Connexion interrompue.")
    connexion.close()


def sousprogenvoi():
    while 1:
        message_emis = input("entrez message:\n")
        message_emis = "," + loco_id + "," + message_emis + ","
        message_emis = message_emis.encode()
        connexion.send(message_emis)


def marche():
    global b
    print("loco beta, bien recu")
    v = b[2]
    vitesse = int(v)
    if vitesse > 0:  # marche avant
        print("j'avance", vitesse)
    if vitesse < 0:  # marche arriere
        print("je recule", vitesse)
    if vitesse == 0:  # arret de la loco
        print("je stoppe")


# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

th1 = threading.Thread(target=sousprogenvoi)
th2 = threading.Thread(target=sousprogrec)
# th3 = threading.Thread(target=retour_code)
th1.start()
th2.start()
# th3.start()