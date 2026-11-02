
import hashlib
import hmac
import os
import re

ITERACIONES = 600_000


def validar_usuario(usuario):
    usuario = usuario.strip().lower()

    if not re.fullmatch(r"[a-z][a-z0-9_]{2,29}", usuario):
        raise ValueError(
            "El usuario debe tener entre 3 y 30 caracteres: "
            "letras, números o _."
        )

    return usuario


def validar_clave(clave):
    if not 10 <= len(clave) <= 128:
        raise ValueError(
            "La contraseña debe contener entre 10 y 128 caracteres."
        )

    return clave


def crear_hash(clave):
    validar_clave(clave)

    sal = os.urandom(16)

    resumen = hashlib.pbkdf2_hmac(
        "sha256",
        clave.encode("utf-8"),
        sal,
        ITERACIONES
    )

    return sal.hex(), resumen.hex()


def verificar_clave(clave, sal_hex, resumen_hex):
    try:
        sal = bytes.fromhex(sal_hex)
        almacenado = bytes.fromhex(resumen_hex)

        calculado = hashlib.pbkdf2_hmac(
            "sha256",
            clave.encode("utf-8"),
            sal,
            ITERACIONES
        )

        return hmac.compare_digest(almacenado, calculado)

    except (ValueError, TypeError, AttributeError):
        return False
