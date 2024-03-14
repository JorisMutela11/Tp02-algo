from datetime import datetime
#client
class Client:
    def __init__(self, nom, date_naissance, numero_telephone):
        self.nom = nom
        self.date_naissance = date_naissance
        self.numero_telephone = numero_telephone
        self.facture = 0
    def getNom(self):
        return self.nom
    def getDateNaissance(self):
        return self.date_naissance
    def getNumeroTelephone(self):
        return self.numero_telephone
    def getFacture(self):
        return self.facture
    
#gestionnaire des clients 
class GererClients(Client):
    def __init__(self):
        self.clients = []
    def setNom(self, newNom):
        self.nom = newNom
    def setDateNaissance(self, newdate):
        self.date_naissance = newdate
    def setNumeroTelephone(self, newTel):
        self.numero_telephone = newTel
    def setfacture(self, newFact):
        self.facture = newFact
    def ajouter_client(self, client):
        self.clients.append(client)

#importation fichier cdr et conversion
class ImportCDR:
    def __init__(self, file_path):
        self.cdr_data = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split('|')
                cdr_dict = {
                    'Identifiant': int(data[0]),
                    'Type call': int(data[1]),
                    'Date et heure': datetime.strptime(data[2], '%Y%m%d%H%M%S'),
                    'Appelant': data[3],
                    'Appelé': data[4],
                    'Durée': int(data[5]),
                    'Taxe': int(data[6]),
                    'TotalVolume': int(data[7])
                }
                self.cdr_data.append(cdr_dict)

class GenererFacture:
    def __init__(self, client, cdr_data):
        self.client = client
        self.cdr_data = cdr_data

    def generer_facture_client(self):
        for cdr in self.cdr_data:
            if cdr['Type call'] == 0:  # Appel
                if cdr['Appelant'][:3] == cdr['Appelé'][:3]:  # Même réseau
                    myfacture = cdr['Durée'] * 0.025
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))                        
                else:
                    myfacture += cdr['Durée'] * 0.05
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))
            elif cdr['Type call'] == 1:  # SMS
                if cdr['Appelant'][:3] == cdr['Appelé'][:3]:  # Même réseau
                    myfacture = 0.001
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))
                else:
                    myfacture = 0.002
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))                    
            elif cdr['Type call'] == 2:  # Internet
                myfacture = cdr['TotalVolume'] * 0.03
                if cdr['Taxe']== 0: #0 : Aucune taxe
                    self.client.facture += myfacture                        
                elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                    self.client.facture += (myfacture + (myfacture * 0.1))
                elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                    self.client.facture += (myfacture + (myfacture * 0.16))

class Statistiques:
    def __init__(self, cdr_data):
        self.cdr_data = cdr_data

    def calculer_statistiques(self):
        nb_appels = sum(1 for cdr in self.cdr_data if cdr['Type call'] == 0)
        duree_appels = sum(cdr['Durée'] for cdr in self.cdr_data if cdr['Type call'] == 0)
        nb_sms = sum(1 for cdr in self.cdr_data if cdr['Type call'] == 1)
        volume_internet = sum(cdr['TotalVolume'] for cdr in self.cdr_data if cdr['Type call'] == 2)
        return nb_appels, duree_appels, nb_sms, volume_internet

# Test unitaire
print()
client_test = Client("POLYTECHNIQUE", "2023-01-11", "243818140560, 243818140120")
cdr_import = ImportCDR("E:/GC/SEMESTER 1/Algo/pro_1/cdr.txt")
generer_facture = GenererFacture(client_test, cdr_import.cdr_data)
generer_facture.generer_facture_client()
statistiques = Statistiques(cdr_import.cdr_data)
nb_appels, duree_appels, nb_sms, volume_internet = statistiques.calculer_statistiques()

client_test2 = Client("POLYTECHNIQUE", "2023-01-11", "243818140560, 243818140120,")
cdr_import = ImportCDR("E:/GC/SEMESTER 1/Algo/pro_1/tp_algo-1.txt")
generer_facture = GenererFacture(client_test2, cdr_import.cdr_data)
generer_facture.generer_facture_client()
statistiques = Statistiques(cdr_import.cdr_data)
nb_appels1, duree_appels1, nb_sms1, volume_internet1 = statistiques.calculer_statistiques()

print(f"Facture de {client_test2.nom}: $",client_test2.facture + client_test.facture)
print(f"Nombre d'appels:", nb_appels + nb_appels1, "Durée totale des appels:", duree_appels + duree_appels1 ," secondes")
print(f"Nombre de SMS: ", nb_sms + nb_sms1)
print(f"Volume internet utilisé: ", volume_internet + volume_internet1 ,"MegaByte")
print()