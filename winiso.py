import argparse
import os
import shutil
import subprocess

def install_iso(iso_path, usb_path, unattend_path="unattend.xml"):
    if not os.path.isfile(iso_path):
        print(f"Файл ISO {iso_path} не знайдено!")
        return

    if not os.path.isdir(usb_path):
        print(f"Диск {usb_path} не знайдено або він недоступний!")
        return

    print(f"Підготовка USB для {iso_path}...")

    # Змонтувати ISO у Windows
    mount_point = "Z:\\"
    subprocess.run(f"PowerShell Mount-DiskImage -ImagePath '{iso_path}'", shell=True)

    # Копіюємо файли ISO на флешку/диск
    for root, dirs, files in os.walk(mount_point):
        rel_path = os.path.relpath(root, mount_point)
        dest_dir = os.path.join(usb_path, rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            shutil.copy(os.path.join(root, file), dest_dir)

    # Копіюємо unattend.xml
    unattend_dest = os.path.join(usb_path, "sources", "unattend.xml")
    if os.path.isfile(unattend_path):
        shutil.copy(unattend_path, unattend_dest)
        print("unattend.xml скопійовано.")
    else:
        print("unattend.xml не знайдено, установка буде з питаннями.")

    # Відмонтувати ISO
    subprocess.run(f"PowerShell Dismount-DiskImage -ImagePath '{iso_path}'", shell=True)

    print(f"Диск {usb_path} готовий! Завантажся з нього для автоматичної установки.")

    # Пропозиція перезавантаження
    resp = input("Перезавантажити зараз? (y/n): ")
    if resp.lower() == "y":
        subprocess.run("shutdown /r /t 0", shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WinISO installer CLI")
    parser.add_argument("--install", metavar="ISO_PATH", required=True,
                        help="Шлях до Windows ISO")
    parser.add_argument("--load", metavar="DISK_PATH", required=True,
                        help="Диск для запису (USB або інший диск)")
    args = parser.parse_args()

    install_iso(args.install, args.load)
