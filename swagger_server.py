from fastapi import FastAPI
import json
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# Load OpenAPI Spec
with open("D:\\10\\openapi.json", "r", encoding="utf-8") as f:
    openapi_spec = json.load(f)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Use the loaded specification 
    app.openapi_schema = openapi_spec
    return app.openapi_schema

app.openapi = custom_openapi

# Dynamic route generation based on OpenAPI spec
for path, path_item in openapi_spec.get('paths', {}).items():
    for method, operation in path_item.items():
        # Convert path parameters from {param} to FastAPI format
        fastapi_path = path.replace('{', '{param_')
        
        def create_route_handler(method_details):
            async def route_handler(*args, **kwargs):
                # Simple placeholder response generation
                return {"message": f"{method.upper()} request to {path}"}
            return route_handler
        
        # Dynamically add routes
        if method == 'get':
            app.get(fastapi_path)(create_route_handler(operation))
        elif method == 'post':
            app.post(fastapi_path)(create_route_handler(operation))
        elif method == 'put':
            app.put(fastapi_path)(create_route_handler(operation))
        elif method == 'delete':
            app.delete(fastapi_path)(create_route_handler(operation))

@app.get("/")
def root():
    return {"message": "Go to /docs for Swagger UI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("swagger_server:app", host="127.0.0.1", port=8000, reload=True)