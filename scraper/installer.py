import sys


def create_launch_bat():
    python_exe = sys.executable

    if not python_exe:
        raise SystemError("Python executable does not exist. Please make sure Python is installed.")

    with open("scraper.bat", "w") as bat:
        bat.write("@echo off\n{} metacritic_scraper.py\npause".format(python_exe))
        bat.close()


def main():
    try:
        create_launch_bat()
    except Exception as e:
        print(e, sys.exc_info()[0])
        sys.exit(-1)


if __name__ == "__main__":
    main()



