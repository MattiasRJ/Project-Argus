from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_brute_force():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            COUNT(*) as attempts
        FROM logs
        WHERE event_type = 'failed_login'
        GROUP BY ip_address
        HAVING COUNT(*) >= 5;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for ip_address, attempts in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[BRUTE FORCE] "
            f"IP: {ip_address} "
            f"| Attempts: {attempts}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()