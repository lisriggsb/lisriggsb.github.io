import random

BOX_A_AMOUNT = 100
BOX_B_AMOUNT = 1000000

def main():
    print_intro()

    keep_playing = True

    while keep_playing:
        accuracy = get_predictor_accuracy()

        print()
        print("Choose a mode:")
        print("1. Play once")
        print("2. Simulate many rounds and compare strategies")

        mode = get_choice("Enter 1 or 2: ")

        if mode == "1":
            play_once(accuracy)
        else:
            run_simulation(accuracy)
        
        ask_boxer_identity()
        
        print()
        
        keep_playing = ask_yes_or_no("Would you like to play again? Enter y or n: ")
        
        print()
        print("Thanks for playing the Newcomb Problem Simulator!")


def pause():
    # I'm wordy, so this lets the user move through the intro and explanations at their own pace:
    input("Press Enter to continue...")

def print_intro():
    print("Welcome to the Newcomb Problem Simulator!")
    print()
    pause()

    print()
    print("There are two boxes:")
    print("Box A is transparent and contains $100.")
    print("Box B is opaque and contains either $1,000,000 or $0.")
    print()
    pause()

    print()
    print("You can choose to take only Box B, or you can take both boxes.")
    print()
    pause()

    print()
    print("But there is a catch!")
    print("A predictor has already predicted what you will do before you do it.")
    print()
    pause()

    print()
    print("If the predictor predicted that you would take only Box B,")
    print("then they have put $1,000,000 in Box B.")
    print()
    pause()

    print()
    print("But if the predictor predicted that you would take both boxes,")
    print("then they have put $0 in Box B.")
    print()
    pause()


def get_choice(prompt):
    # Keeps asking the user for input until they enter 1 or 2.
    choice = input(prompt)

    while choice != "1" and choice != "2":
        print("Sorry, please enter 1 or 2: ")
        choice = input(prompt)

    return choice


def ask_yes_or_no(prompt):
    # This keeps asking the user for input until they enter y or n; returns True for y and False for n.
    answer = input(prompt)

    while answer != "y" and answer != "n":
        print("Sorry, please enter y or n: ")
        answer = input(prompt)

    if answer == "y":
        return True
    else:
        return False


def get_predictor_accuracy():
    # This asks the player for the predictor's accuracy and returns that accuracy as a decimal:
    print()
    print("In the original Newcomb Problem, we are supposed to imagine")
    print("that the predictor has never been wrong before...")
    print("...and that's why it's very tricky!")
    print()
    pause()

    print()
    print("But, in this simulator, you get to choose how accurate the predictor is.")
    print()
    pause()
    print()

    accuracy_percent = float(input("How accurate is the predictor? Enter a number between 0 and 100: "))

    while accuracy_percent < 0 or accuracy_percent > 100:
        print("Sorry, please enter a number between 0 and 100.")
        accuracy_percent = float(input("How accurate is the predictor? Enter a number between 0 and 100: "))

    accuracy = accuracy_percent / 100
    return accuracy


def play_once(accuracy):
    # The user play the Newcomb Problem one time:

    print()
    print("Choose wisely! Which path will you take?")
    print("1. One-box: take only Box B")
    print("2. Two-box: take both Box A and Box B")

    choice = get_choice("Enter 1 or 2: ")

    if choice == "1":
        strategy = "one_box"
    else:
        strategy = "two_box"

    payout, predicted_strategy, box_b = play_newcomb(strategy, accuracy)

    print()
    print("You chose: " + format_strategy(strategy))
    print("You won: $" + str(payout) + " !")

    print()
    wants_explanation = ask_yes_or_no("Would you like an explanation of this outcome? Enter y or n: ")

    if wants_explanation:
        explain_one_round(strategy, predicted_strategy, box_b, payout)

    print()
    wants_theory = ask_yes_or_no("Would you like a decision-theory explanation? Enter y or n: ")

    if wants_theory:
        explain_decision_theory()


def play_newcomb(strategy, accuracy):

    # This runs one simulation of the Newcomb Problem.
    """
    strategy is either "one_box" or "two_box".
    accuracy is the predictor's accuracy as a decimal.

    returns:
    - payout
    - predicted_strategy
    - box_b
    """

    random_number = random.random()

    if random_number < accuracy:
        predictor_is_right = True
    else:
        predictor_is_right = False

    if predictor_is_right:
        predicted_strategy = strategy
    else:
        if strategy == "one_box":
            predicted_strategy = "two_box"
        else:
            predicted_strategy = "one_box"

    if predicted_strategy == "one_box":
        box_b = BOX_B_AMOUNT
    else:
        box_b = 0

    if strategy == "one_box":
        payout = box_b
    else:
        payout = BOX_A_AMOUNT + box_b

    return payout, predicted_strategy, box_b


