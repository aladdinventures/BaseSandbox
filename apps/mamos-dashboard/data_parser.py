import os
import re
import json
import yaml

def parse_summary_report(summary_path):
    data = {"overall_status": "unknown", "projects": {}}
    if not os.path.exists(summary_path):
        return data

    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Overall status
    overall_match = re.search(r'## وضعیت کلی CI/CD: (.+)', content)
    if overall_match:
        data["overall_status"] = overall_match.group(1).strip()

    # Project statuses
    project_matches = re.findall(r'\*\*پروژه (.+?):\*\* وضعیت: (.+?), بیلد: (.+?), تست: (.+?), استقرار: (.+?)', content)
    for match in project_matches:
        project_name = match[0].strip()
        data["projects"][project_name] = {
            "status": match[1].strip(),
            "build_status": match[2].strip(),
            "test_status": match[3].strip(),
            "deploy_status": match[4].strip()
        }
    return data

def parse_detail_report(detail_path):
    data = {"build_log": "", "test_log": "", "deploy_log": "", "duration": "unknown"}
    if not os.path.exists(detail_path):
        return data

    with open(detail_path, 'r', encoding='utf-8') as f:
        content = f.read()

    build_log_match = re.search(r'### لاگ بیلد\n```\n(.+?)\n```', content, re.DOTALL)
    if build_log_match:
        data["build_log"] = build_log_match.group(1).strip()

    test_log_match = re.search(r'### لاگ تست\n```\n(.+?)\n```', content, re.DOTALL)
    if test_log_match:
        data["test_log"] = test_log_match.group(1).strip()

    deploy_log_match = re.search(r'### لاگ استقرار\n```\n(.+?)\n```', content, re.DOTALL)
    if deploy_log_match:
        data["deploy_log"] = deploy_log_match.group(1).strip()

    duration_match = re.search(r'\*\*مدت زمان اجرا:\*\* (.+)', content)
    if duration_match:
        data["duration"] = duration_match.group(1).strip()

    return data

def get_project_names(projects_yaml_path):
    project_names = []
    if not os.path.exists(projects_yaml_path):
        return project_names
    with open(projects_yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    if 'projects' in config:
        for project in config['projects']:
            project_names.append(project['name'])
    return project_names

def collect_all_data(base_path):
    reports_dir = os.path.join(base_path, 'reports')
    projects_yaml_path = os.path.join(base_path, 'config', 'projects.yaml')

    all_data = {"timestamp": os.path.getmtime(reports_dir) if os.path.exists(reports_dir) else 0}

    summary_data = parse_summary_report(os.path.join(reports_dir, 'summary.md'))
    all_data.update(summary_data)

    project_names = get_project_names(projects_yaml_path)
    for project_name in project_names:
        detail_report_path = os.path.join(reports_dir, 'details', f'{project_name}_report.md')
        detail_data = parse_detail_report(detail_report_path)
        if project_name in all_data["projects"]:
            all_data["projects"][project_name].update(detail_data)
        else:
            all_data["projects"][project_name] = detail_data

    return all_data

if __name__ == '__main__':
    # Assuming the script is run from aladdin-sandbox/apps/mamos-dashboard
    # and reports are in aladdin-sandbox/reports
    base_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    collected_data = collect_all_data(base_repo_path)
    
    output_dir = os.path.join(base_repo_path, 'apps', 'mamos-dashboard', 'data')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'dashboard_data.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=4)
    print(f"Data successfully collected and saved to {output_file}")

