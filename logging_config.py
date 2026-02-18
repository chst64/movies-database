# logging_config.py
# Configuracion del logger
#

import logging
import os

# from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler


def setup_logging(max_size_mb=5, backup_count=3):
    # Asegurarse que la carpeta logs existe
    os.makedirs("logs", exist_ok=True)

    # Crear logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)  # Nivel mínimo para todos los handlers

    # Ruta completa al archivo de log dentro de la carpeta logs
    log_file = os.path.join("logs", "app.log")

    # Rotación por tamaño: no supera max_size_mb MB, guarda hasta backup_count copias
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_size_mb * 1024 * 1024,  # Tamaño máximo en bytes
        backupCount=backup_count,  # Número de copias a guardar
        encoding="utf8",
    )

    file_handler.setLevel(logging.WARNING)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Handler para consola: solo muestra CRITICAL
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Añadir handlers al logger principal
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Configuración específica para Peewee y Werkzeug
    logging.getLogger("peewee").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    # == Logger específico para pruebas ==
    logger_pruebas = logging.getLogger("pruebas")
    logger_pruebas.setLevel(logging.INFO)

    # Handler específico para pruebas
    pruebas_log_file = os.path.join("logs", "logger_pruebas.log")
    pruebas_file_handler = RotatingFileHandler(
        pruebas_log_file,
        maxBytes=max_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf8",
    )
    pruebas_file_handler.setLevel(logging.INFO)
    pruebas_formatter = logging.Formatter(
        "%(asctime)s - [PRUEBAS] - %(levelname)s - %(message)s"
    )
    pruebas_file_handler.setFormatter(pruebas_formatter)

    logger_pruebas.addHandler(pruebas_file_handler)

    # Los logs CRITICAL y WARNING aparecen tambien en log.pruebas
    logger.addHandler(pruebas_file_handler)  # Así los logs también van a app.log
