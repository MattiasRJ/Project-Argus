from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from core.models import Log

def dashboard(request):
    return render(request, "dashboard.html")

def metrics_api(request):
    try:
        ahora = datetime.now()  # naive, igual que la columna timestamp de Log

        # 1. Gráfico en tiempo real (último minuto)
        ventana_tiempo = ahora - timedelta(minutes=1)
        volumen_reciente = Log.objects.filter(timestamp__gte=ventana_tiempo).count()

        # 2. Contadores Históricos (Tarjetas)
        brute_force_count = Log.objects.filter(event_type="failed_login").count()
        port_scan_count = Log.objects.filter(event_type="port_scan").count()
        api_abuse_count = Log.objects.filter(event_type="api_abuse").count()
        priv_esc_count = Log.objects.filter(event_type__in=["admin_granted", "role_changed"]).count()
        multi_ip_count = Log.objects.filter(event_type="multi_ip_login").count()
        ticket_flood_count = Log.objects.filter(event_type="ticket_created").count()

        # 3. Historial para la tabla inferior
        ultimos_logs = Log.objects.all().order_by('-timestamp')[:5]
        recent_events = []

        for log in ultimos_logs:
            if log.event_type in ["failed_login", "admin_granted"]:
                severidad = "High"
            elif log.event_type in ["port_scan", "api_abuse", "multi_ip_login"]:
                severidad = "Medium"
            else:
                severidad = "Low"

            recent_events.append({
                "time": log.timestamp.strftime("%H:%M:%S") if log.timestamp else "N/A",
                "source": getattr(log, 'source', 'Argus System'),
                "ip": getattr(log, 'ip_address', '0.0.0.0'),
                "event": log.event_type.replace('_', ' ').title(),
                "severity": severidad
            })

        # 4. Enviamos TODO al Dashboard
        return JsonResponse({
            "time": ahora.strftime("%H:%M:%S"),
            "current_volume": volumen_reciente,
            "brute_force": brute_force_count,
            "port_scan": port_scan_count,
            "api_abuse": api_abuse_count,
            "privilege_escalation": priv_esc_count,
            "multi_ip": multi_ip_count,
            "ticket_flood": ticket_flood_count,
            "recent_events": recent_events
        })

    except Exception as e:
        print(f"🔥 [Argus Error] Fallo en metrics_api: {e}")
        return JsonResponse({
            "time": datetime.now().strftime("%H:%M:%S"),
            "current_volume": 0, "brute_force": 0, "port_scan": 0,
            "api_abuse": 0, "privilege_escalation": 0, "multi_ip": 0, "ticket_flood": 0,
            "recent_events": []
        })