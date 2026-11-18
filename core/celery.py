# core/celery.py
"""Configuración de la aplicación Celery para el proyecto ERP Django.

Este archivo se importa al iniciar Django para registrar la app de Celery
y auto-descubrir las tareas definidas en tasks.py de cada aplicación.

Uso en Windows (sin Docker):
    # Iniciar worker (procesa tareas)
    celery -A core worker -l info -Q erp_django -P solo

    # Monitorear con Flower
    celery -A core flower --port=5555
"""
import os

from celery import Celery

# Establecer el módulo de configuraciones por defecto de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Instanciar la aplicación Celery
app = Celery('core')

# Cargar configuraciones con el prefijo CELERY_ desde settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir tareas en los archivos tasks.py de todas las apps instaladas
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tarea de diagnóstico para verificar el funcionamiento del worker."""
    print(f'Request: {self.request!r}')