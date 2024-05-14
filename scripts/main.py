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


def ApplyRules(fuzzy_nums: dict, rules: RuleList) -> dict:
    # Rule ruleName = rule01, consequent = Risk=HighR, antecedent = [IncomeLevel=Hig, Assets=Abundant, Amount=Small]

    # This will be the fuzzy Low Risk number that will than have to be defuzzified
    LowR: float = 0.0
    # This will be the fuzzy Medium Risk number that will than have to be defuzzified
    MediumR: float = 0.0
    # This will be the fuzzy High Risk number that will than have to be defuzzified
    HighR: float = 0.0

    for rule in rules:
        # For each rule:
        # I will count up the min() of all antecedent of that rule and update the risk consequent if it is a new max
        if (rule.consequent.split('=')[1] == "LowR"):
            # Since we are doing AND we need to keep track of min. We initialize to 1 since nothing will be ever bigger
            min: float = 1
            for antecedent_var in rule.antecedent:
                attribute = antecedent_var.split('=')[0]
                term = antecedent_var.split('=')[1]
                if (fuzzy_nums[attribute][term] < min):
                    min = fuzzy_nums[attribute][term]
            # Since we are grabbing the max I will only updated it if it is bigger
            if (LowR < min):
                LowR = min
        if (rule.consequent.split('=')[1] == "MediumR"):
            min: float = 1
            for antecedent_var in rule.antecedent:
                attribute = antecedent_var.split('=')[0]
                term = antecedent_var.split('=')[1]
                if (fuzzy_nums[attribute][term] < min):
                    min = fuzzy_nums[attribute][term]
            if (MediumR < min):
                MediumR = min
        if (rule.consequent.split('=')[1] == "HighR"):
            min: float = 1
            for antecedent_var in rule.antecedent:
                attribute = antecedent_var.split('=')[0]
                term = antecedent_var.split('=')[1]
                if (fuzzy_nums[attribute][term] < min):
                    min = fuzzy_nums[attribute][term]
            if (HighR < min):
                HighR = min

    return {"HighR": HighR, "MediumR": MediumR, "LowR": LowR}


def DefuzzyfyRisk(risks: dict, output_var_sets: FuzzySetsDict) -> float:
    x_combined = np.linspace(0, 100, 1000)  # Adjust range if needed
    aggregated = np.zeros_like(x_combined)

    # Interpolate and aggregate membership functions
    for risk_level, fuzzy_value in risks.items():
        fuzzy_set = output_var_sets[f"Risk={risk_level}"]
        interpolated_y = skf.interp_membership(fuzzy_set.x, fuzzy_set.y, x_combined) * fuzzy_value
        aggregated = np.fmax(aggregated, interpolated_y)

    # Calculate the centroid (center of gravity) using skfuzzy
    centroid = skf.defuzz(x_combined, aggregated, 'centroid')
    return centroid

    # Find Centroid
    risk_low = np.fmin(risks["LowR"], output_var_sets["Risk=LowR"].y)
    risk_medium = np.fmin(risks["MediumR"], output_var_sets["Risk=MediumR"].y)
    risk_high = np.fmin(risks["LowR"], output_var_sets["Risk=HighR"].y)

    # Aggregate all three output membership functions together
    aggregated = np.fmax(risk_low, np.fmax(risk_medium, risk_high))

    # Calculate defuzzified result
    final_risk = skf.defuzz(output_var_sets['Risk=HighR'].x, aggregated, 'centroid')
    
    return final_risk


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
            # # Print application
            # app.printApplication()
            
            # Fuzzyfy application   
            fuzzy_nums: dict = FuzzyfyApplication(app, input_var_sets)
            
            # Apply rules
            risks: dict = ApplyRules(fuzzy_nums, rules)
            
            # Defuzzyfy application
            risk_value: float = DefuzzyfyRisk(risks, output_var_sets)
            print(app.appId, risks, "| RISK:", risk_value)

            # Write results to file
            #file.write(f"App ID: {app.appId} | {app.data[0]}{app.data[1]}{app.data[2]}{app.data[3]}{app.data[4]}{app.data[5]} |  Risk Level: {risk_value}\n")


if __name__ == "__main__":
    main()
