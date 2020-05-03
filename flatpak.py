from typing import List
import subprocess


def applications() -> List[str]:
    output = subprocess.run(["flatpak", "list", "--columns=application"], capture_output=True, check=True)
    apps = output.stdout.decode("utf-8").split("\n")
    return apps


def run(app: str):
    subprocess.Popen(["flatpak", "run", app])


if __name__ == '__main__':
    print(applications())
