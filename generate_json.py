import re
import json

def clean_docstring(docstring):
    """
    Cleans the docstring by removing asterisks and leading/trailing whitespace.
    """
    return re.sub(r'^\s*\*\*?\s*|^\s*|\s*$|^\*', '', docstring, flags=re.MULTILINE).strip()

def extract_json_from_docstring(docstring):
    """
    Extracts JSON and API details from a C++ Doxygen-style docstring.
    """
    cleaned_docstring = clean_docstring(docstring)
    
    # Extract brief description
    brief_match = re.search(r'@brief\s+(.*?)(?:\n|$)', cleaned_docstring)
    brief = brief_match.group(1).strip() if brief_match else "No description available"

    # Improved regex patterns for JSON extraction with better multiline handling
    request_pattern = r'@Request\s*:\s*(\{(?:[^{}]|(?:\{[^{}]*\}))*\}|\[(?:[^\[\]]|(?:\{[^{}]*\}))*\])'
    response_pattern = r'@Response\s*:\s*(\{(?:[^{}]|(?:\{[^{}]*\}))*\}|\[(?:[^\[\]]|(?:\{[^{}]*\}))*\])'
    
    request_match = re.search(request_pattern, cleaned_docstring, re.DOTALL)
    response_match = re.search(response_pattern, cleaned_docstring, re.DOTALL)
    
    # Extract status code if present
    status_match = re.search(r'@Status\s*:\s*(\d{3}[^"\n]*)', cleaned_docstring)
    status_description = status_match.group(1) if status_match else "200 OK"

    def parse_json(json_text):
        """Helper function to parse JSON with better error handling"""
        if not json_text:
            return None
            
        try:
            # Normalize the JSON text
            normalized = re.sub(r'\s+', ' ', json_text)  # Normalize whitespace
            normalized = normalized.replace('\n', '').strip()
            return json.loads(normalized)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Problematic JSON: {normalized}")
            return None

    example_request = parse_json(request_match.group(1)) if request_match else None
    example_response = parse_json(response_match.group(1)) if response_match else None

    return {
        "brief": brief,
        "request": example_request,
        "response": example_response,
        "status": status_description
    }

def extract_function_parameters(endpoint):
    """
    Extracts parameters from the endpoint.
    """
    path_params = re.findall(r"\{(\w+)\}", endpoint)
    parameters = []

    for param in path_params:
        parameters.append({
            "name": param,
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
            "description": f"Path parameter {param}"
        })

    return parameters

def determine_schema_type(example_data):
    """
    Determines the correct schema type and format based on the example data.
    """
    if isinstance(example_data, list):
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {}
            }
        }
    elif isinstance(example_data, dict):
        return {
            "type": "object",
            "properties": {}
        }
    else:
        return {"type": "object", "properties": {}}

def generate_openapi_from_cpp(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        route_pattern = re.compile(r'CROW_ROUTE\(app, "(.*?)"\)\.methods\((.*?)\)\(.*?\{', re.DOTALL)
        method_mapping = {
            "crow::HTTPMethod::Get": "get",
            "crow::HTTPMethod::Post": "post",
            "crow::HTTPMethod::Put": "put",
            "crow::HTTPMethod::Delete": "delete"
        }

        openapi_json = {
            "openapi": "3.0.0",
            "info": {
                "title": "C++ Crow CRUD API",
                "version": "1.0.0",
                "description": "Auto-generated OpenAPI spec from C++ Doxygen comments."
            },
            "servers": [
                {
                    "url": "https://api.example.com/v1",
                    "description": "Main (production) server"
                }
            ],
            "paths": {}
        }

        for match in route_pattern.finditer(content):
            path, methods = match.groups()
            path = path.replace("<int>", "{id}")
            methods = [method_mapping[m.strip()] for m in methods.split(',') if m.strip() in method_mapping]

            docstring_start = content.rfind("/**", 0, match.start())
            docstring_end = content.find("*/", docstring_start) + 2
            docstring = content[docstring_start:docstring_end]

            api_details = extract_json_from_docstring(docstring)

            if path not in openapi_json["paths"]:
                openapi_json["paths"][path] = {}

            for method in methods:
                status_code = api_details["status"].split()[0]
                request_schema = determine_schema_type(api_details["request"]) if api_details["request"] else None
                response_schema = determine_schema_type(api_details["response"]) if api_details["response"] else None

                openapi_json["paths"][path][method] = {
                    "summary": api_details["brief"],
                    "description": api_details["brief"],
                    "parameters": extract_function_parameters(path),
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": request_schema,
                                "example": api_details["request"]
                            }
                        }
                    } if api_details["request"] else {},
                    "responses": {
                        status_code: {
                            "description": api_details["status"],
                            "content": {
                                "application/json": {
                                    "schema": response_schema,
                                    "example": api_details["response"]
                                }
                            }
                        } if api_details["response"] else {
                            "description": api_details["status"]
                        }
                    }
                }

        output_filename = "openapi.json"
        with open(output_filename, "w", encoding="utf-8") as json_file:
            json.dump(openapi_json, json_file, indent=4)

        print(f"✅ OpenAPI JSON saved as {output_filename}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    generate_openapi_from_cpp("crudapi.cpp")