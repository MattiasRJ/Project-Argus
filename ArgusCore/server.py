"""
ArgusCore — Flask API Server
Lee métricas REALES desde PostgreSQL (misma BD que ArgusDashboard).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import psycopg2

load_dotenv(encoding="utf-8")

app = Flask(__name__)
CORS(app)

DASHBOARD_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'ArgusDashboard', 'core', 'templates', 'dashboard.html')
)


def get_db_connection():
    """Conexión a PostgreSQL usando las mismas variables de entorno que ArgusCore."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


def query_count(cursor, event_type):
    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE event_type = %s",
        (event_type,)
    )
    return cursor.fetchone()[0]


@app.route('/')
def home():
    if os.path.exists(DASHBOARD_PATH):
        return send_file(DASHBOARD_PATH)
    return f"""
        <h1>⚠️ Dashboard No Encontrado</h1>
        <p>Buscando en: <code>{DASHBOARD_PATH}</code></p>
    """, 404


@app.route('/api/metrics')
def get_live_metrics():
    """
    Endpoint de telemetría en tiempo real.
    Lee conteos REALES desde la tabla 'logs' de PostgreSQL.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        brute     = query_count(cur, "failed_login")
        port      = query_count(cur, "port_scan")
        ticket    = query_count(cur, "ticket_created")
        multi     = query_count(cur, "multi_ip_login")
        api       = query_count(cur, "api_abuse")
        privilege = query_count(cur, "admin_granted")

        cur.close()
        conn.close()

        current_volume = brute + port + ticket + multi + api + privilege

        return jsonify({
            "time": datetime.now().strftime("%H:%M:%S"),
            "current_volume": current_volume,
            "metrics": {
                "brute":     brute,
                "port":      port,
                "ticket":    ticket,
                "multi":     multi,
                "api":       api,
                "privilege": privilege
            }
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "time": datetime.now().strftime("%H:%M:%S"),
            "current_volume": 0,
            "metrics": {
                "brute": 0, "port": 0, "ticket": 0,
                "multi": 0, "api": 0, "privilege": 0
            }
        }), 500


@app.route('/api/status')
def get_status():
    return jsonify({
        "status": "ONLINE",
        "version": "1.1.0",
        "detectors": 7,
        "server_time": datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 48)
    print("  🛡️  ArgusCore — Servidor Flask")
    print(f"  Dashboard en: http://127.0.0.1:5000")
    print(f"  API métricas: http://127.0.0.1:5000/api/metrics")
    print("=" * 48)
    app.run(debug=True, port=5000)