# ventas/tasks.py
"""Tareas asíncronas para la aplicación de ventas — W16.

Las tareas son descubiertas automáticamente por el autodiscover de Celery.
"""
import logging

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name='ventas.enviar_confirmacion_pedido',
)
def enviar_confirmacion_pedido(self, pedido_id: int) -> dict:
    """Procesa el envío del correo de confirmación de compra.

    W16: Registra el evento en el log (placeholder).
    W17: Enviará el correo electrónico mediante la API de SendGrid.
    """
    from ventas.models import Pedido  # Importación local para evitar circularidad

    try:
        pedido = Pedido.objects.select_related('cliente').get(pk=pedido_id)
    except Pedido.DoesNotExist:
        logger.error(f'[Tarea enviar_confirmacion] Pedido {pedido_id} no existe.')
        return {'estado': 'error', 'pedido_id': pedido_id}

    logger.info(
        f'[Tarea enviar_confirmacion] Procesando pedido '
        f'{pedido.numero_pedido} para {pedido.cliente.correo}. '
        f'Total: ${pedido.total_pagado}. '
        f'Timestamp: {timezone.now().isoformat()}'
    )

    return {
        'estado':    'ok',
        'pedido_id': pedido_id,
        'numero':    pedido.numero_pedido,
        'cliente':   pedido.cliente.correo,
    }


@shared_task(
    bind=True,
    max_retries=1,
    name='ventas.verificar_stock_bajo',
)
def verificar_stock_bajo(self, umbral: int = 5) -> dict:
    """Inspecciona el inventario para identificar productos con stock reducido.

    W16: Registra los hallazgos en el log (placeholder).
    W17: Enviará una alerta por correo al administrador.
    W18: Se programará de forma periódica con Celery Beat.
    """
    from productos.models import Producto  # Importación local

    productos_bajos = list(
        Producto.objects
        .filter(activo=True, stock__lt=umbral)
        .values('pk', 'nombre', 'stock')
        .order_by('stock')
    )

    if productos_bajos:
        logger.warning(
            f'[Tarea verificar_stock] {len(productos_bajos)} producto(s) '
            f'con stock < {umbral}: '
            f'{[p["nombre"] for p in productos_bajos]}'
        )
    else:
        logger.info(
            f'[Tarea verificar_stock] Todos los productos tienen stock >= {umbral}. OK.'
        )

    return {
        'umbral':          umbral,
        'productos_bajos': productos_bajos,
        'total':           len(productos_bajos),
    }