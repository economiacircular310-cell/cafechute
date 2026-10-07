"""Utilidades de mantenimiento.

    python manage.py hash-password     → genera ADMIN_PASSWORD_HASH para el .env
    python manage.py secret-key        → genera un SECRET_KEY aleatorio
    python manage.py init-db           → crea la base de datos si no existe
"""
import getpass
import secrets
import sys

from werkzeug.security import generate_password_hash


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "hash-password":
        pw = getpass.getpass("Contraseña del panel (mín. 12 caracteres): ")
        if len(pw) < 12:
            sys.exit("Usa al menos 12 caracteres.")
        if pw != getpass.getpass("Repítela: "):
            sys.exit("No coinciden.")
        print("\nAñade esta línea a tu .env:\nADMIN_PASSWORD_HASH=" + generate_password_hash(pw))
    elif cmd == "secret-key":
        print("SECRET_KEY=" + secrets.token_hex(32))
    elif cmd == "init-db":
        from app import create_app
        create_app()
        print("Base de datos lista.")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
