#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(current_path)
sys.path.append(cityframe_path)
from data.database.data_population_scripts import update_weather_fc, update_weather_current
from data import machine_learning_app


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_app.settings_dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    update_weather_current.update_weather()
    update_weather_fc.main()
    machine_learning_app.main()
    main()
