import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# =========================================================
# 1. CREATE INPUT VARIABLES
# =========================================================

def create_input_variables():

    coding = ctrl.Antecedent(
        np.arange(0, 11, 1), "coding"
    )

    mathematics = ctrl.Antecedent(
        np.arange(0, 11, 1), "mathematics"
    )

    logical_thinking = ctrl.Antecedent(
        np.arange(0, 11, 1), "logical_thinking"
    )

    creativity = ctrl.Antecedent(
        np.arange(0, 11, 1), "creativity"
    )

    communication = ctrl.Antecedent(
        np.arange(0, 11, 1), "communication"
    )

    technology_interest = ctrl.Antecedent(
        np.arange(0, 11, 1), "technology_interest"
    )

    variables = [
        coding,
        mathematics,
        logical_thinking,
        creativity,
        communication,
        technology_interest
    ]

    # -----------------------------------------------------
    # Overlapping membership functions
    # -----------------------------------------------------

    for variable in variables:

        variable["low"] = fuzz.trapmf(
            variable.universe,
            [0, 0, 3, 5]
        )

        variable["medium"] = fuzz.trimf(
            variable.universe,
            [3, 5, 7]
        )

        variable["high"] = fuzz.trapmf(
            variable.universe,
            [5, 7, 10, 10]
        )

    return {
        "coding": coding,
        "mathematics": mathematics,
        "logical_thinking": logical_thinking,
        "creativity": creativity,
        "communication": communication,
        "technology_interest": technology_interest
    }


# =========================================================
# 2. CREATE OUTPUT VARIABLE
# =========================================================

def create_output_variable():

    suitability = ctrl.Consequent(
        np.arange(0, 101, 1),
        "suitability"
    )

    suitability["low"] = fuzz.trapmf(
        suitability.universe,
        [0, 0, 25, 50]
    )

    suitability["medium"] = fuzz.trimf(
        suitability.universe,
        [25, 50, 75]
    )

    suitability["high"] = fuzz.trapmf(
        suitability.universe,
        [50, 75, 100, 100]
    )

    return suitability


# =========================================================
# 3. CREATE CAREER-SPECIFIC FUZZY RULES
# =========================================================

