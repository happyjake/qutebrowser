import subprocess
import sys


def make_dmg():
    subprocess.run(
        ["pyinstaller", "--noconfirm", "misc/qutebrowser.spec"],
        check=True,
    )
    scripts = ""
    with open("./scripts/dev/Makefile-dmg", "r") as src_file:
        scripts = src_file.read()
    scripts = scripts.replace("TEMPLATE_SIZE ?= 500m", "TEMPLATE_SIZE ?= 1200m")
    with open("./build/Makefile-dmg", "w") as dict_file:
        dict_file.write(scripts)
    subprocess.run(["make", "-f", "./build/Makefile-dmg"], check=True)


def main():
    make_dmg()


if __name__ == "__main__":
    main()
