from pathlib import Path
import json

async def get_user_schemas():
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "all_schemas.json"
    print(file_path)
    schemas = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            openapi_json = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from file: {file_path}")
        return None
    except Exception as e:
        print(f"Unexpected error while reading the schema file: {e}")
        return None

    components = openapi_json.get("components")
    if not components:
        print("'components' key not found in the OpenAPI data.")
        return None

    schemas_section = components.get("schemas")
    if not schemas_section:
        print("'schemas' key not found in the 'components' section of the OpenAPI data.")
        return None

    for schema_name, schema in schemas_section.items():
        schemas.append({schema_name: schema})
    if not schemas:
        print("No schemas found in the OpenAPI data.")
        return None
    
    return schemas
def parse_openapi_paths_by_id(paths, components, url, target_method):
    path_item = paths.get(url, {})
    if not path_item:
        return None

    resolved_path_item = copy.deepcopy(path_item)

    for method, info in resolved_path_item.items():
        if method != target_method:
            continue
        if info.get("requestBody"):
            info["requestBody"] = resolve_ref(info["requestBody"], components)
        if info.get("responses"):
            info["responses"] = resolve_ref(info["responses"], components)

    return resolved_path_item
async def get_user_operation_by_id(request, url, method):
    
    openapi_json = request.app.openapi()
    components = openapi_json.get("components", {})
    result = parse_openapi_paths_by_id(openapi_json.get("paths", {}), components, url, method)
    return result
