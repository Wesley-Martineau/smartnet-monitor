import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib, os
 
  # Charger les donnees
df = pd.read_csv('data/traffic.csv')
print(f'{len(df)} paquets charges')
 
  # Verifier que les colonnes existent
colonnes_ia = ['taille', 'ttl', 'protocole', 'src_port', 'dst_port']
manquantes = [c for c in colonnes_ia if c not in df.columns]
if manquantes:
    print(f'ERREUR : colonnes manquantes dans traffic.csv : {manquantes}')
    print(f'Colonnes trouvees : {df.columns.tolist()}')
    print('Verifiez que vous avez utilise le sniffer.py du sujet.')
    exit(1)
 
  # Colonnes pour l'IA (que des chiffres)
features = df[colonnes_ia].fillna(0)
 
  # Entrainer le modele
modele = IsolationForest(
    n_estimators=100,       # 100 arbres
    contamination=0.05,     # ~5% d'anomalies
    random_state=42
)
modele.fit(features)
 
  # Predictions : 1=normal, -1=anomalie
df['prediction'] = modele.predict(features)
df['score'] = modele.decision_function(features)
 
nb = len(df[df['prediction'] == -1])
print(f'Anomalies detectees : {nb}')
 
  # Sauvegarder
os.makedirs('ia', exist_ok=True)
joblib.dump(modele, 'ia/model.pkl')
df.to_csv('data/traffic_analyse.csv', index=False)
print('Modele sauvegarde !')
