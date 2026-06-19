import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from console.console import start_console

if __name__ == "__main__":
    start_console()