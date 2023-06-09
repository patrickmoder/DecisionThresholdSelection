
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after incorrect predictions (false alarms and missed hits). We hypothesize that despite provided with all relevant cost information, decision makers may not select a threshold that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
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
        choices=[['True Positive (TP)', 'Correct Prediction of Breakdown'],
                 ['True Negative (TN)', 'Correct Prediction of No Breakdown'],
                 ['False Positive (FP)', 'False Alarm'], ['False Negative (FN)', 'Missed Hit']],
        label='<b> What outcome is missing (?) in the matrix above? </b>')
    Confusion_Matrix_missing_value_C = models.StringField(
        choices=[['True Positive (TP)', 'Correct Prediction of Complaint'],
                 ['True Negative (TN)', 'Correct Prediction of No Complaint'],
                 ['False Positive (FP)', 'False Alarm'], ['False Negative (FN)', 'Missed Hit']],
        label='<b> What outcome is missing (?) in the matrix above? </b>')
    #Accuracy_Understanding_Check = models.StringField(
        #choices=[['0', '0'], ['0.2', '0.2'], ['0.4', '0.4'], ['0.6', '0.6'], ['0.8', '0.8'], ['1', '1']],
        #label='<b> Based on the confusion matrix shown above, what is the classification accuracy of the algorithm? </b>')
    Misclassification_Costs_Understanding_Check_1 = models.IntegerField(
        label='<b> For a threshold D = 0.32, what is the overall number of incorrect predictions on the training set? </b>')
    Misclassification_Costs_Understanding_Check_2 = models.IntegerField(
        label='<b> For a threshold D = 0.53, what are the total costs for incorrect predictions on the training set? </b>')
    Threshold_Introduction_Understanding_Check = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']],
        label='<b> Do you agree with the following statement? "In order to reduce Missed Hits, the threshold D should be increased." </b>')
    Threshold_Introduction_Easy = models.StringField(
        choices=[['Breakdown', 'Breakdown'], ['No Breakdown', 'No Breakdown']],
        label='Imagine, an AI algorithm outputs a breakdown-probability for a particular machine of 0.41 in the next 48 hours and your chosen decision threshold D is 0.35. <b>What would be predicted to happen in the next 48 hours for that particular machine? </b>',
        )
    Threshold_Introduction_Easy_C = models.StringField(
        choices=[['Complaint', 'Complaint'], ['No Complaint', 'No Complaint']],
        label='Imagine, an AI algorithm outputs a complaint-probability for a particular customer of 0.41 your chosen decision threshold D is 0.35. <b>What would be predicted to happen for that particular customer? </b>',
        )

    Payoff_Introduction_Understanding_Check = models.IntegerField(label='Let us consider that in the example above you select the threshold D = 0.66 in one particular round of the experiment. When the AI algorithm gets applied to predict breakdowns of the 10 machines, the following outcomes get realized <i>(remember that these numbers will be shown to you only after the last round of the experiment)</i>:'
                                                                        '<ul><li>3 Correct Predictions of Breakdowns and 4 Correct Predictions of No Breakdown</li><li>2 Missed Hits and 1 False Alarm</li></ul>'
                                                                        '<b>Remember that your maximum bonus payoff for each round is 50 cost units. According to the payoff calculation rule introduced earlier, what would be your bonus payoff (cost units) for this round?</b>'
                                                                  )
    Payoff_Introduction_Understanding_Check_C = models.IntegerField(
        label='Let us consider that in the example above you select the threshold D = 0.66 in one particular round of the experiment. When the AI algorithm gets applied to predict complaints of the 10 customers, the following outcomes get realized <i>(remember that these numbers will be shown to you only after the last round of the experiment)</i>:'
              '<ul><li>3 Correct Predictions of Complaints and 4 Correct Predictions of No Complaints</li><li>2 Missed Hits and 1 False Alarm</li></ul>'
              '<b>Remember that your maximum bonus payoff for each round is 50 cost units. According to the payoff calculation rule introduced earlier, what would be your bonus payoff (cost units) for this round?</b>'
        )

    #understand_instr = models.BooleanField(
    #    choices=[[True, 'Yes'], [False, 'No']],
    #    label='Did you understand the instructions and how your payoff gets calculated?')
    num_ui_false = models.IntegerField(initial=0)
    num_failed_attempts = models.IntegerField(initial=0)

class Welcome(Page):
    pass
class ScenarioDescription(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        if player.id_in_group % 2 == 0:
            participant.scenario = "breakdown"
        else:
            participant.scenario = "complaint"
class ThresholdIntroduction(Page):
    pass
class MisclassificationCosts(Page):
    pass
class TaskDescription(Page):
    pass
class PayoffCalculation(Page):
    pass
    #form_model = 'player'
    #form_fields = ['understand_instr']
    #@staticmethod
    #def error_message(player:Player, values):
    #    solutions = dict(understand_instr=True)
    #    if values != solutions:
    #        player.num_ui_false += 1
    #        return "Are you sure? You might not be able to participate in the experiment if you answer again that you did not understand the instructions. Please review your answer."


class UnderstandingChecks(Page):
    form_model = 'player'
    form_fields = ['Confusion_Matrix_missing_value', 'Threshold_Introduction_Easy',
                   'Misclassification_Costs_Understanding_Check_1', 'Misclassification_Costs_Understanding_Check_2', 'Threshold_Introduction_Understanding_Check',
                   'Payoff_Introduction_Understanding_Check']
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.scenario == "breakdown"

    @staticmethod
    def error_message(player, values):
        solutions = dict(Confusion_Matrix_missing_value='False Positive (FP)',
                         Threshold_Introduction_Easy='Breakdown',
                         Misclassification_Costs_Understanding_Check_1=51,
                         Misclassification_Costs_Understanding_Check_2=102,
                         Threshold_Introduction_Understanding_Check=False,
                         Payoff_Introduction_Understanding_Check=43)

        if values != solutions:
            player.num_failed_attempts += 1

        error_messages = dict()

        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = 'Wrong answer. Please try again.'

        return error_messages

        #return error_messages
                #return "One or more answers were incorrect. Please try again."

class UnderstandingChecks_C(Page):
    form_model = 'player'
    form_fields = ['Confusion_Matrix_missing_value_C', 'Threshold_Introduction_Easy_C',
                   'Misclassification_Costs_Understanding_Check_1', 'Misclassification_Costs_Understanding_Check_2', 'Threshold_Introduction_Understanding_Check',
                   'Payoff_Introduction_Understanding_Check_C']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.scenario != "breakdown"

    @staticmethod
    def error_message(player, values):
        solutions_c = dict(Confusion_Matrix_missing_value_C='False Positive (FP)', Threshold_Introduction_Easy_C='Complaint',
                             Misclassification_Costs_Understanding_Check_1=51,
                             Misclassification_Costs_Understanding_Check_2=102,
                             Threshold_Introduction_Understanding_Check=False,
                             Payoff_Introduction_Understanding_Check_C = 43
                             )

        if values != solutions_c:
            player.num_failed_attempts += 1

        error_messages_c = dict()

        for field_name in solutions_c:
            if values[field_name] != solutions_c[field_name]:
                error_messages_c[field_name] = 'Wrong answer. Please try again.'

        return error_messages_c

class CorrectAnswers(Page):
    pass

page_sequence = [Welcome, ScenarioDescription, ThresholdIntroduction, MisclassificationCosts, TaskDescription, PayoffCalculation, UnderstandingChecks, UnderstandingChecks_C, CorrectAnswers]

