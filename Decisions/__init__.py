
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
    #session = subsession.session
    import csv
    import random
    import itertools

    f = open(r"_static/treatments.csv", "r", encoding='utf-8-sig')
    rowsa = list(csv.DictReader(f))
    rowsb = rowsa[::-1]
    rowsc = random.sample(rowsa, len(rowsa))
    sequences = itertools.cycle([rowsa, rowsb, rowsc])
    #rowsr = itertools.cycle(rows)
    for player in subsession.get_players():
        r = subsession.round_number - 1
        rows = next(sequences)
        row = rows[r]
        #print('treatment is', row)
        player.n_N = int(row['n_N'])
        player.n_P = int(row['n_P'])
        player.c_FN = int(row['c_FN'])
        player.c_FP = int(row['c_FP'])
        player.th_opt = int(row['th_opt'])
        player.scen = int(row['scen'])
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    n_N = models.IntegerField()
    n_P = models.IntegerField()
    c_FN = models.IntegerField()
    c_FP = models.IntegerField()
    scen = models.IntegerField()
    #seq = models.IntegerField()
    th_opt = models.FloatField()
    selected_threshold = models.IntegerField()
    cost_opt = models.IntegerField()
    #reward = models.IntegerField()
    #theta = models.IntegerField()

class CutoffSelection(Page):
    form_model = 'player'
    form_fields = ['selected_threshold']
    @staticmethod
    def vars_for_template(player: Player):
        abs = player.n_N + player.n_P
        baseN = player.n_N / 20
        baseP = player.n_P / 20
        thr = player.field_maybe_none(selected_threshold) / 100
        costr = player.c_FN * Math.round((thr * 20) * Math.pow(baseP, thr)) + player.c_FP * Math.round(((-thr + 1)* 20) * Math.pow(baseN, (-thr + 1)))
        thropt = player.th_opt / 100
        costoptr = player.c_FN * Math.round((thropt * 20) * Math.pow(baseP, thropt)) + player.c_FP * Math.round(((-thropt + 1)* 20) * Math.pow(baseN, (-thropt + 1)))
        
        return dict(
            abs = abs,
            baseN = int(baseN),
            baseP = int(baseP),
            thr = field_maybe_none(thr),
            costr = field_maybe_none(costr),
            thropt = thropt,
            costoptr = costoptr,
        )
    def before_next_page(player: Player):
        if 100 - (costr - costoptr) > 0:
            player.payoff = 100 - (costr - costoptr)
        else:
            player.payoff = 0

page_sequence = [CutoffSelection]