def create_rules(career, variables, suitability):

    coding = variables["coding"]
    mathematics = variables["mathematics"]
    logical_thinking = variables["logical_thinking"]
    creativity = variables["creativity"]
    communication = variables["communication"]
    technology_interest = variables["technology_interest"]

    # -----------------------------------------------------
    # SOFTWARE ENGINEERING
    # -----------------------------------------------------

    if career == "Software Engineering":

        rules = [

            ctrl.Rule(
                coding["high"]
                & logical_thinking["high"]
                & technology_interest["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                coding["high"]
                & logical_thinking["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                coding["medium"]
                & logical_thinking["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                coding["medium"]
                & technology_interest["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                coding["low"]
                & logical_thinking["low"],
                suitability["low"]
            ),

            ctrl.Rule(
                coding["low"]
                & technology_interest["low"],
                suitability["low"]
            ),

            # Coverage rules
            ctrl.Rule(
                coding["high"],
                suitability["medium"]
            ),

            ctrl.Rule(
                logical_thinking["high"]
                & technology_interest["medium"],
                suitability["medium"]
            )
        ]

    # -----------------------------------------------------
    # DATA SCIENCE
    # -----------------------------------------------------

    elif career == "Data Science":

        rules = [

            ctrl.Rule(
                mathematics["high"]
                & logical_thinking["high"]
                & technology_interest["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                mathematics["high"]
                & logical_thinking["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                mathematics["medium"]
                & logical_thinking["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                mathematics["medium"]
                & technology_interest["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                mathematics["low"]
                & logical_thinking["low"],
                suitability["low"]
            ),

            ctrl.Rule(
                mathematics["low"]
                & technology_interest["low"],
                suitability["low"]
            ),

            # Coverage rules
            ctrl.Rule(
                mathematics["high"],
                suitability["medium"]
            ),

            ctrl.Rule(
                logical_thinking["high"]
                & technology_interest["medium"],
                suitability["medium"]
            )
        ]

    # -----------------------------------------------------
    # UI/UX DESIGN
    # -----------------------------------------------------

    elif career == "UI/UX Design":

        rules = [

            ctrl.Rule(
                creativity["high"]
                & communication["high"]
                & technology_interest["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                creativity["high"]
                & communication["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                creativity["medium"]
                & communication["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                creativity["medium"]
                & communication["high"],
                suitability["medium"]
            ),

            ctrl.Rule(
                creativity["high"]
                & communication["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                creativity["low"]
                & communication["low"],
                suitability["low"]
            ),

            ctrl.Rule(
                creativity["low"]
                & technology_interest["low"],
                suitability["low"]
            ),

            # Coverage rules
            ctrl.Rule(
                creativity["high"],
                suitability["medium"]
            ),

            ctrl.Rule(
                communication["high"]
                & technology_interest["medium"],
                suitability["medium"]
            )
        ]

    # -----------------------------------------------------
    # DIGITAL MARKETING
    # -----------------------------------------------------

    elif career == "Digital Marketing":

        rules = [

            ctrl.Rule(
                communication["high"]
                & creativity["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                communication["high"]
                & creativity["medium"],
                suitability["high"]
            ),

            ctrl.Rule(
                communication["medium"]
                & creativity["medium"],
                suitability["medium"]
            ),

            ctrl.Rule(
                communication["medium"]
                & creativity["high"],
                suitability["high"]
            ),

            ctrl.Rule(
                communication["high"]
                & creativity["low"],
                suitability["medium"]
            ),

            ctrl.Rule(
                communication["low"]
                & creativity["low"],
                suitability["low"]
            ),

            # Coverage rules
            ctrl.Rule(
                communication["high"],
                suitability["medium"]
            ),

            ctrl.Rule(
                creativity["high"],
                suitability["medium"]
            )
        ]

    else:

        raise ValueError(
            f"Unknown career: {career}"
        )

    return rules


# =========================================================
# 4. CALCULATE ONE CAREER SCORE
# =========================================================

def calculate_career_score(profile, career):

    variables = create_input_variables()

    suitability = create_output_variable()

    rules = create_rules(
        career,
        variables,
        suitability
    )

    control_system = ctrl.ControlSystem(
        rules
    )

    simulation = ctrl.ControlSystemSimulation(
        control_system
    )

    # -----------------------------------------------------
    # CAREER-SPECIFIC INPUTS
    # -----------------------------------------------------

    if career == "Software Engineering":

        simulation.input["coding"] = profile["coding"]

        simulation.input["logical_thinking"] = (
            profile["logical_thinking"]
        )

        simulation.input["technology_interest"] = (
            profile["technology_interest"]
        )

    elif career == "Data Science":

        simulation.input["mathematics"] = (
            profile["mathematics"]
        )

        simulation.input["logical_thinking"] = (
            profile["logical_thinking"]
        )

        simulation.input["technology_interest"] = (
            profile["technology_interest"]
        )

    elif career == "UI/UX Design":

        simulation.input["creativity"] = (
            profile["creativity"]
        )

        simulation.input["communication"] = (
            profile["communication"]
        )

        simulation.input["technology_interest"] = (
            profile["technology_interest"]
        )

    elif career == "Digital Marketing":

        simulation.input["communication"] = (
            profile["communication"]
        )

        simulation.input["creativity"] = (
            profile["creativity"]
        )

    # -----------------------------------------------------
    # FUZZY INFERENCE + DEFUZZIFICATION
    # -----------------------------------------------------

    simulation.compute()

    score = simulation.output["suitability"]

    return round(score, 2)


# =========================================================
# 5. CALCULATE ALL CAREERS
# =========================================================

def calculate_all_careers(profile):

    careers = [
        "Software Engineering",
        "Data Science",
        "UI/UX Design",
        "Digital Marketing"
    ]

    results = {}

    for career in careers:

        results[career] = calculate_career_score(
            profile,
            career
        )

    return results


# =========================================================
# 6. TEST FUZZY SYSTEM
# =========================================================

if __name__ == "__main__":

    test_profile = {

        "coding": 9,
        "mathematics": 8,
        "logical_thinking": 9,
        "creativity": 5,
        "communication": 8,
        "technology_interest": 9
    }

    print()
    print("=" * 55)
    print("AI CAREER ADVISOR - FUZZY LOGIC TEST")
    print("=" * 55)

    results = calculate_all_careers(
        test_profile
    )

    print()

    for career, score in results.items():

        print(
            f"{career}: {score}/100"
        )

    print()
    print("=" * 55)