import time

import config.settings as settings

from collector.collector import load_logs

from analyzer.analyzer import run_analysis


monitor_running = False


def run_monitor():

    global monitor_running

    monitor_running = True

    while monitor_running:

        if settings.DEBUG_MODE:

            print(
                "\n[DEBUG] Starting analysis cycle"
            )

        load_logs()

        run_analysis()

        if settings.DEBUG_MODE:

            print(
                "\n[DEBUG] Analysis cycle completed"
            )

            print(
                "\n[DEBUG] Waiting next cycle..."
            )

        else:

            print(
                "\n[SCAN ENGINE] Waiting next cycle..."
            )

        time.sleep(
            settings.MONITOR_INTERVAL
        )


def stop_monitor():

    global monitor_running

    monitor_running = False

    print(
        "\n[+] Monitoring stopped\n"
    )