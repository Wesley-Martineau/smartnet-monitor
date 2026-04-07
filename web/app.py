# web/app.py
from flask import Flask, jsonify, render_template
import sqlite3, joblib, pandas as pd, os

app = Flask(__name__)
modele = joblib.load('ia/model.pkl')

def get_db():
    conn = sqlite3.connect('data/smartnet.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS trafic (id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp TEXT, src_ip TEXT, dst_ip TEXT,protocole INT, taille INT, ttl INT,src_port INT, dst_port INT,est_anomalie INT DEFAULT 0, score REAL)''')
    db.commit()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def stats():
    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM trafic').fetchone()[0]
    anom = db.execute('SELECT COUNT(*) FROM trafic WHERE est_anomalie=1').fetchone()[0]
    return jsonify({'total': total,'anomalies': anom,'taux': round(anom/max(total,1)*100, 1)
    })

@app.route('/api/anomalies')
def anomalies():
    db = get_db()
    rows = db.execute('SELECT * FROM trafic WHERE est_anomalie=1 ''ORDER BY id DESC LIMIT 50').fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__':
    init_db()
    if os.path.exists('data/traffic_analyse.csv'):
        df = pd.read_csv('data/traffic_analyse.csv')
        db = get_db()
        for _, r in df.iterrows():
            db.execute('INSERT INTO trafic ''(timestamp,src_ip,dst_ip,protocole,''taille,ttl,src_port,dst_port,''est_anomalie,score) VALUES ''(?,?,?,?,?,?,?,?,?,?)',
                        (r['timestamp'], r['src_ip'], r['dst_ip'],r['protocole'], r['taille'], r['ttl'],r['src_port'], r['dst_port'],1 if r.get('prediction')==-1 else 0,r.get('score', 0)))
        db.commit()
    app.run(debug=True, port=5000)