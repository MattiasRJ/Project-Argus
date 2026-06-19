from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_ticket_flood():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            COUNT(*) as total_tickets
        FROM logs
        WHERE event_type = 'ticket_created'
        GROUP BY ip_address
        HAVING COUNT(*) >= 10;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for ip_address, total_tickets in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[TICKET FLOOD] "
            f"IP: {ip_address} "
            f"| Tickets: {total_tickets}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()