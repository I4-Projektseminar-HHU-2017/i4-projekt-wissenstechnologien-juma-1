import sys
import subprocess
import os


def create_launch_bat():
    print("Checking requirements...")

    requirements_fulfilled = True
    python_exe = sys.executable

    if not python_exe:
        raise SystemError("Python executable does not exist. Please make sure Python (at least 3.5) is installed.")

    run_subprocess(['pip', '-m', 'install', '-U', 'pip'])

    try:
        __import__("bs4")
    except ImportError:
        if run_subprocess(['pip', 'install', 'beautifulsoup4']):
            print("\n")
        else:
            print("Could not install beautifulsoup4.")
            requirements_fulfilled = False

    try:
        __import__("html5lib")
    except ImportError:
        if run_subprocess(['pip', 'install', 'html5lib']):
            print("\n")
        else:
            print("Could not install html5lib.")
            requirements_fulfilled = False

    try:
        __import__("request")
    except ImportError:
        if run_subprocess(['pip', 'install', 'request']):
            print("\n")
        else:
            print("Could not install request.")
            requirements_fulfilled = False

    try:
        __import__("argparse")
    except ImportError:
        if run_subprocess(['pip', 'install', 'argparse']):
            print("\n")
        else:
            print("Could not install argparse.")
            requirements_fulfilled = False

    if requirements_fulfilled:
        print("Python requirements OK!")
        with open("scraper.bat", "w") as bat:
            bat.write("@echo off\n{} metacritic_scraper.py\npause".format(python_exe))
            bat.close()


def run_subprocess(code):
    try:
        process = subprocess.Popen(' '.join(code), stderr=open(os.devnull), stdout=None)
        while process:
            if process.poll() is not None:
                return True
            else:
                continue
    except Exception:
        return False


def create_textfiles():
    print("Creating output files...")
    textfile_names = [str(i) + "_reviews.txt" for i in range(0, 11)]
    for name in textfile_names:
        open("./output/"+name, 'w').close()
    print("Done.")


def main():
    try:
        create_launch_bat()
        create_textfiles()
        print("\nUse 'scraper.bat' to begin scraping.")
    except Exception as e:
        print(e, sys.exc_info()[0])
        sys.exit(-1)


if __name__ == "__main__":
    main()
