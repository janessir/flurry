import subprocess

def run_python_webserver_file(input_str, sudo_password=None):
    try:
        # Run the Python file with input string
        process = subprocess.Popen(['python3', 'webserver.py'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
        
        # Feed input string
        output, error = process.communicate(input=input_str, timeout=50)

        # Check if sudo password is required
        if "[sudo] password" in output.lower() and sudo_password:
            process.stdin.write(sudo_password + '\n')
            output, error = process.communicate(timeout=30)

        return output, error

    except Exception as e:
        return None, str(e)

def read_input_file(input_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()[1:]  # Exclude the first line
        return lines
    except FileNotFoundError:
        return []

def main():
    scenarios_file = str(input("Enter your input scenario text file path: "))  # Path to your input scenario text file (benign_scenario.txt or malicious_scenario.txt)
    unsuccessful_runs = []

    lines = read_input_file(scenarios_file)
    if not lines:
        print("Input file is empty or not found.")
        return

    sudo_password = input("Enter sudo password if needed (leave empty if not required): ")

    for line in lines:
        line = line.strip()
        print(f"Running scenario: {line}")
        output, error = run_python_webserver_file(line, sudo_password)
        if error:
            unsuccessful_runs.append((line, error))

    if unsuccessful_runs:
        print("Unsuccessful runs:")
        for run in unsuccessful_runs:
            print(f"Input: {run[0]}\nError: {run[1]}")
    else:
        print("All runs were successful.")

if __name__ == "__main__":
    main()
