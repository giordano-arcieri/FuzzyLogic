from MFIS_Classes import *
from MFIS_Read_Functions import *


def FuzzyfyApplication(app: Application, input_var_sets: FuzzySetsDict) -> dict:
    fuzzified_app: dict = dict()
    for item in app.data:
        attribute = item[0]
        value = item[1]
        fuzzy_values = dict()
        for key, sets in input_var_sets.items():
            if (key.split('=')[0] == attribute):
                # Get the index of the x value in the array x
                index = np.where(sets.x == value)[0]
                if len(index) > 0:  # Check if the x value exists in the array x
                    fuzzy_values.update({key.split('=')[1]: sets.y[index[0]]})
            else:
                continue

        fuzzified_app.update({attribute: fuzzy_values})

    return fuzzified_app


def ApplyRules(fuzzy_set: FuzzySet, rules: RuleList) -> str:
    # Rule ruleName = rule01, consequent = Risk=HighR, antecedent = [IncomeLevel=Hig, Assets=Abundant, Amount=Small]
    
    
    for rule in rules:
        print(rule.ruleName, rule.consequent, rule.antecedent)
    
    return "HighR"


def DefuzzyfyRisk(risk: str, output_var_sets: FuzzySetsDict) -> float:
    return 0


def plotFuzzySets(fuzzySetsDict: FuzzySetsDict):

    prev: str = ""

    # var: str, sets: FuzzySet
    for var, sets in fuzzySetsDict.items():
        current_group = var.split('=')[0]
        if prev != "" and current_group != prev:
            # Save and close the figure for the previous group
            plt.title(f'Fuzzy Sets for {prev}')
            plt.legend()
            plt.savefig('Graphs/' + prev + '.png')
            plt.close()

            # Start a new figure for the new group
            plt.figure(figsize=(10, 5))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)

        # Plot current set
        plt.plot(sets.x, sets.y, label=f"{sets.label}")
        prev = current_group

    # Handle the last group after exiting the loop
    if prev != "":
        plt.title(f'Fuzzy Sets for {prev}')
        plt.legend()
        plt.savefig('Graphs/' + prev + '.png')
        plt.close()


def main():
    # Initialize systems and read data
    input_var_sets = readFuzzySetsFile('InputTextFiles/InputVarSets.txt')
    output_var_sets = readFuzzySetsFile('InputTextFiles/Risks.txt')
    rules = readRulesFile()
    applications: list[Application] = readApplicationsFile()

    # Plot all fuzzy graphs
    plotFuzzySets(input_var_sets)
    plotFuzzySets(output_var_sets)

    with open('Results.txt', 'w') as file:
        for app in applications:
            # Print application
            app.printApplication()
            # Fuzzyfy application
            fuzzy_nums: dict = FuzzyfyApplication(app, input_var_sets)
            # Apply rules
            risk: str = ApplyRules(fuzzy_nums, rules)
            return
            # # Defuzzyfy application
            # risk_value: float = DefuzzyfyRisk(risk, output_var_sets)
            # # Write results to file
            # file.write(f"App ID: {app.appId}, Risk Level: {risk_value}\n")


if __name__ == "__main__":
    main()
