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
