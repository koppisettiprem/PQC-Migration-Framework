import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def detect_algorithm(host, port):

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((host, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:

            tls_version = ssock.version()
            cipher_suite = ssock.cipher()[0]

            cert_bin = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_bin, default_backend())

            public_key = cert.public_key()
            algo_name = public_key.__class__.__name__

            try:
                key_size = public_key.key_size
            except:
                key_size = "Unknown"

            signature_algorithm = cert.signature_algorithm_oid._name
            issuer = cert.issuer.rfc4514_string()
            subject = cert.subject.rfc4514_string()

            return {
                "algorithm": algo_name,
                "key_size": key_size,
                "tls_version": tls_version,
                "cipher_suite": cipher_suite,
                "signature_algorithm": signature_algorithm,
                "issuer": issuer,
                "subject": subject
            }