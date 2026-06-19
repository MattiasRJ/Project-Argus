from analyzer.brute_force import (
    detect_brute_force
)

from analyzer.port_scan import (
    detect_port_scan
)

from analyzer.critical_events import (
    detect_critical_events
)

from analyzer.multi_ip import (
    detect_multi_ip_login
)

from analyzer.privilege_escalation import (
    detect_privilege_escalation
)

from analyzer.ticket_flood import (
    detect_ticket_flood
)

from analyzer.api_abuse import (
    detect_api_abuse
)

import config.settings as settings


DETECTORS = [

    detect_brute_force,

    detect_port_scan,

    detect_critical_events,

    detect_multi_ip_login,

    detect_privilege_escalation,

    detect_ticket_flood,

    detect_api_abuse
]


def run_analysis():

    if settings.DEBUG_MODE:

        print(
            "\n[DEBUG] Starting analysis cycle\n"
        )

    for detector in DETECTORS:

        try:

            if settings.DEBUG_MODE:

                print(
                    f"[DEBUG] Running detector: "
                    f"{detector.__name__}"
                )

            detector()

        except Exception as error:

            print(
                f"[ERROR] Detector "
                f"{detector.__name__} "
                f"failed: {error}"
            )

    if settings.DEBUG_MODE:

        print(
            "\n[DEBUG] Analysis cycle completed\n"
        )