"""
ArgusCore — Collector
Inserta logs simulados variados en la BD para alimentar el dashboard en tiempo real.
Cada ciclo genera eventos distintos para que los contadores suban progresivamente.
"""

import random
import psycopg2

import config.settings as settings
from database.connection import get_connection


# Catálogo de eventos con sus pesos de probabilidad
EVENT_CATALOG = [
    # (source, ip_pool, event_type, severity_options, weight)
    ("Firewall",  ["192.168.1.10", "192.168.1.11", "10.10.0.5"],  "failed_login",      ["high", "medium"],          40),
    ("IDS",       ["10.0.0.5",     "172.16.0.3",   "10.0.0.99"],  "port_scan",         ["critical", "high"],        30),
    ("WebProxy",  ["203.0.113.7",  "198.51.100.4"],               "api_abuse",         ["medium", "high"],          10),
    ("SIEM",      ["10.10.1.50",   "192.168.2.20"],               "multi_ip_login",    ["high"],                    8),
    ("Ticketing", ["10.0.1.100",   "10.0.1.101"],                 "ticket_created",    ["low", "medium"],           7),
    ("IAM",       ["192.168.0.50"],                               "admin_granted",     ["critical"],                5),
]


def _random_events(n: int = None) -> list:
    """Genera entre 1 y 4 eventos aleatorios ponderados."""
    if n is None:
        n = random.randint(1, 4)

    population = EVENT_CATALOG
    weights = [e[4] for e in population]
    chosen = random.choices(population, weights=weights, k=n)

    rows = []
    for source, ips, event_type, severities, _ in chosen:
        rows.append((
            random.choice(ips),
            source,
            event_type,
            random.choice(severities),
        ))
    return rows


def load_logs():
    if settings.DEBUG_MODE:
        print("[DEBUG] Insertando logs simulados en PostgreSQL")

    conn = get_connection()
    cursor = conn.cursor()

    events = _random_events()

    query = """
        INSERT INTO logs (
            timestamp,
            source,
            ip_address,
            event_type,
            severity,
            username,
            processed
        )
        VALUES (
            NOW(),
            %s,
            %s,
            %s,
            %s,
            %s,
            FALSE
        )
    """

    rows = [
        (source, ip, event_type, severity, "system")
        for ip, source, event_type, severity in events
    ]

    cursor.executemany(query, rows)
    conn.commit()

    if settings.DEBUG_MODE:
        print(f"[DEBUG] {len(rows)} log(s) insertados:")
        for r in rows:
            print(f"  → {r[2]} | {r[3]} | {r[1]}")

    cursor.close()
    conn.close()