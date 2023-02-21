
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
    
#    def Confusion_Matrix_missing_value_error_message(group, value):
#        if value!='False Positive (FP)':
#            return 'Your answer was incorrect. Please try again.'
#        
#    def Threshold_Introduction_Understanding_Check_error_message(group, value):
#        if value!=False:
#            return 'Your answer was incorrect. Please try again.'
#            
#    def Misclassification_Costs_Understanding_Check_error_message(group, value):
#        if value!=20:
#            return 'Your answer was incorrect. Please try again.'
#        
#    def understand_instr_error_message(group, value):
#        if value!=True:
#            return 'Are you sure that you did not understand the instructions and payoff calculation? In this case you can not participate in the experiment. Please submit your answer again.'
    
class Player(BasePlayer):
    Confusion_Matrix_missing_value = models.StringField(
        choices=[['True Positive (TP)', 'True Positive (TP)'], ['True Negative (TN)', 'True Negative (TN)'],
                 ['False Positive (FP)', 'False Positive (FP)'], ['False Negative (FN)', 'False Negative (FN)']],
        label='Please answer the following question before you can move to the next page. <b> What outcome is missing (?) in the matrix above? </b> <br /> <br /> Please click "Next" to confirm your answer.')
    Threshold_Introduction_Understanding_Check = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']],
                                                                     label='Please answer the following question before you can move to the next page. <b> Do you agree with the following statement? "In order to reduce False Negative (FN) classifications, the threshold θ should be increased." </b> <br /> <br /> Please click "Next" to confirm your answer.')
    Misclassification_Costs_Understanding_Check = models.IntegerField(
        label='Please answer the following question before you can move to the next page. <b> Based on the exemplary costs for misclassifications introduced above, how much would four (4) False Positive Predictions cost? </b> <br /> <br /> Please click "Next" to confirm your answer.')
    understand_instr = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']],
                                           label='Did you understand the instructions and how your payoff gets calculated?')
class Welcome(Page):
    pass
class ScenarioDescription(Page):
    pass
class ThresholdIntroduction(Page):
    pass
   # @staticmethod
   # def is_displayed(player: Player):
   #     group = player.group
   #     return group.Confusion_Matrix_missing_value = "False Positive (FP)"
class MisclassificationCosts(Page):
    pass
    #@staticmethod
    #def is_displayed(player: Player):
    #    group = player.group
    #    return group.Threshold_Introduction_Understanding_Check = False
class PayoffExplanation(Page):
    pass
class PayoffCalculation(Page):
    form_model = 'player'
    form_fields = ['understand_instr']
class UnderstandingChecks(Page):
    form_model = 'player'
    form_fields = ['Confusion_Matrix_missing_value', 'Threshold_Introduction_Understanding_Check', 'Misclassification_Costs_Understanding_Check']
    @staticmethod
    def is_displayed(player: Player):
        return player.understand_instr != False

    #@staticmethod
    #def is_displayed(player: Player):
    #    group = player.group
    #    return group.Confusion_Matrix_missing_value != "False Positive (FP)"
    #    return group.Threshold_Introduction_Understanding_Check != False
    #    return group.Misclassification_Costs_Understanding_Check != 20

page_sequence = [Welcome, ScenarioDescription, ThresholdIntroduction, MisclassificationCosts, PayoffExplanation, PayoffCalculation, UnderstandingChecks]