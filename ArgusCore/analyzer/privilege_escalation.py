from database.connection import get_connection

from utils.security_logger import security_logger

from utils.incident_manager import generate_incident_id


def detect_privilege_escalation():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            username,
            event_type,
            COUNT(*) as total
        FROM logs
        WHERE event_type IN (
            'admin_granted',
            'role_changed',
            'privilege_escalation'
        )
        GROUP BY username, event_type;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    for username, event_type, total in results:

        incident_id = generate_incident_id()

        message = (
            f"[{incident_id}] "
            f"[PRIVILEGE ESCALATION] "
            f"User: {username} "
            f"| Event: {event_type} "
            f"| Count: {total}"
        )

        print(message)

        security_logger.info(message)

    cursor.close()

    conn.close()