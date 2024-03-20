import subprocess
import sys
sys.path.append('/home/teehee2/flurry/flurry')
from util.driversetup import DRIVER

def run_python_webserver_file(input_str, sudo_password=None):
    try:
        # Run the Python file with input string
        process = subprocess.Popen(['python3', 'webserver.py'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
        
        # Feed input string
        output, error = process.communicate(input=input_str, timeout=100)

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
    try:
        scenarios_file = str(input("Enter your input scenarios (.txt file) path: "))  # Path to your input scenario text file (benign_scenario.txt or malicious_scenario.txt)
        unsuccessful_runs = []
        successful_runs = []

        # Save output and specifically, the unsuccessful runs in a .txt file
        output_file = 'generate_graphs/webserver_output/' + str(input("Enter a tag (no whitespaces) for this test run: ")) + '.txt'
        lines = read_input_file(scenarios_file)
        if not lines:
            print("Input file is empty or not found.")
            return

        sudo_password = input("Enter sudo password if needed (leave empty if not required): ")

        for line in lines:
            line = line.strip()
            print(f"Running scenario: {line}")
            output, error = run_python_webserver_file(line, sudo_password)
            # Write output of webserver.py run into a .txt file for debugging
            with open(output_file, 'a') as f:
                f.write(f"Input: {line}\nOutput:\n{output}\n\n")
            if error:
                unsuccessful_runs.append((line, error))
            else:
                successful_runs.append(line)

        if successful_runs:
            # Write to output file
            with open(output_file, 'a') as f:
                f.write(f"\n\n------------------------------------------------------\nSuccessful runs:")
            
            for run in successful_runs:
                with open(output_file, 'a') as f:
                    f.write(f"{run}\n")
            

        if unsuccessful_runs:
            # Print unsuccessful run output
            print("\n\nUnsuccessful runs:\n")

            # Also write unsuccessful run to output file
            with open(output_file, 'a') as f:
                f.write(f"\n\n------------------------------------------------------\nUnsuccessful runs:")
            
            for run in unsuccessful_runs:
                if 'timed out' not in run[1]: # ignoring time out errors
                    print(f"Input: {run[0]}\nError: {run[1]}")

                    with open(output_file, 'a') as f:
                        f.write(f"{run[0]}\n")
        else:
            print("All runs were successful.")
            
            with open(output_file, 'a') as f:
                f.write(f"\n\n>>> All runs were successful\n")
        
        print("Output of running webserver.py can be found in: ", output_file)

    except Exception as e:
        with open(output_file, 'a') as f:
            f.write(f"\n\n------------------------------------------------------\nAn error occured: ", e)
            f.write(f"Possibly stopped at: {line}\n")

        if successful_runs:
            # Write to output file
            with open(output_file, 'a') as f:
                f.write(f"\n\n------------------------------------------------------\nSuccessful runs:")
        
            for run in successful_runs:
                with open(output_file, 'a') as f:
                        f.write(f"{run}\n")
                
        if unsuccessful_runs:

            # Also write unsuccessful run (so far) to output file
            with open(output_file, 'a') as f:
                f.write(f"\n\n------------------------------------------------------\nUnsuccessful runs (up to point of execution):")
            
            for run in unsuccessful_runs:
                if 'timed out' not in run[1]: # ignoring time out errors
                    with open(output_file, 'a') as f:
                        f.write(f"{run[0]}\n")
        else:
            with open(output_file, 'a') as f:
                f.write(f"\n\n>>> All runs were successful\n")
            
            print("Output of running webserver.py can be found in: ", output_file)

if __name__ == "__main__":
    main()
