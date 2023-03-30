
from otree.api import *
c = cu

doc = 'When Artificial Intelligence based models are used to make predictions about a future state in operations management, they often classify two different outcomes: positive or negative. In order to adjust the algorithm for a given problem, one can tune the cutoff value, that determines the decision threshold between positive and negative predictions. The threshold should ideally be selected at a cutoff value that minimizes the costs for consequences after incorrect predictions (false alarms and missed hits). We hypothesize that despite provided with all relevant cost information, decision makers may not select a threshold that minimizes the overall costs but deviate from it. We are interested in which decision problem characteristics, cognitive limitations and human biases explain that behavior.'
class C(BaseConstants):
    NAME_IN_URL = 'Decisions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 18

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
    clicked_help = models.IntegerField(blank=True)
    moved_slider = models.IntegerField(blank=True)
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
    form_fields = ['selected_threshold', 'clicked_help', 'moved_slider']
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
        costs_FP = float(player.c_FP) / 100
        costs_FN = float(player.c_FN) / 100

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
                payoff_m1 = .05
                player.out1 = "TP"
            else:
                payoff_m1 = -costs_FP
                player.out1 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob1_TN, prob1_FN], k=1)
            if "TN" in out:
                payoff_m1 = .05
                player.out1 = "TN"
            else:
                payoff_m1 = -costs_FN
                player.out1 = "FN"

        if player.m_prob2 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob2_TP, prob2_FP], k=1)
            if "TP" in out:
                payoff_m2 = .05
                player.out2 = "TP"
            else:
                payoff_m2 = -costs_FP
                player.out2 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob2_TN, prob2_FN], k=1)
            if "TN" in out:
                payoff_m2 = .05
                player.out2 = "TN"
            else:
                payoff_m2 = -costs_FN
                player.out2 = "FN"

        if player.m_prob3 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob3_TP, prob3_FP], k=1)
            if "TP" in out:
                payoff_m3 = .05
                player.out3 = "TP"
            else:
                payoff_m3 = -costs_FP
                player.out3 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob3_TN, prob3_FN], k=1)
            if "TN" in out:
                payoff_m3 = .05
                player.out3 = "TN"
            else:
                payoff_m3 = -costs_FN
                player.out3 = "FN"

        if player.m_prob4 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob4_TP, prob4_FP], k=1)
            if "TP" in out:
                payoff_m4 = .05
                player.out4 = "TP"
            else:
                payoff_m4 = -costs_FP
                player.out4 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob4_TN, prob4_FN], k=1)
            if "TN" in out:
                payoff_m4 = .05
                player.out4 = "TN"
            else:
                payoff_m4 = -costs_FN
                player.out4 = "FN"

        if player.m_prob5 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob5_TP, prob5_FP], k=1)
            if "TP" in out:
                payoff_m5 = .05
                player.out5 = "TP"
            else:
                payoff_m5 = -costs_FP
                player.out5 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob5_TN, prob5_FN], k=1)
            if "TN" in out:
                payoff_m5 = .05
                player.out5 = "TN"
            else:
                payoff_m5 = -costs_FN
                player.out5 = "FN"

        if player.m_prob6 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob6_TP, prob6_FP], k=1)
            if "TP" in out:
                payoff_m6 = .05
                player.out6 = "TP"
            else:
                payoff_m6 = -costs_FP
                player.out6 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob6_TN, prob6_FN], k=1)
            if "TN" in out:
                payoff_m6 = .05
                player.out6 = "TN"
            else:
                payoff_m6 = -costs_FN
                player.out6 = "FN"

        if player.m_prob7 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob7_TP, prob7_FP], k=1)
            if "TP" in out:
                payoff_m7 = .05
                player.out7 = "TP"
            else:
                payoff_m7 = -costs_FP
                player.out7 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob7_TN, prob7_FN], k=1)
            if "TN" in out:
                payoff_m7 = .05
                player.out7 = "TN"
            else:
                payoff_m7= -costs_FN
                player.out7 = "FN"

        if player.m_prob8 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob8_TP, prob8_FP], k=1)
            if "TP" in out:
                payoff_m8 = .05
                player.out8 = "TP"
            else:
                payoff_m8 = -costs_FP
                player.out8 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob8_TN, prob8_FN], k=1)
            if "TN" in out:
                payoff_m8 = .05
                player.out8 = "TN"
            else:
                payoff_m8 = -costs_FN
                player.out8 = "FN"

        if player.m_prob9 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob9_TP, prob9_FP], k=1)
            if "TP" in out:
                payoff_m9 = .05
                player.out9 = "TP"
            else:
                payoff_m9 = -costs_FP
                player.out9 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob9_TN, prob9_FN], k=1)
            if "TN" in out:
                payoff_m9 = .05
                player.out9 = "TN"
            else:
                payoff_m9 = -costs_FN
                player.out9 = "FN"

        if player.m_prob10 >= thr:
            out = random.choices(["TP", "FP"], weights = [prob10_TP, prob10_FP], k=1)
            if "TP" in out:
                payoff_m10 = .05
                player.out10 = "TP"
            else:
                payoff_m10 = -costs_FP
                player.out10 = "FP"
        else:
            out = random.choices(["TN", "FN"], weights = [prob10_TN, prob10_FN], k=1)
            if "TN" in out:
                payoff_m10 = .05
                player.out10 = "TN"
            else:
                payoff_m10 = -costs_FN
                player.out10 = "FN"

        player.payoff = payoff_m1 + payoff_m2 + payoff_m3 + payoff_m4 + payoff_m5 + payoff_m6 + payoff_m7 + payoff_m8 + payoff_m9 + payoff_m10

        if player.payoff > 0:
            player.payoff = payoff_m1 + payoff_m2 + payoff_m3 + payoff_m4 + payoff_m5 + payoff_m6 + payoff_m7 + payoff_m8 + payoff_m9 + payoff_m10
        else:
            player.payoff = 0

        participant = player.participant
        if player.round_number == 1:
            pl_r1 = player.in_round(1)
            participant.payoff_r1 = pl_r1.payoff
            participant.th_select_r1 = pl_r1.selected_threshold / 100
            #participant.th_opt_r1 = pl_r1.th_opt
            participant.realizations_r1_m1 = pl_r1.out1
            participant.realizations_r1_m2 = pl_r1.out2
            participant.realizations_r1_m3 = pl_r1.out3
            participant.realizations_r1_m4 = pl_r1.out4
            participant.realizations_r1_m5 = pl_r1.out5
            participant.realizations_r1_m6 = pl_r1.out6
            participant.realizations_r1_m7 = pl_r1.out7
            participant.realizations_r1_m8 = pl_r1.out8
            participant.realizations_r1_m9 = pl_r1.out9
            participant.realizations_r1_m10 = pl_r1.out10

        if player.round_number == 2:
            pl_r2 = player.in_round(2)
            participant.payoff_r2 = pl_r2.payoff
            participant.th_select_r2 = pl_r2.selected_threshold / 100
            participant.realizations_r2_m1 = pl_r2.out1
            participant.realizations_r2_m2 = pl_r2.out2
            participant.realizations_r2_m3 = pl_r2.out3
            participant.realizations_r2_m4 = pl_r2.out4
            participant.realizations_r2_m5 = pl_r2.out5
            participant.realizations_r2_m6 = pl_r2.out6
            participant.realizations_r2_m7 = pl_r2.out7
            participant.realizations_r2_m8 = pl_r2.out8
            participant.realizations_r2_m9 = pl_r2.out9
            participant.realizations_r2_m10 = pl_r2.out10

        if player.round_number == 3:
            pl_r3 = player.in_round(3)
            participant.payoff_r3 = pl_r3.payoff
            participant.th_select_r3 = pl_r3.selected_threshold / 100
            participant.realizations_r3_m1 = pl_r3.out1
            participant.realizations_r3_m2 = pl_r3.out2
            participant.realizations_r3_m3 = pl_r3.out3
            participant.realizations_r3_m4 = pl_r3.out4
            participant.realizations_r3_m5 = pl_r3.out5
            participant.realizations_r3_m6 = pl_r3.out6
            participant.realizations_r3_m7 = pl_r3.out7
            participant.realizations_r3_m8 = pl_r3.out8
            participant.realizations_r3_m9 = pl_r3.out9
            participant.realizations_r3_m10 = pl_r3.out10

        if player.round_number == 4:
            pl_r4 = player.in_round(4)
            participant.payoff_r4 = pl_r4.payoff
            participant.th_select_r4 = pl_r4.selected_threshold / 100
            participant.realizations_r4_m1 = pl_r4.out1
            participant.realizations_r4_m2 = pl_r4.out2
            participant.realizations_r4_m3 = pl_r4.out3
            participant.realizations_r4_m4 = pl_r4.out4
            participant.realizations_r4_m5 = pl_r4.out5
            participant.realizations_r4_m6 = pl_r4.out6
            participant.realizations_r4_m7 = pl_r4.out7
            participant.realizations_r4_m8 = pl_r4.out8
            participant.realizations_r4_m9 = pl_r4.out9
            participant.realizations_r4_m10 = pl_r4.out10
        
        if player.round_number == 5:
            pl_r5 = player.in_round(5)
            participant.payoff_r5 = pl_r5.payoff
            participant.th_select_r5 = pl_r5.selected_threshold / 100
            participant.realizations_r5_m1 = pl_r5.out1
            participant.realizations_r5_m2 = pl_r5.out2
            participant.realizations_r5_m3 = pl_r5.out3
            participant.realizations_r5_m4 = pl_r5.out4
            participant.realizations_r5_m5 = pl_r5.out5
            participant.realizations_r5_m6 = pl_r5.out6
            participant.realizations_r5_m7 = pl_r5.out7
            participant.realizations_r5_m8 = pl_r5.out8
            participant.realizations_r5_m9 = pl_r5.out9
            participant.realizations_r5_m10 = pl_r5.out10
        
        if player.round_number == 6:
            pl_r6 = player.in_round(6)
            participant.payoff_r6 = pl_r6.payoff
            participant.th_select_r6 = pl_r6.selected_threshold / 100
            participant.realizations_r6_m1 = pl_r6.out1
            participant.realizations_r6_m2 = pl_r6.out2
            participant.realizations_r6_m3 = pl_r6.out3
            participant.realizations_r6_m4 = pl_r6.out4
            participant.realizations_r6_m5 = pl_r6.out5
            participant.realizations_r6_m6 = pl_r6.out6
            participant.realizations_r6_m7 = pl_r6.out7
            participant.realizations_r6_m8 = pl_r6.out8
            participant.realizations_r6_m9 = pl_r6.out9
            participant.realizations_r6_m10 = pl_r6.out10

        if player.round_number == 7:
            pl_r7 = player.in_round(7)
            participant.payoff_r7 = pl_r7.payoff
            participant.th_select_r7 = pl_r7.selected_threshold / 100
            participant.realizations_r7_m1 = pl_r7.out1
            participant.realizations_r7_m2 = pl_r7.out2
            participant.realizations_r7_m3 = pl_r7.out3
            participant.realizations_r7_m4 = pl_r7.out4
            participant.realizations_r7_m5 = pl_r7.out5
            participant.realizations_r7_m6 = pl_r7.out6
            participant.realizations_r7_m7 = pl_r7.out7
            participant.realizations_r7_m8 = pl_r7.out8
            participant.realizations_r7_m9 = pl_r7.out9
            participant.realizations_r7_m10 = pl_r7.out10

        if player.round_number == 8:
            pl_r8 = player.in_round(8)
            participant.payoff_r8 = pl_r8.payoff
            participant.th_select_r8 = pl_r8.selected_threshold / 100
            participant.realizations_r8_m1 = pl_r8.out1
            participant.realizations_r8_m2 = pl_r8.out2
            participant.realizations_r8_m3 = pl_r8.out3
            participant.realizations_r8_m4 = pl_r8.out4
            participant.realizations_r8_m5 = pl_r8.out5
            participant.realizations_r8_m6 = pl_r8.out6
            participant.realizations_r8_m7 = pl_r8.out7
            participant.realizations_r8_m8 = pl_r8.out8
            participant.realizations_r8_m9 = pl_r8.out9
            participant.realizations_r8_m10 = pl_r8.out10

        if player.round_number == 9:
            pl_r9 = player.in_round(9)
            participant.payoff_r9 = pl_r9.payoff
            participant.th_select_r9 = pl_r9.selected_threshold / 100
            participant.realizations_r9_m1 = pl_r9.out1
            participant.realizations_r9_m2 = pl_r9.out2
            participant.realizations_r9_m3 = pl_r9.out3
            participant.realizations_r9_m4 = pl_r9.out4
            participant.realizations_r9_m5 = pl_r9.out5
            participant.realizations_r9_m6 = pl_r9.out6
            participant.realizations_r9_m7 = pl_r9.out7
            participant.realizations_r9_m8 = pl_r9.out8
            participant.realizations_r9_m9 = pl_r9.out9
            participant.realizations_r9_m10 = pl_r9.out10
        
        if player.round_number == 10:
            pl_r10 = player.in_round(10)
            participant.payoff_r10 = pl_r10.payoff
            participant.th_select_r10 = pl_r10.selected_threshold / 100
            participant.realizations_r10_m1 = pl_r10.out1
            participant.realizations_r10_m2 = pl_r10.out2
            participant.realizations_r10_m3 = pl_r10.out3
            participant.realizations_r10_m4 = pl_r10.out4
            participant.realizations_r10_m5 = pl_r10.out5
            participant.realizations_r10_m6 = pl_r10.out6
            participant.realizations_r10_m7 = pl_r10.out7
            participant.realizations_r10_m8 = pl_r10.out8
            participant.realizations_r10_m9 = pl_r10.out9
            participant.realizations_r10_m10 = pl_r10.out10

        if player.round_number == 11:
            pl_r11 = player.in_round(11)
            participant.payoff_r11 = pl_r11.payoff
            participant.th_select_r11 = pl_r11.selected_threshold / 100
            participant.realizations_r11_m1 = pl_r11.out1
            participant.realizations_r11_m2 = pl_r11.out2
            participant.realizations_r11_m3 = pl_r11.out3
            participant.realizations_r11_m4 = pl_r11.out4
            participant.realizations_r11_m5 = pl_r11.out5
            participant.realizations_r11_m6 = pl_r11.out6
            participant.realizations_r11_m7 = pl_r11.out7
            participant.realizations_r11_m8 = pl_r11.out8
            participant.realizations_r11_m9 = pl_r11.out9
            participant.realizations_r11_m10 = pl_r11.out10
        
        if player.round_number == 12:
            pl_r12 = player.in_round(12)
            participant.payoff_r12 = pl_r12.payoff
            participant.th_select_r12 = pl_r12.selected_threshold / 100
            participant.realizations_r12_m1 = pl_r12.out1
            participant.realizations_r12_m2 = pl_r12.out2
            participant.realizations_r12_m3 = pl_r12.out3
            participant.realizations_r12_m4 = pl_r12.out4
            participant.realizations_r12_m5 = pl_r12.out5
            participant.realizations_r12_m6 = pl_r12.out6
            participant.realizations_r12_m7 = pl_r12.out7
            participant.realizations_r12_m8 = pl_r12.out8
            participant.realizations_r12_m9 = pl_r12.out9
            participant.realizations_r12_m10 = pl_r12.out10

        if player.round_number == 13:
            pl_r13 = player.in_round(13)
            participant.payoff_r13 = pl_r13.payoff
            participant.th_select_r13 = pl_r13.selected_threshold / 100
            participant.realizations_r13_m1 = pl_r13.out1
            participant.realizations_r13_m2 = pl_r13.out2
            participant.realizations_r13_m3 = pl_r13.out3
            participant.realizations_r13_m4 = pl_r13.out4
            participant.realizations_r13_m5 = pl_r13.out5
            participant.realizations_r13_m6 = pl_r13.out6
            participant.realizations_r13_m7 = pl_r13.out7
            participant.realizations_r13_m8 = pl_r13.out8
            participant.realizations_r13_m9 = pl_r13.out9
            participant.realizations_r13_m10 = pl_r13.out10

        if player.round_number == 14:
            pl_r14 = player.in_round(14)
            participant.payoff_r14 = pl_r14.payoff
            participant.th_select_r14 = pl_r14.selected_threshold / 100
            participant.realizations_r14_m1 = pl_r14.out1
            participant.realizations_r14_m2 = pl_r14.out2
            participant.realizations_r14_m3 = pl_r14.out3
            participant.realizations_r14_m4 = pl_r14.out4
            participant.realizations_r14_m5 = pl_r14.out5
            participant.realizations_r14_m6 = pl_r14.out6
            participant.realizations_r14_m7 = pl_r14.out7
            participant.realizations_r14_m8 = pl_r14.out8
            participant.realizations_r14_m9 = pl_r14.out9
            participant.realizations_r14_m10 = pl_r14.out10

        if player.round_number == 15:
            pl_r15 = player.in_round(15)
            participant.payoff_r15 = pl_r15.payoff
            participant.th_select_r15 = pl_r15.selected_threshold / 100
            participant.realizations_r15_m1 = pl_r15.out1
            participant.realizations_r15_m2 = pl_r15.out2
            participant.realizations_r15_m3 = pl_r15.out3
            participant.realizations_r15_m4 = pl_r15.out4
            participant.realizations_r15_m5 = pl_r15.out5
            participant.realizations_r15_m6 = pl_r15.out6
            participant.realizations_r15_m7 = pl_r15.out7
            participant.realizations_r15_m8 = pl_r15.out8
            participant.realizations_r15_m9 = pl_r15.out9
            participant.realizations_r15_m10 = pl_r15.out10

        if player.round_number == 16:
            pl_r16 = player.in_round(16)
            participant.payoff_r16 = pl_r16.payoff
            participant.th_select_r16 = pl_r16.selected_threshold / 100
            participant.realizations_r16_m1 = pl_r16.out1
            participant.realizations_r16_m2 = pl_r16.out2
            participant.realizations_r16_m3 = pl_r16.out3
            participant.realizations_r16_m4 = pl_r16.out4
            participant.realizations_r16_m5 = pl_r16.out5
            participant.realizations_r16_m6 = pl_r16.out6
            participant.realizations_r16_m7 = pl_r16.out7
            participant.realizations_r16_m8 = pl_r16.out8
            participant.realizations_r16_m9 = pl_r16.out9
            participant.realizations_r16_m10 = pl_r16.out10

        if player.round_number == 17:
            pl_r17 = player.in_round(17)
            participant.payoff_r17 = pl_r17.payoff
            participant.th_select_r17 = pl_r17.selected_threshold / 100
            participant.realizations_r17_m1 = pl_r17.out1
            participant.realizations_r17_m2 = pl_r17.out2
            participant.realizations_r17_m3 = pl_r17.out3
            participant.realizations_r17_m4 = pl_r17.out4
            participant.realizations_r17_m5 = pl_r17.out5
            participant.realizations_r17_m6 = pl_r17.out6
            participant.realizations_r17_m7 = pl_r17.out7
            participant.realizations_r17_m8 = pl_r17.out8
            participant.realizations_r17_m9 = pl_r17.out9
            participant.realizations_r17_m10 = pl_r17.out10

        if player.round_number == 18:
            pl_r18 = player.in_round(18)
            participant.payoff_r18 = pl_r18.payoff
            participant.th_select_r18 = pl_r18.selected_threshold / 100
            participant.realizations_r18_m1 = pl_r18.out1
            participant.realizations_r18_m2 = pl_r18.out2
            participant.realizations_r18_m3 = pl_r18.out3
            participant.realizations_r18_m4 = pl_r18.out4
            participant.realizations_r18_m5 = pl_r18.out5
            participant.realizations_r18_m6 = pl_r18.out6
            participant.realizations_r18_m7 = pl_r18.out7
            participant.realizations_r18_m8 = pl_r18.out8
            participant.realizations_r18_m9 = pl_r18.out9
            participant.realizations_r18_m10 = pl_r18.out10

page_sequence = [CutoffSelection]