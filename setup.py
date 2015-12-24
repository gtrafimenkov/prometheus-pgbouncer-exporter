from setuptools import setup, find_packages

setup(
    name="prometheus-pgbouncer-exporter",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'prometheus-pgbouncer-exporter = prometheus_pgbouncer_exporter.cli:main',
        ],
    },
)
