from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_port_scan():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            COUNT(*) as scans
        FROM logs
        WHERE event_type = 'port_scan'
        GROUP BY ip_address
        HAVING COUNT(*) >= 5;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for ip_address, scans in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[PORT SCAN] "
            f"IP: {ip_address} "
            f"| Scans: {scans}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()