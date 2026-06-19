import psycopg2

import config.settings as settings

from database.connection import get_connection


def load_logs():

    if settings.DEBUG_MODE:

        print(
            "[DEBUG] Inserting simulated logs"
        )

    conn = get_connection()

    cursor = conn.cursor()

    logs = [

        (
            "Firewall",
            "192.168.1.10",
            "failed_login",
            "high"
        ),

        (
            "IDS",
            "10.0.0.5",
            "port_scan",
            "critical"
        )

    ]

    query = """
        INSERT INTO logs (
            timestamp,
            source,
            ip_address,
            event_type,
            severity
        )
        VALUES (
            NOW(),
            %s,
            %s,
            %s,
            %s
        )
    """

    if settings.DEBUG_MODE:

        print(query)

    cursor.executemany(query, logs)

    conn.commit()

    cursor.close()

    conn.close()

    if settings.DEBUG_MODE:

        print(
            "[DEBUG] Logs inserted successfully"
        )