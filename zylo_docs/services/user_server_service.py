from collections import defaultdict
import copy

async def get_user_schemas(request):
    schemas = []

    openapi_json = request.app.openapi()
    if openapi_json.get("components") is None:
        print("OpenAPI data does not contain 'components' key.")
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

def parse_openapi_paths(paths):
    grouped = defaultdict(list)

    for path, methods in paths.items():
        for method, info in methods.items():
            tag = (info.get("tags") or ["default"])[0]

            grouped[tag].append({
                "operationId": info.get("operationId", ""),
                "method": method.upper(),
                "path": path,
                "summary": info.get("summary", "")
            })
    return {
        "operationGroups": [
            {
                "tag": tag,
                "operations": operation
            } for tag, operation in grouped.items()
        ]
    
    }

async def get_user_operation(request):
    openapi_json = request.app.openapi()
    result = parse_openapi_paths(openapi_json.get("paths", {}))
    return result

def resolve_ref(obj, components):
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref_path = obj['$ref'].strip('#/').split('/')
            ref = components
            for key in ref_path[1:]:
                if not isinstance(ref, dict) or key not in ref:
                    return obj
                ref = ref[key]
            return resolve_ref(ref, components)
        else:
            return {k: resolve_ref(v, components) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_ref(item, components) for item in obj]
    else:
        return obj

def parse_openapi_paths_by_id(paths, components, path, target_method):
    path_item = paths.get(path, {})
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

async def get_user_operation_by_id(request, path, method):

    openapi_json = request.app.openapi()
    components = openapi_json.get("components", {})
    result = parse_openapi_paths_by_id(openapi_json.get("paths", {}), components, path, method)
    return result