def explain_one_round(strategy, predicted_strategy, box_b, payout):
    # This explains why the user got the payout they got (if they choose to learn why):
    
    print()
    print("Explanation:")
    print("The predictor predicted that you would choose: " + format_strategy(predicted_strategy))

    if predicted_strategy == "one_box":
        print("Because the predictor predicted that you'd take one box, Box B contained $1,000,000.")
    else:
        print("Because the predictor predicted that you'd take both boxes, Box B contained $0.")

    if strategy == "one_box":
        print("You took only Box B, so your payout was exactly what was in Box B.")
    else:
        print("You took both boxes, so your payout was Box A plus Box B.")
        print("Box A contained $" + str(BOX_A_AMOUNT) + ".")

    print("So, your total payout was $" + str(payout) + ".")


def run_simulation(accuracy):
    #Compares one-boxing and two-boxing over many rounds!
    print()
    num_rounds = int(input("How many rounds would you like to simulate? "))

    while num_rounds <= 0:
        print("Sorry, please enter a number greater than 0.")
        num_rounds = int(input("How many rounds would you like to simulate? "))

    one_box_total = 0
    two_box_total = 0

    for i in range(num_rounds):
        one_box_payout, one_box_prediction, one_box_box_b = play_newcomb("one_box", accuracy)
        two_box_payout, two_box_prediction, two_box_box_b = play_newcomb("two_box", accuracy)

        one_box_total = one_box_total + one_box_payout
        two_box_total = two_box_total + two_box_payout

    one_box_average = one_box_total / num_rounds
    two_box_average = two_box_total / num_rounds

    print()
    print("After " + str(num_rounds) + " rounds:")
    print("One-boxing average payout: $" + str(round(one_box_average, 2)))
    print("Two-boxing average payout: $" + str(round(two_box_average, 2)))

    print()
    if one_box_average > two_box_average:
        print("In this simulation, one-boxing did better.")
    elif two_box_average > one_box_average:
        print("In this simulation, two-boxing did better.")
    else:
        print("In this simulation, both strategies tied!")

    print()
    wants_explanation = ask_yes_or_no("Would you like an explanation of the simulation? Enter 'y' or 'n': ")

    if wants_explanation:
        explain_simulation(accuracy, one_box_average, two_box_average, num_rounds)

    print()
    wants_theory = ask_yes_or_no("Would you like a decision-theory explanation? Enter 'y' or 'n': ")

    if wants_theory:
        explain_decision_theory()


def explain_simulation(accuracy, one_box_average, two_box_average, num_rounds):
    # This explains why the simulation results came out the way they did; doesn't discuss decision theory
   
    print()
    print("Simulation Explanation:")
    print("In each simulated round, the predictor was right about " + str(round(accuracy * 100, 2)) + "% of the time.")
    print()
    pause()

    print("When the strategy was one-boxing:")
    print("- If the predictor correctly predicted one-boxing, Box B had $1,000,000.")
    print("- If the predictor incorrectly predicted two-boxing, Box B had $0.")
    print()
    pause()

    print("When the strategy was two-boxing:")
    print("- If the predictor correctly predicted two-boxing, Box B had $0.")
    print("- If the predictor incorrectly predicted one-boxing, Box B had $1,000,000.")
    print("- The two-boxer also gets Box A, which contains $" + str(BOX_A_AMOUNT) + ".")
    print()
    pause()

    difference = abs(one_box_average - two_box_average)

    if difference < 10000:
        print("The two averages were pretty close in this run.")
        print("This can happen because simulations involve randomness, especially with a small number of rounds.")
        print("You simulated " + str(num_rounds) + " rounds.")
        print("If you run many more rounds, the averages usually settle into a clearer pattern!")
    elif one_box_average > two_box_average:
        print("In this run, one-boxing had the higher average payout.")
        print("This happened because one-boxing was more often paired with Box B containing $1,000,000.")
        print("That is more likely when the predictor is very accurate!")
    else:
        print("In this run, two-boxing had the higher average payout.")
        print("This can happen if the predictor accuracy is low.")
        print("It can also happen because of randomness if the number of simulated rounds is small.")
        print("In those cases, two-boxing may more often get the extra Box A money,")
        print("or may sometimes get both Box A and a full Box B.")

    print()
    print("One-boxing average: $" + str(round(one_box_average, 2)))
    print("Two-boxing average: $" + str(round(two_box_average, 2)))


