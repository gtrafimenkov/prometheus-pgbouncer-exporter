#!/usr/bin/python3

# Copyright (C) 2015  Christopher Baines <mail@cbaines.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from prometheus_client.exposition import MetricsHandler

index_page = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Prometheus PgBouncer Exporter</title>
</head>

<body>
  <h1>PgBouncer exporter for Prometheus</h1>

  <p>
    This is a simple exporter for PgBouncer that makes several metrics
    available to Prometheus.
  </p>

  <p>
    Metrics are exported from the SHOW LISTS, STATS, POOLS and DATABASE comand
    output.
  </p>

  <a href="/metrics">View metrics</a>
</body>
</html>
"""


class RequestHandler(MetricsHandler):
    def do_GET(self):
        if self.path == "/metrics":
            return super().do_GET()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(index_page.encode('UTF-8'))
