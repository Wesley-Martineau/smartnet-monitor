from scapy.all import sniff, IP, TCP
import csv, datetime, os

os.makedirs('data', exist_ok=True)
FICHIER = 'data/traffic.csv'
COLS = ['timestamp','src_ip','dst_ip','protocole','taille','ttl','src_port','dst_port']

# Creer le fichier avec en-tetes
if not os.path.exists(FICHIER):
    with open(FICHIER,'w',newline='') as f:
        csv.DictWriter(f, fieldnames=COLS).writeheader()

def traiter(paquet):
    if IP in paquet:
        ligne = {
            'timestamp': datetime.datetime.now().isoformat(),
            'src_ip': paquet[IP].src,
            'dst_ip': paquet[IP].dst,
            'protocole': paquet[IP].proto,
            'taille': len(paquet),
            'ttl': paquet[IP].ttl,
            'src_port': paquet[TCP].sport if TCP in paquet else 0,
            'dst_port': paquet[TCP].dport if TCP in paquet else 0,
        }
        with open(FICHIER,'a',newline='') as f:
            csv.DictWriter(f, fieldnames=COLS).writerow(ligne)
        print(f"{ligne['src_ip']} -> {ligne['dst_ip']}")

print('Capture en cours... (500 paquets)')
sniff(prn=traiter, count=500, store=0)
print('Termine ! Voir data/traffic.csv')
