import requests
import json
import yaml
import jsonref
from openapi_spec_validator import validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


def load_openapi_spec_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch OpenAPI spec from {url}. Status code: {response.status_code}"
        )
    try:
        return response.json()
    except json.JSONDecodeError:
        return yaml.safe_load(response.text)



def load_openapi_spec_from_string(spec_string):
    """Load OpenAPI spec from a string/text input (YAML)."""
    try:
        return yaml.safe_load(spec_string) 
    except Exception as e:
        print(e)


def validate_openapi_spec(spec):
    """Validate the OpenAPI spec."""
    try:
        validate(spec)
        print("OpenAPI spec is valid.")
    except OpenAPIValidationError as e:
        raise Exception(f"OpenAPI spec is invalid: {e}")


def check_server_availability(spec):
    """Check if the server URL in the OpenAPI spec is available."""
    servers = spec.get("servers", [])
    if not servers:
        raise Exception("No server URLs found in the OpenAPI spec.")



def inline_schemas(spec):
    """Bring referenced schemas inline by resolving $ref fields."""
    inlined_spec = jsonref.JsonRef.replace_refs(spec)
    return inlined_spec


def add_server_details_if_missing(spec, base_url):
    """Insert server details into the OpenAPI spec if the 'servers' section is missing."""
    if "servers" not in spec or not spec["servers"]:
        spec["servers"] = [{"url": base_url}]
        print(f"Added server URL: {base_url}")
    return spec


def load_and_process_openapi_spec(input_type, input_value):
 
    # Load the spec based on the input type
    if input_type == "url":
        spec = load_openapi_spec_from_url(input_value)
    elif input_type == "string":
        spec = load_openapi_spec_from_string(input_value)
    else:
        raise ValueError("Invalid input type. Must be 'url', or 'string'.")

    # Step1: Validate that base_url/server url is provided in the spec
    #check_server_availability(spec)

    # Step 2: Validate the OpenAPI spec
    #validate_openapi_spec(spec)

    # Step 3: Inline any referenced schemas
    inlined_spec = inline_schemas(spec)

    # send inlined_spec to frontend to display openapi spec text area - provide the user with a message that 
    
    print(inlined_spec)



if __name__ == "__main__":
    # Example usage:

    # Load from a URL (JSON or YAML)
    input_type = "url"
    input_value = "https://supply-chain-api.azurewebsites.net/openapi.json"



    load_and_process_openapi_spec(input_type, input_value)
