from django.core.management.base import BaseCommand
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os
from pathlib import Path

class Command(BaseCommand):
    help = "Rotate JWT signing keys by generating a new RSA key pair"

    def handle(self, *args, **options):
        # Generate new RSA private key
        new_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        # Serialize private and public halves
        private_pem = new_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = new_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # Determine new version number by scanning existing files
        keys_dir = Path(os.environ.get("KEYS_DIR", "/keys"))
        existing = [f.name for f in keys_dir.glob("jwt_private_*.pem")]
        if existing:
            latest = max(int(name.split("_v")[1].split(".pem")[0]) for name in existing)
        else:
            latest = 0
        new_version = latest + 1
        # Define filenames for new keys
        priv_filename = f"jwt_private_v{new_version}.pem"
        pub_filename = f"jwt_public_v{new_version}.pem"
        priv_path = keys_dir / priv_filename
        pub_path = keys_dir / pub_filename
        # Write the key files
        with open(priv_path, "wb") as f:
            f.write(private_pem)
        # Set restrictive permissions on private key (readable only by owner)
        os.chmod(priv_path, 0o600)
        with open(pub_path, "wb") as f:
            f.write(public_pem)

        self.stdout.write(self.style.SUCCESS(f"Generated new key pair version {new_version}: {priv_filename}, {pub_filename}"))
