
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after misclassifications (false negatives and false positives). We hypothesize that despite provided with all relevant cost information, decision makers may not select a cutoff that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
class C(BaseConstants):
    NAME_IN_URL = 'PostExperiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    age = models.IntegerField(label='Your age?')
    similar_task = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Have you ever done some similar task before?')
    understand_instr = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Did you understand the instructions?')
    choice_criterion = models.StringField(choices=[['cost', 'cost'], ['probability of positive characteristic', 'probability of positive characteristic'], ['probability of negative characteristic', 'probability of negative characteristic'], ['algorithm performance', 'algorithm performance'], ['other', 'other']], label='What criterion did you use to select the threshold?')
    choice_criterion_add = models.StringField(label='Which additional criteria did you use to select the threshold?')
    gender = models.StringField(choices=[['female', 'female'], ['male', 'male'], ['diverse', 'diverse'], ['do not want to disclose', 'do not want to disclose']], label='Your gender?')
    nationality = models.StringField(label='Your nationality?')
    study_progress = models.IntegerField(label='Your overall study progress in years?')
    professional_experience = models.IntegerField(label='Your professional experience in years?')
    highest_degree = models.StringField(choices=[['High School', 'High School'], ['Bachelors', 'Bachelors'], ['Masters', 'Masters'], ['Doctorate', 'Doctorate']], label='What is your highest degree in education?')
    strategy_change = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Did you change your strategy to select the threshold during the experiment?')
    strategy_how_why = models.LongStringField(label='If yes, why and how did you adjust your strategy?')
    strategy_when = models.IntegerField(label='If yes, after how many rounds did you adjust the strategy?', max=C.NUM_ROUNDS, min=1)
    optimal_how_often = models.StringField(choices=[['never', 'never'], ['rarely', 'rarely'], ['sometimes', 'sometimes'], ['often', 'often'], ['always', 'always']], label='How often do you think that you selected the optimal threshold?')
    optimal_confident = models.IntegerField(label='How confident are you that you selected the optimal threshold in the majority of rounds in this experiment?', max=5, min=1)
    feedback_general = models.LongStringField(blank=True, label='Do you like to share any other feedback with the experimenters?')
    study_field = models.StringField(choices=[['Formal sciences (incl. mathematics, computer science, etc.)', 'Formal sciences (incl. mathematics, computer science, etc.)'], ['Natural sciences (incl. physics, engineering, medicine, etc.)', 'Natural sciences (incl. physics, engineering, medicine, etc.)'], ['Social sciences (incl. economics, psychology, jurisprudence, etc.)', 'Social sciences (incl. economics, psychology, jurisprudence, etc.)']], label='Your field of study?')
    theta = models.FloatField(min=0)
    treatment = models.StringField(choices=[['1', '1'], ['2', '2'], ['3', '3']])
    n_N = models.IntegerField(choices=[])
    n_P = models.IntegerField(choices=[])
    c_FN = models.IntegerField(choices=[])
    c_FP = models.IntegerField(choices=[])
class CutoffSelection1(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        abs = player.n_N + player.n_P
        baseN = player.n_N / 20
        baseP = player.n_P / 20
        return dict(
            abs = abs,
            baseN = int(baseN),
            baseP = int(baseP)
        )
    @staticmethod
    def js_vars(player: Player):
        return dict(threshold_range=C.THRESHOLD_RANGE)
page_sequence = [CutoffSelection1]