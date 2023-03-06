
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after misclassifications (false negatives and false positives). We hypothesize that despite provided with all relevant cost information, decision makers may not select a cutoff that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
class C(BaseConstants):
    NAME_IN_URL = 'Instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Confusion_Matrix_missing_value = models.StringField(
        choices=[['True Positive (TP)', 'True Positive (TP)'], ['True Negative (TN)', 'True Negative (TN)'],
                 ['False Positive (FP)', 'False Positive (FP)'], ['False Negative (FN)', 'False Negative (FN)']],
        label='<b> What outcome is missing (?) in the matrix above? </b>')
    Accuracy_Understanding_Check = models.StringField(
        choices=[['0', '0'], ['0.2', '0.2'], ['0.4', '0.4'], ['0.6', '0.6'], ['0.8', '0.8'], ['1', '1']],
        label='<b> Based on the confusion matrix shown above, what is the classification accuracy of the algorithm? </b>')
    Misclassification_Costs_Understanding_Check = models.IntegerField(
        label='<b> Based on the confusion matrix shown above, what are the overall misclassification costs [$]? </b>')
    Threshold_Introduction_Understanding_Check = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']],
        label='<b> Do you agree with the following statement? "In order to reduce False Negative (FN) classifications, the threshold D should be increased." </b>')
    understand_instr = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']],
        label='Did you understand the instructions and how your payoff gets calculated?')
    num_failed_attempts = models.IntegerField(initial = 0, blank = True)

class Welcome(Page):
    pass
class ScenarioDescription(Page):
    pass
class ThresholdIntroduction(Page):
    pass
class MisclassificationCosts(Page):
    pass
class PayoffExplanation(Page):
    pass
class PayoffCalculation(Page):
    form_model = 'player'
    form_fields = ['understand_instr']
    @staticmethod
    def error_message(player:Player, values):
        solutions = dict(understand_instr=True)
        if values != solutions:
            return "Are you sure? You cannot participate in the experiment if you answer again that you did not understand the instructions. Please review your answer."
class UnderstandingChecks(Page):
    form_model = 'player'
    form_fields = ['Confusion_Matrix_missing_value', 'Accuracy_Understanding_Check', 'Misclassification_Costs_Understanding_Check', 'Threshold_Introduction_Understanding_Check', 'num_failed_attempts']
    @staticmethod
    def is_displayed(player: Player):
        return player.understand_instr != False

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            Confusion_Matrix_missing_value='False Positive (FP)',
            Accuracy_Understanding_Check='0.8',
            Misclassification_Costs_Understanding_Check=20,
            Threshold_Introduction_Understanding_Check=False)

        #if values != solutions:
            #player.num_failed_attempts += 1
        if values != solutions:
            return "One or more answers were incorrect. Please try again."

class CorrectAnswers(Page):
    pass

page_sequence = [Welcome, ScenarioDescription, ThresholdIntroduction, MisclassificationCosts, PayoffExplanation, PayoffCalculation, UnderstandingChecks, CorrectAnswers]