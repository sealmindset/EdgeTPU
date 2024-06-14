import os
import subprocess
import sys
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def print_task(message):
    print(Fore.YELLOW + message)

def print_result(message):
    print(Fore.GREEN + message)

def print_error(message):
    print(Fore.RED + message)

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    stderr = process.communicate()[1]
    if stderr:
        print_error(stderr.strip())
    return process.returncode

def main():
    try:
        # Upgrade pycoral
        print_task("Upgrading pycoral...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--extra-index-url", "https://google-coral.github.io/py-repo/", "pycoral"])

        # Run stress-tpu.py
        print_task("Running stress-tpu.py...")
        run_command("python3 stress-tpu.py")
        
        print_result("All tests completed successfully.")
    
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
