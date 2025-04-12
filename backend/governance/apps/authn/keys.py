import os
import time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Use an environment variable to specify the keys directory; default to /keys.
KEYS_DIR = Path(os.environ.get("KEYS_DIR", "/keys"))
KEYS_GRACE_PERIOD = int(os.environ.get("KEYS_GRACE_PERIOD", 7200))
KEYS_DIR.mkdir(parents=True, exist_ok=True)

# Cache for keys with a timestamp for when they were last loaded.
_key_cache = {
    "last_loaded": 0,
    "private_key": None,
    "public_keys": {},  # dict of {kid: public_key_str}
    "current_kid": None,
}

def generate_initial_keys():
    """Generate an initial RSA key pair and save them with version 1. Failsafe in case volume disappears."""
    new_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = new_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = new_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    version = 1
    priv_path = KEYS_DIR / f"jwt_private_v{version}.pem"
    pub_path = KEYS_DIR / f"jwt_public_v{version}.pem"
    with open(priv_path, "wb") as f:
        f.write(private_pem)
    os.chmod(priv_path, 0o600)
    with open(pub_path, "wb") as f:
        f.write(public_pem)
    return version

def load_keys(force=False, cache_timeout=3600):
    """
    Load RSA keys from disk into memory.
    - Refreshes the cache if forced or if cache_timeout has passed.
    - Uses a 'minimum key age' (default 2 hours) to determine the active key.
      If the newest key is younger than min_age and an older key exists,
      the function will use the previous key for signing.
    """
    if force or time.time() - _key_cache["last_loaded"] > cache_timeout:
        # Look for private key files.
        priv_files = list(KEYS_DIR.glob("jwt_private_*.pem"))
        if not priv_files:
            generate_initial_keys()
            priv_files = list(KEYS_DIR.glob("jwt_private_*.pem"))
        # Get sorted versions (as integers).
        versions = sorted(int(f.name.split("_v")[1].split(".pem")[0]) for f in priv_files)
        latest_version = versions[-1]
        latest_key_path = KEYS_DIR / f"jwt_private_v{latest_version}.pem"
        # Check the age of the newest key.
        age = time.time() - latest_key_path.stat().st_mtime
        if age < KEYS_GRACE_PERIOD and len(versions) > 1:
            # Use the previous key if available.
            active_version = str(versions[-2])
        else:
            active_version = str(latest_version)
        # Load the active private key.
        priv_path = KEYS_DIR / f"jwt_private_v{active_version}.pem"
        with open(priv_path, "rb") as f:
            _key_cache["private_key"] = f.read()
        # Load all public keys.
        pub_files = list(KEYS_DIR.glob("jwt_public_*.pem"))
        new_public_keys = {}
        for pub_file in pub_files:
            ver = int(pub_file.name.split("_v")[1].split(".pem")[0])
            with open(pub_file, "rb") as f:
                new_public_keys[str(ver)] = f.read().decode("utf-8")
        _key_cache["public_keys"] = new_public_keys
        _key_cache["current_kid"] = active_version
        _key_cache["last_loaded"] = time.time()
    return _key_cache

load_keys()