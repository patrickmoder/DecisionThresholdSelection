
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after misclassifications (false negatives and false positives). We hypothesize that despite provided with all relevant cost information, decision makers may not select a cutoff that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
class C(BaseConstants):
    NAME_IN_URL = 'PostExperiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    age = models.IntegerField(label='Your age?', min=18)
    similar_task = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Have you ever done any similar task before?')
    similar_exp = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Have you taken part in a similar experiment before?')
    choice_criterion = models.StringField(choices=[['cost', 'overall cost'], ['cost after missed hits', 'cost after missed hits'], ['cost after false alarms', 'cost after false alarms'], ['probability of positive characteristic', 'probability of breakdown'], ['probability of negative characteristic', 'probability of no breakdown'], ['algorithm performance', 'algorithm performance'], ['other', 'other']], label='What criterion did you use to select the threshold?')
    choice_criterion_add = models.StringField(label='Which additional criteria did you use to select the threshold?', blank=True)
    gender = models.StringField(choices=[['female', 'female'], ['male', 'male'], ['diverse', 'diverse'], ['do not want to disclose', 'do not want to disclose']], label='Your gender?')
    nationality = models.StringField(label='Your nationality?')
    study_progress = models.IntegerField(label='How many semesters did you study so far in total?')
    professional_experience = models.IntegerField(label='Your professional experience in years?')
    highest_degree = models.StringField(choices=[['High School', 'High School'], ['Bachelors', 'Bachelors'], ['Masters', 'Masters'], ['Doctorate', 'Doctorate']], label='What is your highest degree in education?')
    strategy_change = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Did you change your strategy to select the threshold during the experiment?')
    strategy_how_why = models.LongStringField(label='&emsp;If yes, why and how did you adjust your strategy?', blank=True)
    strategy_when = models.IntegerField(label='&emsp;If yes, after how many rounds did you adjust the strategy?', max=12, min=1, blank=True)
    optimal_how_often = models.StringField(choices=[['never', 'never'], ['rarely', 'rarely'], ['sometimes', 'sometimes'], ['often', 'often'], ['always', 'always']], label='How often do you think did you select the optimal threshold?')
    optimal_confident = models.StringField(choices=[['not at all', 'not at all'], ['slightly', 'slightly'], ['quite a bit', 'quite a bit'], ['very', 'very'], ['extremely', 'extremely']], label='How confident are you that you selected the optimal threshold in the majority of rounds in this experiment?')
    feedback_general = models.LongStringField(blank=True, label='Do you like to share any other feedback with the experimenters?')
    study_field = models.StringField(choices=[['Formal sciences (incl. mathematics, computer science, etc.)', 'Formal sciences (incl. mathematics, computer science, etc.)'], ['Natural sciences (incl. physics, engineering, medicine, etc.)', 'Natural sciences (incl. physics, engineering, medicine, etc.)'], ['Social sciences (incl. economics, psychology, jurisprudence, etc.)', 'Social sciences (incl. economics, psychology, jurisprudence, etc.)']], label='Your field of study?')
class PostExperimentSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'nationality', 'study_progress', 'highest_degree', 'study_field', 'professional_experience',
                   'similar_exp', 'similar_task', 'optimal_confident', 'optimal_how_often',
                   'choice_criterion', 'choice_criterion_add',
                   'strategy_change', 'strategy_how_why', 'strategy_when',
                   'feedback_general']

class FinalPage(Page):
    pass

page_sequence = [FinalPage]