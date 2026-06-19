from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_multi_ip_login():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            username,
            COUNT(DISTINCT ip_address) as unique_ips
        FROM logs
        WHERE event_type = 'login_success'
        GROUP BY username
        HAVING COUNT(DISTINCT ip_address) >= 3;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for username, unique_ips in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[MULTI-IP LOGIN] "
            f"User: {username} "
            f"| IPs: {unique_ips}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()