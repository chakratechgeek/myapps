import json
import platform
import requests
import winreg

def get_installed_software():
    software_list = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for hive in (winreg.HKEY_LOCAL_MACHINE,):
        for path in registry_paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                try:
                                    version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                except FileNotFoundError:
                                    version = ""
                                software_list.append({
                                    "hostname": platform.node(),
                                    "software_name": name,
                                    "version": version,
                                    "license_key": "",
                                    "is_valid": True
                                })
                        except FileNotFoundError:
                            continue
            except FileNotFoundError:
                continue

    return software_list

def post_software_data():
    url = "http://localhost:8000/software/api/collect/"
    software_list = get_installed_software()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(software_list), headers=headers)

    if response.status_code == 201:
        print(f"[✓] Successfully sent {len(software_list)} software records.")
    else:
        print(f"[✗] Failed. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    post_software_data()
