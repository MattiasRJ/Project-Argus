from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_api_abuse():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            COUNT(*) as requests
        FROM logs
        WHERE event_type = 'api_request'
        GROUP BY ip_address
        HAVING COUNT(*) >= 20;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for ip_address, requests in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[API ABUSE] "
            f"IP: {ip_address} "
            f"| Requests: {requests}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()