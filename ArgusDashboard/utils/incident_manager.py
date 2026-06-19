incident_counter = 0


def generate_incident_id():

    global incident_counter

    incident_counter += 1

    return (
        f"ARG-{incident_counter:05d}"
    )