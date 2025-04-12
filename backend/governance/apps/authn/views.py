import base64
from django.http import JsonResponse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from .keys import load_keys

def jwks_view(request):
    keys_data = load_keys(cache_timeout=60)  # load (or fetch cached) keys, one minute interval as new public keys need to propagate
    jwks_keys = []
    for kid, public_pem in keys_data["public_keys"].items():
        # We have the PEM public key; convert it to JWK fields
        # Using cryptography library to get modulus and exponent
        public_key = serialization.load_pem_public_key(public_pem.encode('utf-8'), backend=default_backend())
        numbers = public_key.public_numbers()
        e = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, 'big')
        n = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, 'big')
        e_b64 = base64.urlsafe_b64encode(e).decode('utf-8').rstrip("=")
        n_b64 = base64.urlsafe_b64encode(n).decode('utf-8').rstrip("=")
        jwks_keys.append({
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig",
            "kid": kid,
            "n": n_b64,
            "e": e_b64
        })
    return JsonResponse({"keys": jwks_keys})
