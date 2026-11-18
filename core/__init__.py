# core/__init__.py
"""Inicialización del paquete core del ERP.

Registra la app Celery para habilitar el uso del decorador @shared_task.
"""
from .celery import app as celery_app

__all__ = ('celery_app',)