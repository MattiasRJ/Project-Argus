from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_critical_events():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            event_type,
            ip_address,
            COUNT(*) as total
        FROM logs
        WHERE severity = 'critical'
        GROUP BY event_type, ip_address;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for event_type, ip_address, total in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[CRITICAL EVENT] "
            f"{event_type} "
            f"from {ip_address} "
            f"| Events: {total}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()