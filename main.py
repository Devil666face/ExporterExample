#!./venv/bin/python
import random
from http.server import HTTPServer
from prometheus_client import (
    MetricsHandler,
    Gauge,
    Counter,
    Summary,
    Histogram,
)


class MyExporter:
    def __init__(self):
        self.cpu_utilization = Gauge("cpu_utilization", "CPU utilization in percentage")
        self.memory_utilization = Gauge(
            "memory_utilization", "Memory utilization in percentage"
        )
        self.request_counter = Counter("myapp_requests", "Number of requests received")
        self.c = Counter("cc", "A counter")
        self.g = Gauge("gg", "A gauge")
        self.s = Summary("ss", "A summary", ["a", "b"])
        self.h = Histogram("hh", "A histogram")
        self.string = Gauge("s_param", "S param", ["string"])

    def collect_metrics(self):
        self.cpu_utilization.set(random.uniform(0, 100))
        self.memory_utilization.set(random.uniform(0, 100))
        self.request_counter.inc()
        self.c.inc()
        self.g.set(17)
        self.s.labels("c", "d").observe(17)
        self.h.observe(0.6)
        self.string.labels(string="foo").set(0)


class HttpHandler(MetricsHandler):
    exporter = MyExporter()

    def do_GET(self):
        if self.path == "/metrics":
            self.exporter.collect_metrics()
            super().do_GET()
        else:
            self.send_error(404)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 80), HttpHandler).serve_forever()
