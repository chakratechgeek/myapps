import json
import platform
import requests
import winreg
import datetime

def get_installed_software():
    software_list = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    hostname = platform.node()

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

                                # Get installation date — fallback to "now"
                                try:
                                    install_time = winreg.QueryInfoKey(subkey)[2]  # last write time (timestamp)
                                    installed_at = datetime.datetime.fromtimestamp(install_time / 10_000_000 - 11644473600).isoformat()
                                except Exception:
                                    installed_at = datetime.datetime.utcnow().isoformat()

                                software_list.append({
                                    "hostname": hostname,
                                    "software_name": name,
                                    "version": version,
                                    "license_key": "",
                                    "is_valid": True,
                                    "installed_at": installed_at,
                                    "last_used_at": None,            # You can implement this later
                                    "is_active_user": True           # Always True on first collect
                                })
                        except Exception:
                            continue
            except FileNotFoundError:
                continue

    return software_list

def post_software_data():
    url = "http://localhost:8000/software/api/collect/"
    data = get_installed_software()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 201:
        print(f"[✓] Sent {len(data)} software records.")
    else:
        print(f"[✗] Failed to send data: {response.status_code} - {response.text}")

if __name__ == "__main__":
    post_software_data()
