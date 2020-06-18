from typing import List
import subprocess
import logging


def applications() -> List[str]:
    output = subprocess.run(["flatpak", "list", "--columns=application"], capture_output=True, check=True)
    apps = output.stdout.decode("utf-8").split("\n")
    logging.info("Available applications")
    for app in apps:
        logging.info(app)
    return apps


def run(app: str):
    logging.info("Run " + app)
    subprocess.Popen(["flatpak", "run", app])


if __name__ == '__main__':
    print(applications())
