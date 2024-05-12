from MFIS_Classes import *
from MFIS_Read_Functions import *


def FuzzyfyApplication(app: Application, input_var_sets: FuzzySetsDict) -> FuzzySet:
    fuzzified_app = FuzzySet()
    fuzzified_app.x = 0
    fuzzified_app.y = 0
    return fuzzified_app


def ApplyRules(fuzzy_set: FuzzySet, rules: RuleList) -> str:
    return "HighR"


def DefuzzyfyRisk(risk: str, output_var_sets: FuzzySetsDict) -> float:
    return 0


def plotFuzzySets(fuzzySetsDict):
    # var: str, sets: list[FuzzySet]
    prev:str = ""
    plt.plot(fuzzySetsDict["Age=Young"].x, fuzzySetsDict["Age=Young"].y, label=f"Ahhh")
    plt.title('Title')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-40, 40)  # Set the y-axis limit
    plt.ylim(0, 1)  # Set the x-axis limit

    plt.grid(True)
    plt.savefig('Graphs/' + prev + '.png')
    
    return
    for var, sets in fuzzySetsDict.items():
        if(prev == ""):
            prev = var.split('=')[0]
        if(var.split('=')[0] == prev):
            plt.plot(sets.x, sets.y, label=f"{sets.label}")
        else:
            plt.title(f'Fuzzy Sets for {prev}')
            plt.figure(figsize=(10, 6))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig('Graphs/' + prev + '.png')
            prev = var.split('=')[0]
            plt.plot(sets.x, sets.y, label=f"{sets.label}")

            

    return 
    # Generating x and y values for the graph
    x_values = np.linspace(xmin, xmax, 1000)
    y_values = np.zeros_like(x_values)
    y_values[(x_values >= a) & (x_values <= b)] = (
        x_values[(x_values >= a) & (x_values <= b)] - a) / (b - a)
    y_values[(x_values > b) & (x_values < c)] = 1
    y_values[(x_values >= c) & (x_values <= d)] = (
        d - x_values[(x_values >= c) & (x_values <= d)]) / (d - c)

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(x_values, y_values, color='red')
    plt.title(title, pad=20)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(-0.01, 1.1)  # Set the y-axis limit
    plt.xlim(xmin, xmax)  # Set the x-axis limit
    plt.grid(True)
    plt.xticks(np.arange(xmin, xmax + 1, (xmax - xmin) / 5))
    plt.yticks(np.arange(0, 1.25, 0.25))
    plt.legend()

    # Show the plot
    plt.savefig('Graphs/' + title + '.png')


def main():
    # Initialize systems and read data
    input_var_sets = readFuzzySetsFile('InputVarSets.txt')
    output_var_sets = readFuzzySetsFile('Risks.txt')
    rules = readRulesFile()
    applications: list[Application] = readApplicationsFile()
    
    plotFuzzySets(input_var_sets)
        
    
    
    return 

    with open('Results.txt', 'w') as file:
        for app in applications:
            # Print application
            app.printApplication()
            # Fuzzyfy application
            fuzzy_set: FuzzySet = FuzzyfyApplication(app, input_var_sets)
            # Apply rules
            risk: str = ApplyRules(fuzzy_set, rules)
            # Defuzzyfy application
            risk_value: float = DefuzzyfyRisk(risk, output_var_sets)
            # Write results to file
            file.write(f"App ID: {app.appId}, Risk Level: {risk_value}\n")


if __name__ == "__main__":
    main()
