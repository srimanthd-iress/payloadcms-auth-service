from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from saml2 import BINDING_HTTP_POST
from saml2.metadata import entity_descriptor
from saml2.sigver import security_context
from saml2.server import Server
from .config import get_idp_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

idp_config = get_idp_config()
idp_server = Server(config=idp_config)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/idp/metadata")
async def metadata():
    metadata_str = entity_descriptor(idp_config).to_string().decode("utf-8")
    return Response(content=metadata_str, media_type="application/xml")

@app.get("/idp/sso")
async def sso():
    # Prepare a standard SAML response
    response_id = "123456"
    destination = "http://localhost:3000/auth/callback"
    sp_entity_id = "https://example-sp.com"

    IDP = Server(config=idp_config)

    # TODO get user and caps from xplan

    # Create the SAML response
    resp = IDP.create_authn_response(
        identity={"email_address": "srimanth.duggineni@iress.com", "sites": ["site1", "site2"]},
        userid="user123",
        in_response_to=response_id,
        destination=destination,
        sp_entity_id=sp_entity_id,
        binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
        sign_response=True,
        sign_assertion=True,
    )

    # Sign the response
    security_context(idp_config).sign_statement(resp, node_name="Response")

    # Apply binding
    http_info = IDP.apply_binding(BINDING_HTTP_POST, resp, destination, response_id, True)

    # Redirect the user to the SP
    return Response(content=http_info["data"], media_type="text/html")

