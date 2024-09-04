from saml2.config import IdPConfig

def get_idp_config():
    config = IdPConfig()
    config.load({
        "entityid": "http://localhost:8000/idp/metadata",
        "description": "My Identity Provider",
        "service": {
            "idp": {
                "name": "My Identity Provider",
                "endpoints": {
                    "single_sign_on_service": [
                        ("http://localhost:8000/idp/sso", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect")
                    ],
                },
            },
        },
        "key_file": "./server/keys/private_key.pem",
        "cert_file": "./server/keys/certificate.crt",
        "metadata": {
            "local": ["./server/keys/metadata.xml"],
        },
        "organization": {
            "name": ("My Organization", "en"),
            "display_name": [("My Organization", "en")],
            "url": "http://localhost:8000",
        },
        "contact_person": [
            {
                "given_name": "Admin",
                "sur_name": "User",
                "email_address": ["admin@example.com"],
                "contact_type": "technical",
            },
        ],
    })
    return config