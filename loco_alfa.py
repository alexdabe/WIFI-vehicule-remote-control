# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
import socket
import sys
import threading

host = "192.168.0.20"
port = 40000

a = ["defaut", "omega", "0", "m", "'"]
loco_id = "alfa"
message_recu = ' '


def marche():
    global a
    print("loco alfa, bien recu", message_recu)
    v = a[2]
    vitesse = int(v)
    if vitesse > 0:  # marche avant
        print("j'avance", vitesse)
    if vitesse < 0:  # marche arriere
        print("je recule", vitesse)
    if vitesse == 0:  # arret de la loco
        print("je stoppe")


class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion

    def run(self):
        global a
        while 1:
            message_recu = self.connexion.recv(1024)
            message_recu = message_recu.decode('utf-8')
            print(message_recu)  # pour info, message brut
            a = message_recu.split(",")
            if a[1] == loco_id:
                marche()
            if a[1] == loco_id and a[3] == "s":
                print("La loco,", loco_id, "est deconnectée")
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        # th_E._Thread__stop()
        print("Loco alfa. Connexion interrompue.")
        self.connexion.close()


class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion

    def run(self):
        message_emis = " "
        while 1:
            message_emis = input("entrez message:\n")
            message_emis = "," + loco_id + "," + message_emis + ","
            message_emis = message_emis.encode()
            self.connexion.send(message_emis)


# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_E.start()
th_R.start()
