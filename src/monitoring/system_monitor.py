##### LIBRERÍAS
import threading
import time

class SystemMonitor:
    """Guarda métricas básicas del servicio mientras la API está activa."""

    def __init__(self): # Momento en que comienza el monitor. Se usa para calcular el tiempo activo.
        self.started_at = time.time()

        # Contadores que se actualizan cada vez que la API recibe una solicitud.
        self.total_requests = 0
        self.error_requests = 0
        self.total_latency_ms = 0.0

        # El Lock evita que dos solicitudes cambien los contadores al mismo tiempo.
        self._lock = threading.Lock()

    def record_request(self, latency_ms, status_code):
        """Registra el tiempo y el resultado de una solicitud atendida."""
        with self._lock:
            # Se suma una solicitud y su tiempo de respuesta.
            self.total_requests += 1
            self.total_latency_ms += latency_ms

            # Los códigos HTTP 500 o mayores se consideran errores del servidor.
            if status_code >= 500:
                self.error_requests += 1

    def get_metrics(self):
        """Calcula y devuelve las métricas actuales del servicio."""
        # Se usa un mínimo pequeño para evitar una división entre cero al iniciar.
        uptime_seconds = max(time.time() - self.started_at, 0.001)
        total = self.total_requests

        # Si todavía no hay solicitudes, la tasa de error se considera cero.
        error_rate = self.error_requests / total if total else 0.0

        # Las métricas se devuelven en un diccionario que FastAPI convierte a JSON.
        return {
            "latency_avg_ms": round(self.total_latency_ms / total, 3) if total else 0.0,
            "throughput_requests_per_second": round(total / uptime_seconds, 4),
            "error_rate": round(error_rate, 4),
            "availability": round(1 - error_rate, 4),
            "total_requests": total,
            "uptime_seconds": round(uptime_seconds, 2),
        }
