#!/usr/bin/env python3
import sys
import yaml
import os

CONFIG_PATH = "config/projects.yaml"

def main():
    if len(sys.argv) < 2:
        print("❌ [ERROR] Project name argument missing.")
        sys.exit(1)

    project_name = sys.argv[1]
    print(f"🔍 Validating project: {project_name}")

    if not os.path.exists(CONFIG_PATH):
        print(f"❌ [ERROR] Config file not found: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    if project_name not in config:
        print(f"❌ [ERROR] Project '{project_name}' not found in {CONFIG_PATH}")
        print("📌 Please add the project with proper configuration.")
        sys.exit(1)

    # check secrets
    for env in ["TEST", "STAGING", "PRODUCTION"]:
        secret_name = f"RENDER_{project_name.upper().replace('-', '_')}_{env}_API_KEY"
        if not os.getenv(secret_name):
            print(f"⚠️  [WARNING] Secret {secret_name} is not set in environment.")
            print("   This may cause deployment failure at later stages.")

    print(f"✅ [OK] Project '{project_name}' found in config.")
    sys.exit(0)

if __name__ == "__main__":
    main()
