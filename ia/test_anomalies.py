# ia/test_anomalies.py
import pandas as pd
import joblib

modele = joblib.load('ia/model.pkl')

tests = pd.DataFrame([
    {'taille':500, 'ttl':64, 'protocole':6,'src_port':52000,'dst_port':80}, # Normal
    {'taille':50000,'ttl':64, 'protocole':6,'src_port':52000,'dst_port':80}, # Trop gros
    {'taille':40, 'ttl':1, 'protocole':6,'src_port':12345,'dst_port':31337}, # Scan
    {'taille':100, 'ttl':128,'protocole':17,'src_port':666, 'dst_port':4444}, # Suspect
])
for i, p in enumerate(modele.predict(tests)):
    r = 'NORMAL' if p==1 else 'ANOMALIE'
    print(f'Test {i+1}: {r}')
