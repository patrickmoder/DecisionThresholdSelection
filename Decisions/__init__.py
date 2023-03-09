
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
    f1 = open(r"_static/treatments_rand1.csv", "r", encoding='utf-8-sig')
    f2 = open(r"_static/treatments_rand2.csv", "r", encoding='utf-8-sig')
    f3 = open(r"_static/treatments_rand3.csv", "r", encoding='utf-8-sig')
    f4 = open(r"_static/treatments_rand4.csv", "r", encoding='utf-8-sig')
    #asc = list(csv.DictReader(f))
    #desc = asc[::-1]
    rand1 = list(csv.DictReader(f1))
    rand2 = list(csv.DictReader(f2))
    rand3 = list(csv.DictReader(f3))
    rand4 = list(csv.DictReader(f4))
    sequences = itertools.cycle([rand1, rand2, rand3, rand4])
    #rowsr = itertools.cycle(rows)
    for player in subsession.get_players():
        r = subsession.round_number - 1
        rows = next(sequences)
        row = rows[r]
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
    treat = models.StringField(choices=[['rand1', 'rand1'], ['rand2', 'rand2'], ['rand3', 'rand3'], ['rand4', 'rand4']])
    th_opt = models.FloatField()
    selected_threshold = models.IntegerField()
    outcome = models.StringField()
    #cost_opt = models.IntegerField()
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
        thr = 0
        costr = 0
        thropt = player.th_opt / 100
        costoptr = player.c_FN * round((thropt * 20) * pow(baseP, thropt)) + player.c_FP * round(
            ((-thropt + 1) * 20) * pow(baseN, (-thropt + 1)))

        list_rand1 = list(range(1,97,4))
        list_rand2 = list(range(2,98,4))
        list_rand3 = list(range(3,99,4))
        list_rand4 = list(range(4,100,4))

        if player.id_in_group in list_rand1:
            player.treat = 'rand1'
        elif player.id_in_group in list_rand2:
            player.treat = 'rand2'
        elif player.id_in_group in list_rand3:
            player.treat = 'rand3'
        elif player.id_in_group in list_rand4:
            player.treat = 'rand4'

        return dict(
            abs = abs,
            baseN = int(baseN),
            baseP = int(baseP),
            thr = thr,
            costr = costr,
            thropt = thropt,
            costoptr = costoptr,
            list_rand1 = list_rand1,
            list_rand2 = list_rand2,
            list_rand3 = list_rand3,
            list_rand4 = list_rand4
        )
    def before_next_page(player, timeout_happened):
        import random
        thr = player.selected_threshold / 100
        abs = player.n_N + player.n_P
        baseN = player.n_N / 20
        baseP = player.n_P / 20
        #thropt = player.th_opt / 100
        #costoptr = player.c_FN * round((thropt * 20) * pow(baseP, thropt)) + player.c_FP * round(
            #((-thropt + 1) * 20) * pow(baseN, (-thropt + 1)))
        #costr = player.c_FN * round((thr * 20) * pow(baseP, thr)) + player.c_FP * round(
            #((-thr + 1) * 20) * pow(baseN, (-thr + 1)))
        m_prob = random.randrange(0, 100, 1) / 100
        prob_TP = 1 - (((-m_prob + 1) * 20) * pow(baseN, (-m_prob + 1))) / abs
        prob_TN = 1 - round((m_prob * 20) * pow(baseP, m_prob)) / abs

        if m_prob >= thr:
            out = random.choices(["TP", "FP"], weights = [prob_TP, 1-prob_TP], k=1)
            if TP in out:
                player.payoff = 100
                player.outcome = "TP"
            else:
                player.payoff = 100 - player.c_FP
                player.outcome = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob_TN, 1-prob_TN], k=1)
            if TN in out:
                player.payoff = 100
                player.outcome = "TN"
            else:
                player.payoff = 100 - player.c_FN
                player.outcome = "FN"


        #if 100 - (costr - costoptr) > 0:
        #    player.payoff = (100 - (costr - costoptr)) / 100
        #else:
        #    player.payoff = 0

page_sequence = [CutoffSelection]