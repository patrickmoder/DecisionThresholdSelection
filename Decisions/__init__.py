
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after misclassifications (false negatives and false positives). We hypothesize that despite provided with all relevant cost information, decision makers may not select a cutoff that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
class C(BaseConstants):
    NAME_IN_URL = 'Decisions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 13
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
    clicked_help = models.IntegerField(initial=0, blank=True)
    out1 = models.StringField()
    out2 = models.StringField()
    out3 = models.StringField()
    out4 = models.StringField()
    out5 = models.StringField()
    out6 = models.StringField()
    out7 = models.StringField()
    out8 = models.StringField()
    out9 = models.StringField()
    out10 = models.StringField()
    m_prob1 = models.FloatField()
    m_prob2 = models.FloatField()
    m_prob3 = models.FloatField()
    m_prob4 = models.FloatField()
    m_prob5 = models.FloatField()
    m_prob6 = models.FloatField()
    m_prob7 = models.FloatField()
    m_prob8 = models.FloatField()
    m_prob9 = models.FloatField()
    m_prob10 = models.FloatField()

    #cost_opt = models.IntegerField()
    #reward = models.IntegerField()
    #theta = models.IntegerField()

class CutoffSelection(Page):
    form_model = 'player'
    form_fields = ['selected_threshold', 'clicked_help']
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
        import numpy as np
        thr = player.selected_threshold / 100
        abs = player.n_N + player.n_P
        baseN = player.n_N / 20
        baseP = player.n_P / 20
        #thropt = player.th_opt / 100
        #costoptr = player.c_FN * round((thropt * 20) * pow(baseP, thropt)) + player.c_FP * round(
            #((-thropt + 1) * 20) * pow(baseN, (-thropt + 1)))
        #costr = player.c_FN * round((thr * 20) * pow(baseP, thr)) + player.c_FP * round(
            #((-thr + 1) * 20) * pow(baseN, (-thr + 1)))
        #player.m_prob1 = random.uniform(1, 99) / 100
        player.m_prob1 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob2 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob3 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob4 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob5 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob6 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob7 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob8 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob9 = np.random.binomial(n=100, p=player.n_P/abs) / 100
        player.m_prob10 = np.random.binomial(n=100, p=player.n_P/abs) / 100

        prob1_FP = (((-player.m_prob1 + 1) * 20) * pow(baseN, (-player.m_prob1 + 1))) / abs
        prob1_FN = round((player.m_prob1 * 20) * pow(baseP, player.m_prob1)) / abs
        prob1_TP = (player.n_P - round((player.m_prob1 * 20) * pow(baseP, player.m_prob1))) / abs
        prob1_TN = (player.n_N - (((-player.m_prob1 + 1) * 20) * pow(baseN, (-player.m_prob1 + 1)))) / abs

        prob2_FP = (((-player.m_prob2 + 1) * 20) * pow(baseN, (-player.m_prob2 + 1))) / abs
        prob2_FN = round((player.m_prob2 * 20) * pow(baseP, player.m_prob2)) / abs
        prob2_TP = (player.n_P - round((player.m_prob2 * 20) * pow(baseP, player.m_prob2))) / abs
        prob2_TN = (player.n_N - (((-player.m_prob2 + 1) * 20) * pow(baseN, (-player.m_prob2 + 1)))) / abs

        prob3_FP = (((-player.m_prob3 + 1) * 20) * pow(baseN, (-player.m_prob3 + 1))) / abs
        prob3_FN = round((player.m_prob3 * 20) * pow(baseP, player.m_prob3)) / abs
        prob3_TP = (player.n_P - round((player.m_prob3 * 20) * pow(baseP, player.m_prob3))) / abs
        prob3_TN = (player.n_N - (((-player.m_prob3 + 1) * 20) * pow(baseN, (-player.m_prob3 + 1)))) / abs

        prob4_FP = (((-player.m_prob4 + 1) * 20) * pow(baseN, (-player.m_prob4 + 1))) / abs
        prob4_FN = round((player.m_prob4 * 20) * pow(baseP, player.m_prob4)) / abs
        prob4_TP = (player.n_P - round((player.m_prob4 * 20) * pow(baseP, player.m_prob4))) / abs
        prob4_TN = (player.n_N - (((-player.m_prob4 + 1) * 20) * pow(baseN, (-player.m_prob4 + 1)))) / abs

        prob5_FP = (((-player.m_prob5 + 1) * 20) * pow(baseN, (-player.m_prob5 + 1))) / abs
        prob5_FN = round((player.m_prob5 * 20) * pow(baseP, player.m_prob5)) / abs
        prob5_TP = (player.n_P - round((player.m_prob5 * 20) * pow(baseP, player.m_prob5))) / abs
        prob5_TN = (player.n_N - (((-player.m_prob5 + 1) * 20) * pow(baseN, (-player.m_prob5 + 1)))) / abs

        prob6_FP = (((-player.m_prob6 + 1) * 20) * pow(baseN, (-player.m_prob6 + 1))) / abs
        prob6_FN = round((player.m_prob6 * 20) * pow(baseP, player.m_prob6)) / abs
        prob6_TP = (player.n_P - round((player.m_prob6 * 20) * pow(baseP, player.m_prob6))) / abs
        prob6_TN = (player.n_N - (((-player.m_prob6 + 1) * 20) * pow(baseN, (-player.m_prob6 + 1)))) / abs

        prob7_FP = (((-player.m_prob7 + 1) * 20) * pow(baseN, (-player.m_prob7 + 1))) / abs
        prob7_FN = round((player.m_prob7 * 20) * pow(baseP, player.m_prob7)) / abs
        prob7_TP = (player.n_P - round((player.m_prob7 * 20) * pow(baseP, player.m_prob7))) / abs
        prob7_TN = (player.n_N - (((-player.m_prob7 + 1) * 20) * pow(baseN, (-player.m_prob7 + 1)))) / abs

        prob8_FP = (((-player.m_prob8 + 1) * 20) * pow(baseN, (-player.m_prob8 + 1))) / abs
        prob8_FN = round((player.m_prob8 * 20) * pow(baseP, player.m_prob8)) / abs
        prob8_TP = (player.n_P - round((player.m_prob8 * 20) * pow(baseP, player.m_prob8))) / abs
        prob8_TN = (player.n_N - (((-player.m_prob8 + 1) * 20) * pow(baseN, (-player.m_prob8 + 1)))) / abs

        prob9_FP = (((-player.m_prob9 + 1) * 20) * pow(baseN, (-player.m_prob9 + 1))) / abs
        prob9_FN = round((player.m_prob9 * 20) * pow(baseP, player.m_prob9)) / abs
        prob9_TP = (player.n_P - round((player.m_prob9 * 20) * pow(baseP, player.m_prob9))) / abs
        prob9_TN = (player.n_N - (((-player.m_prob9 + 1) * 20) * pow(baseN, (-player.m_prob9 + 1)))) / abs

        prob10_FP = (((-player.m_prob10 + 1) * 20) * pow(baseN, (-player.m_prob10 + 1))) / abs
        prob10_FN = round((player.m_prob10 * 20) * pow(baseP, player.m_prob10)) / abs
        prob10_TP = (player.n_P - round((player.m_prob10 * 20) * pow(baseP, player.m_prob10))) / abs
        prob10_TN = (player.n_N - (((-player.m_prob10 + 1) * 20) * pow(baseN, (-player.m_prob10 + 1)))) / abs

        if player.m_prob1 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob1_TP, prob1_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out1 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out1 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob1_TN, prob1_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out1 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out1 = "FN"

        if player.m_prob2 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob2_TP, prob2_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out2 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out2 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob2_TN, prob2_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out2 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out2 = "FN"

        if player.m_prob3 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob3_TP, prob3_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out3 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out3 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob3_TN, prob3_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out3 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out3 = "FN"

        if player.m_prob4 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob4_TP, prob4_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out4 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out4 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob4_TN, prob4_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out4 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out4 = "FN"

        if player.m_prob5 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob5_TP, prob5_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out5 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out5 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob5_TN, prob5_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out5 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out5 = "FN"

        if player.m_prob6 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob6_TP, prob6_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out6 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out6 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob6_TN, prob6_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out6 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out6 = "FN"

        if player.m_prob7 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob7_TP, prob7_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out7 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out7 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob7_TN, prob7_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out7 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out7 = "FN"

        if player.m_prob8 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob8_TP, prob8_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out8 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out8 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob8_TN, prob8_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out8 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out8 = "FN"

        if player.m_prob9 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob9_TP, prob9_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out9 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out9 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob9_TN, prob9_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out9 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out9 = "FN"

        if player.m_prob10 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob10_TP, prob10_FP], k=1)
            if "TP" in out:
                player.payoff += .05
                player.out10 = "TP"
            else:
                player.payoff -= player.c_FP / 100
                player.out10 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob10_TN, prob10_FN], k=1)
            if "TN" in out:
                player.payoff += .05
                player.out10 = "TN"
            else:
                player.payoff -= player.c_FN / 100
                player.out10 = "FN"

        #if 100 - (costr - costoptr) > 0:
        #    player.payoff = (100 - (costr - costoptr)) / 100
        #else:
        #    player.payoff = 0

page_sequence = [CutoffSelection]