def explain_decision_theory():
    # This gives an interactive explanation of Evidential Decision Theory and Causal Decision Theory.
   
    print()
    print("Decision Theory Explanation:")
    print()
    print("Newcomb's Problem is hard, and it's famous because it shows us how two")
    print("reasonable ways of thinking about rational choice can prescribe")
    print("different actions.")
    print()
    pause()

    print()
    print("In one camp is Evidential Decision Theory, which asks something like:")
    print("\"What would my choice be evidence of?\"")
    print()
    pause()

    print()
    print("In Newcomb's Problem, if the predictor is highly accurate,")
    print("then choosing only Box B is strong evidence that the predictor")
    print("already predicted one-boxing.")
    print()
    pause()

    print()
    print("And if the predictor did predict one-boxing, Box B contains $1,000,000.")
    print()
    print("So, from an evidential point of view, one-boxing looks like the way to go!")
    print()
    pause()

    print()
    print("This is why one-boxing usually does better in the simulator")
    print("when the predictor is highly accurate:")
    print()
    print("One-boxing is connected to a prediction that was probably already favorable.")
    print()
    pause()

    print()
    print("On the other hand, Causal Decision Theory asks something like this:")
    print()
    print("\"What can my imminent choice actually cause?\"")
    print()
    pause()

    print()
    print("Recall that in Newcomb's Problem, the prediction has already been made.")
    print("The money has already, as a matter of fact, either been placed in") 
    print("Box B, or left out of Box B.")
    print()
    print("So, the causal decision theorist says,")
    print("\"my choice now cannot actually *cause* Box B to be full or empty.\"")
    print()
    pause()

    print()
    print("As a quick last exercise, let's test the causal argument:")
    print()

    print("Quick question:")
    print("If Box B is already full, which strategy gets more money?")
    print("1. One-boxing")
    print("2. Two-boxing")

    answer = get_choice("Enter 1 or 2: ")

    if answer == "2":
        print("Correct! If Box B is already full, two-boxing gets the $1,000,000 + Box A.")
    else:
        print("Not quite! If Box B is already full, one-boxing gets the $1,000,000,")
        print("but two-boxing gets the $1,000,000 + Box A.")

    print()
    pause()

    print()
    print("Another quick question:")
    print("If Box B is already empty, which strategy gets more money?")
    print("1. One-boxing")
    print("2. Two-boxing")

    answer = get_choice("Enter 1 or 2: ")

    if answer == "2":
        print("Correct! If Box B is already empty, two-boxing still gets Box A.")
    else:
        print("Not quite! If Box B is already empty, the one-boxer gets $0,")
        print("but the two-boxer gets Box A, too.")

    print()
    pause()

    print()
    print("And that is the causal decision theorist's main argument:")
    print()
    print("Once the boxes are already set, taking both boxes gets you")
    print("everything one-boxing gets, plus Box A. :)")
    print()
    print("The expected utility of 2-boxing is higher in both possible states")
    print("of Box B, which we can especially see when we think about the money")
    print("already being there or not.")
    print()
    pause()

    print()
    print("So... does this simulator show that Evidential Decision Theory is better?!")
    print()
    pause()
    print()
    print("In one sense, yes, because if the predictor is highly accurate,")
    print("one-boxing usually gets more money, as stipulated by the case.")
    print()
    pause()

    print()
    print("But, the causal decision theorist thinks, this doesn't settle everything!")
    print("They might think that one-boxers tend to be in better pre-set situations.")
    print()
    pause()

    print()
    print("The highly accurate predictor saw them as one-boxers and filled Box B.")
    print("But once I am choosing, that setup has already happened (or not).")
    print()
    print("So, it's ultimately my pre-set circumstances that come to bite me; not my choice.")
    print()
    pause()

    print()
    print("So, EDT tells us to:")
    print("\"choose the action that is the best evidence of your situation.\"")
    print()
    print("But CDT says:")
    print("\"choose the action that best improves your situation causally.\"")
    print()
    pause()

    print()
    print("Again, Newcomb's Problem is famous because these two theories come apart!")
    print()
    print("EDT seems to give the money-winning recommendation.")
    print("And CDT seems to better respect the fact that the prediction")
    print("and box-filling (or not-filling) have already happened.")
    print()

def ask_boxer_identity():
    # This asks the player whether they are a one-boxer or two-boxer after playing, so I can joke with them.
    print()
    print("After playing this round, are you a one-boxer or a two-boxer?")
    print("1. One-boxer")
    print("2. Two-boxer")

    answer = get_choice("Enter 1 or 2: ")

    if answer == "1":
        print("\"Why ain't you richer?\" - Jim Joyce")
    else:
        print("\"Yay!\" - Jim Joyce somewhere, probably")

def format_strategy(strategy):
    # This makes strategy names look nicer when printed :)

    if strategy == "one_box":
        return "one-box"
    else:
        return "two-box"


if __name__ == '__main__':
    main()