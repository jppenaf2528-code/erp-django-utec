# Sprint 5 Planning — ERP Django
## Semanas W16–W18 · Espiral 6: Celery e Integraciones

## Sprint Backlog — actualización W16

| Tarea | Estado |
|---|---|
| pip install celery (+ pywin32 en Windows) | ✅ W16 |
| core/celery.py + core/__init__.py | ✅ W16 |
| CELERY_* + broker de archivos en settings.py | ✅ W16 |
| ventas/tasks.py (2 tareas placeholder) | ✅ W16 |
| pago_exitoso: .delay() solo si el pedido está pagado | ✅ W16 |
| webhook: .delay() al confirmar pago | ✅ W16 |
| Worker corriendo (-P solo) y verificado en su log | ✅ W16 |
| Correo transaccional real (Django) | ⏳ W17 |
| Alerta de stock bajo por correo | ⏳ W17 |
| Celery Beat + tareas programadas | ⏳ W18 |

**Total Sprint 5:** 18 puntos

## DoD — Sprint 5
- celery -A core worker -P solo → procesa tareas sin error
- Pago confirmado → tarea de correo en la cola (no espera)
- Correo de confirmación generado una sola vez por pedido (W17)
- Alerta de stock enviada cuando stock < umbral (W17)
- Reporte diario ejecutado a las 8:00 AM (W18)
- python manage.py test → ≥ 155 tests OK al cierre de W16