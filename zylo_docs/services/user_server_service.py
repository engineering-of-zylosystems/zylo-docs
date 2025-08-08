from collections import defaultdict
import copy
from zylo_docs.services.openapi_service import OpenApiService

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
    service: OpenApiService = request.app.state.openapi_service
    openapi_json = service.get_current_spec()
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
def resolve_testcase_inputs(info):
    testcase = {}
    parameters = info.get("parameters", [])
    for param in parameters:
        if param.get("in")=="query":
            if param.get("examples"):
                for key, value in param["examples"].items():
                    if key not in testcase:
                        testcase[key] = {}
                    if testcase[key].get("query_params") is None:
                        testcase[key]["query_params"] = {}
                    testcase[key]["query_params"][param["name"]] = value.get("value")
        if param.get("in")=="path":
            if param.get("examples"):
                for key, value in param["examples"].items():
                    if key not in testcase:
                        testcase[key] = {}
                    if testcase[key].get("path_params") is None:
                        testcase[key]["path_params"] = {}
                    testcase[key]["path_params"][param["name"]] = value.get("value")
    requestBody_examples = info.get("requestBody", {}).get("content",{}).get("application/json", {}).get("examples", {})
    for key, value in requestBody_examples.items():
        if key not in testcase:
            testcase[key] = {}
        if testcase[key].get("body") is None:
            testcase[key]["body"] = {}
        testcase[key]["body"] = value
    return testcase

def parse_openapi_paths_by_method(paths, components, path, target_method):
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
        testcase = resolve_testcase_inputs(info)
        info["testcase_inputs"] = testcase
        
    return resolved_path_item

async def get_user_operation_by_path(request, path, method):
    service: OpenApiService = request.app.state.openapi_service
    openapi_json = service.get_current_spec()
    components = openapi_json.get("components", {})

    result = parse_openapi_paths_by_method(openapi_json.get("paths", {}), components, path, method)
    return result



async def get_cur_test_case(request, path, method):
    service: OpenApiService = request.app.state.openapi_service
    openapi_json = service.get_current_spec()
    result = copy.deepcopy(openapi_json.get("paths", {}).get(path, {}).get(method))
    if result:
        result.pop("responses", None)
    
    return result 
async def update_current_spec(request, new_spec, path, method):
    service: OpenApiService = request.app.state.openapi_service
    openapi_json = service.get_current_spec()
    for param in openapi_json["paths"][path][method].get("parameters", []):
        if param.get("in") == "path":
            if param.get("examples"):
                for new_param in new_spec["parameters"]:
                    if new_param.get("in") == "path" and new_param.get("examples"):
                        param["examples"] = new_param["examples"]
        if param.get("in") == "query":
            if param.get("examples"):
                for new_param in new_spec["parameters"]:
                    if new_param.get("in") == "query" and new_param.get("examples"):
                        param["examples"] = new_param["examples"]


    if "requestBody" in openapi_json["paths"][path][method]:
        if openapi_json["paths"][path][method]["requestBody"].get("content", {}).get("application/json", {}).get("examples"):
            new_body_example = new_spec["requestBody"].get("content", {}).get("application/json", {}).get("examples", {})
            openapi_json["paths"][path][method]["requestBody"]["content"]["application/json"]["examples"] = new_body_example
    service.set_current_spec(openapi_json)
    return 
