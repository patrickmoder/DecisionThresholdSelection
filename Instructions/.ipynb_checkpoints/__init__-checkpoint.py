
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
    Confusion_Matrix_missing_value = models.StringField(choices=[['True Positive (TP)', 'True Positive (TP)'], ['True Negative (TN)', 'True Negative (TN)'], ['False Positive (FP)', 'False Positive (FP)'], ['False Negative (FN)', 'False Negative (FN)']], label='What outcome is missing (?) in the matrix below? Please click "Next" to confirm your answer.')
    Threshold_Introduction_Understanding_Check = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Do you agree with the following statement? In order to reduce False Negative (FN) classifications, the threshold θ should be increased. Please click "Next" to confirm your answer.')
    Misclassification_Costs_Understanding_Check = models.IntegerField(label='Based on the exemplary costs for misclassifications introduced above, how much would four (4) False Positive Predictions cost? Please click "Next" to confirm your answer.')
    understand_instr = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Did you understand the instructions and how your payoff gets calculated?')
class Player(BasePlayer):
    pass
class Welcome(Page):
    form_model = 'player'
class ScenarioDescription(Page):
    form_model = 'group'
    form_fields = ['Confusion_Matrix_missing_value']
class IncorrectAnswerConfusionMatrix(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return group.Confusion_Matrix_missing_value != "False Positive (FP)"
class ThresholdIntroduction(Page):
    form_model = 'group'
    form_fields = ['Threshold_Introduction_Understanding_Check']
class IncorrectAnswerThresholdIntroduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return group.Threshold_Introduction_Understanding_Check != "No"
class MisclassificationCosts(Page):
    form_model = 'group'
    form_fields = ['Misclassification_Costs_Understanding_Check']
class IncorrectAnswerMisclassificationCosts(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return group.Misclassification_Costs_Understanding_Check != "20"
class PayoffExplanation(Page):
    form_model = 'player'
    form_fields = ['understand_instr']
page_sequence = [Welcome, ScenarioDescription, IncorrectAnswerConfusionMatrix, ThresholdIntroduction, IncorrectAnswerThresholdIntroduction, MisclassificationCosts, IncorrectAnswerMisclassificationCosts, PayoffExplanation]