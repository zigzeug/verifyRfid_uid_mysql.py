
import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
from pirc522 import RFID
import time
import mysql.connector


#Code MySQL\
#connexion au serveur
conn = mysql.connector.connect(host="localhost", user="root", password="root", database="CISB")
cursor = conn.cursor()

#la liste des id_cards dans la database
cursor.execute("SELECT * FROM card")
#Définit la liste des UIDs du badge 
RFID_UID =[] 
for e in cursor.fetchall():
    if e != ():
        RFID_UID +=[e[2]] 



GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

LED_RED = 3 #Définit le numéro du port GPIO qui alimente la led rouge
LED_GREEN = 5 #Définit le numéro du port GPIO qui alimente la led verte


#Active le contrôle du GPIO
GPIO.setup(LED_RED, GPIO.OUT) 
GPIO.setup(LED_GREEN, GPIO.OUT) 

#On éteint initialement les 2 leds
GPIO.output(LED_GREEN, GPIO.LOW) 



rc522 = RFID() #On instancie la librairie

print('En attente d\'un badge (pour quitter, Ctrl + c): ') #On affiche un message demandant à l'utilisateur de passer son badge


try:
  #On va faire une boucle infinie pour lire en boucle
  while True :
      rc522.wait_for_tag() #On attend qu'une puce RFID passe à portée
      (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

      if not error : #Si on a pas d'erreur
          (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps

          if not error : #Si on a réussi à nettoyer
              uid = ''.join(str(v) for v in uid)
              if uid in RFID_UID :
                  print('Badge {} autorisé !'.format(uid))
                  GPIO.output(LED_GREEN, GPIO.HIGH)
                  time.sleep(1)
                  GPIO.output(LED_GREEN, GPIO.LOW)
                  time.sleep(1)
              else :
                  print('Badge {} interdit !'.format(uid))
                  GPIO.output(LED_RED, GPIO.HIGH)
                  time.sleep(1)
                  GPIO.output(LED_RED, GPIO.LOW)
                  time.sleep(1)

              time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes
except:
    GPIO.cleanup()  # extinction de la led à l'arrêt du programme


                             