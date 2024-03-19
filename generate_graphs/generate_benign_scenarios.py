from helper_functions import generate_combinations

# Benign scenarios
benign_actions = ['message', 'submit', 'query', 'ping', 'databaseentry', 'login']
benign_scenarios = generate_combinations(benign_actions)

# Write to benign_scenarios.txt file
output_file = './generate_graphs/scenarios/benign_scenarios.txt'
with open(output_file, 'w') as file:
    file.write(f"{len(benign_scenarios)} possible combinations of actions:")
    for scenario in benign_scenarios:
        file.write('\n' + scenario)

print("File has been generated successfully.")