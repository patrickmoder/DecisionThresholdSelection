
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after misclassifications (false negatives and false positives). We hypothesize that despite provided with all relevant cost information, decision makers may not select a cutoff that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
class C(BaseConstants):
    NAME_IN_URL = 'Decisions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9
    THRESHOLD_RANGE = 1
    BUDGET_START = cu(8)
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    import csv
    import random
    import itertools
    
    
    f = open(r"_static/treatments.csv", "r", encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    rowsr = itertools.cycle(random.sample(rows, len(rows)))
    print(rows)
    
    for p in subsession.get_players():
        row = next(rowsr)
        #print('treatment is', row)
        p.n_N = int(row['n_N'])
        p.n_P = int(row['n_P'])
        p.c_FN = int(row['c_FN'])
        p.c_FP = int(row['c_FP'])
        p.th_opt = int(row['th_opt'])
        p.scen = int(row['scen'])
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    n_N = models.IntegerField()
    n_P = models.IntegerField()
    c_FN = models.IntegerField()
    c_FP = models.IntegerField()
    scen = models.IntegerField()
    th_opt = models.FloatField()
    selected_threshold = models.IntegerField(blank=True)
    cost_opt = models.IntegerField()
    reward = models.IntegerField()
    theta = models.IntegerField()
def set_payoffs(player: Player):
    session = player.session
    subsession = player.subsession
    players = subsession.get_players()
    for player in players:
        player.payoff = player.n_N
class CutoffSelection(Page):
    form_model = 'player'
    form_fields = ['selected_threshold']
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
page_sequence = [CutoffSelection]