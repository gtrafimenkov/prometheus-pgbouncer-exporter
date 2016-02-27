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

import logging
import configargparse

from os.path import join, dirname, normpath
from http.server import HTTPServer
from prometheus_client.core import REGISTRY

from . import __version__
from .utils import get_connection
from .exposition import create_request_handler
from .collectors import StatsCollector, ListsCollector, PoolsCollector, \
    DatabasesCollector


def main():
    p = configargparse.ArgParser(
        prog="prometheus-pgbouncer-exporter",
    )

    p.add(
        '--version',
        action='store_true',
        help="Show the version",
    )

    p.add(
        '-c',
        '--config',
        is_config_file=True,
        help='config file path',
    )

    p.add(
        '--port',
        default='9127',
        help="Port on which to expose metrics",
        type=int,
        env_var='PORT',
    )
    p.add(
        '--host',
        default='0.0.0.0',
        help="Host on which to expose metrics",
        env_var='HOST',
    )

    p.add(
        '--pgbouncer-port',
        default='6432',
        help="Port to connect to pgbouncer",
        env_var='PGBOUNCER_PORT',
    )
    p.add(
        '--pgbouncer-user',
        default='pgbouncer',
        help="User to connect to pgbouncer with",
        env_var='PGBOUNCER_USER',
    )
    p.add(
        '--pgbouncer-host',
        default=None,
        help="Host on which to connect to pgbouncer",
        env_var='PGBOUNCER_HOST',
    )

    p.add(
        '--database',
        action='append',
        help="Databases to report metrics for, if this is not specified, all metrics will be reported",
        env_var='PGBOUNCER_DATABASES',
    )

    p.add(
        '--licence-location',
        default=join(dirname(dirname(normpath(__file__))), 'LICENSE'),
        help="The location of the licence, linked to through the web interface",
        env_var='LICENCE_LOCATION',
    )

    options = p.parse_args()

    if options.version:
        print("prometheus-pgbouncer-exporter %s" % __version__)
        return

    logging.basicConfig(level=logging.DEBUG)

    logging.info(p.format_values())

    connection = get_connection(
        options.pgbouncer_user,
        options.pgbouncer_port,
        options.pgbouncer_host,
    )

    REGISTRY.register(StatsCollector(
        connection=connection,
        databases=options.database,
    ))

    REGISTRY.register(PoolsCollector(
        connection=connection,
        databases=options.database,
    ))

    REGISTRY.register(DatabasesCollector(
        connection=connection,
        databases=options.database,
    ))

    REGISTRY.register(ListsCollector(
        connection=connection,
    ))

    httpd = HTTPServer(
        (options.host, options.port),
        create_request_handler(options.licence_location),
    )

    logging.info("Listing on port %s:%d" % (options.host, options.port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        connection.close()
