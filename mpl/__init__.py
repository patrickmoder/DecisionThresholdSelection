from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from mpl.config import *
import random
from random import randrange


author = 'Felix Holzmeister'

doc = """
Multiple price list task as proposed by Holt/Laury (2002), American Economic Review 92(5).
"""

class Constants(BaseConstants):

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Task-specific Settings --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # lottery payoffs
    # "high" and "low" outcomes (in currency units set in settings.py) of "lottery A" and "lottery B"
    # note that payoffs are identical for all choices and only probabilities of "high" and "low" outcomes change
    lottery_a_hi = 2.00
    lottery_a_lo = 1.60
    lottery_b_hi = 3.85
    lottery_b_lo = 0.10

    # number of binary choices between "lottery A" and "lottery B"
    # note that the number of choices determines the probabilities of high and low outcomes of lotteries "A" and "B"
    # for <num_choices = X>, the probability of outcome "high" is 1/X for the first choice, 2/X for the second, etc.
    num_choices = 10

    # include 'certain' choice (** only applies if <variation_type = 'probability'> **)
    # if <certain_choice = True>, the binary choice with probability of the outcome "high" being equal to 1 is included
    # if <certain_choice = False>, the list only contains (<num_choices> - 1) binary decision pairs
    # note, however, that the probability of outcome "high" is set by <num_choices>, not (<num_choices> - 1), though
    # i.e., if <certain_choice = False>, the last choice implies a probability of (X - 1)/X (given <num_choices = X>)
    certain_choice = True

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # show each lottery pair on a separate page
    # if <one_choice_per_page = True>, each single binary choice between lottery "A" and "B" is shown on a separate page
    # if <one_choice_per_page = False>, all <num_choices> choices are displayed in a table on one page
    one_choice_per_page = False

    # order choices between lottery pairs randomly
    # if <random_order = True>, the ordering of binary decisions is randomized for display
    # if <random_order = False>, binary choices are listed in ascending order of the probability of the "high" outcome
    random_order = False

    # enforce consistency, i.e. only allow for a single switching point
    # if <enforce_consistency = True>, all options "A" above a selected option "A" are automatically selected
    # similarly, all options "B" below a selected option "B" are automatically checked, implying consistent choices
    # note that <enforce_consistency> is only implemented if <one_choice_per_page = False> and <random_order = False>
    enforce_consistency = False

    # depict probabilities as percentage numbers
    # if <percentage = True>, the probability of outcome "high" will be displayed as percentage number
    # if <percentage = False>, the probabilities will be displayed as fractions, i.e. "1/X", "2/X", etc.
    percentage = False

    # show small pie charts for each lottery
    # if <small_pies = True>, a pie chart depicting the probabilities of outcomes is rendered next to each lottery
    # if <small_pies = False>, no graphical representation of probabilities is displayed
    small_pies = True

    # display lotteries in terms of large pie charts
    # if <large_pies = True>, lotteries are depicted as pie charts; if <large_pies = False> lotteries are list items
    # note that <large_pies = True> only affects the task's appearance if <one_choice_per_page = True>
    large_pies = True

    # show progress bar
    # if <progress_bar = True> and <one_choice_per_page = True>, a progress bar is rendered
    # if <progress_bar = False>, no information with respect to the advance within the task is displayed
    # the progress bar graphically depicts the advance within the task in terms of how many decision have been made
    # further, information in terms of "page x out of <num_choices>" (with x denoting the current choice) is provided
    progress_bar = True

    # show instructions page
    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show results page summarizing the task's outcome including payoff information
    # if <results = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <results = False>, the template "Decision.html" will not be rendered
    results = True

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- oTree Settings (Don't Modify) --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    name_in_url = 'mpl'
    players_per_group = None

    if one_choice_per_page:
        if certain_choice:
            num_rounds = num_choices
        else:
            num_rounds = num_choices - 1
    else:
        num_rounds = 1


# ******************************************************************************************************************** #
# *** CLASS SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:

            n = Constants.num_choices
            for p in self.get_players():

                # create list of lottery indices
                # ----------------------------------------------------------------------------------------------------
                indices = [j for j in range(1, n)]
                indices.append(n) if Constants.certain_choice else None

                # create list of probabilities
                # ----------------------------------------------------------------------------------------------------
                if Constants.percentage:
                    probabilities = [
                        "{0:.2f}".format(k / n * 100) + "%"
                        for k in indices
                    ]
                else:
                    probabilities = [
                        str(k) + "/" + str(n)
                        for k in indices
                    ]

                # create list corresponding to form_field variables including all choices
                # ----------------------------------------------------------------------------------------------------
                form_fields = ['choice_' + str(k) for k in indices]

                # create list of choices
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['mpl_choices'] = list(
                    zip(indices, form_fields, probabilities)
                )

                # randomly determine index/choice of binary decision to pay
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['mpl_index_to_pay'] = random.choice(indices)
                p.participant.vars['mpl_choice_to_pay'] = 'choice_' + str(p.participant.vars['mpl_index_to_pay'])

                # randomize order of lotteries if <random_order = True>
                # ----------------------------------------------------------------------------------------------------
                if Constants.random_order:
                    random.shuffle(p.participant.vars['mpl_choices'])

                # initiate list for choices made
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['mpl_choices_made'] = [None for j in range(1, n + 1)]

            # generate random switching point for PlayerBot in tests.py
            # --------------------------------------------------------------------------------------------------------
            for participant in self.session.get_participants():
                participant.vars['mpl_switching_point'] = random.randint(1, n)


# ******************************************************************************************************************** #
# *** CLASS GROUP
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER
# ******************************************************************************************************************** #
class Player(BasePlayer):

    # add model fields to class player
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if Constants.certain_choice:
        for j in range(1, Constants.num_choices + 1):
            locals()['choice_' + str(j)] = models.StringField()
        del j
    else:
        for j in range(1, Constants.num_choices):
            locals()['choice_' + str(j)] = models.StringField()
        del j

    random_draw = models.IntegerField()
    choice_to_pay = models.StringField()
    option_to_pay = models.StringField()
    inconsistent = models.IntegerField()
    switching_row = models.IntegerField()

    # set player's payoff
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_payoffs(self):

        # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
        # ------------------------------------------------------------------------------------------------------------
        self.random_draw = randrange(1, len(self.participant.vars['mpl_choices']))

        # set <choice_to_pay> to participant.var['choice_to_pay'] determined creating_session
        # ------------------------------------------------------------------------------------------------------------
        self.choice_to_pay = self.participant.vars['mpl_choice_to_pay']

        # elicit whether lottery "A" or "B" was chosen for the respective choice
        # ------------------------------------------------------------------------------------------------------------
        self.option_to_pay = getattr(self, self.choice_to_pay)

        # set player's payoff
        # ------------------------------------------------------------------------------------------------------------
        if self.option_to_pay == 'A':
            if self.random_draw <= self.participant.vars['mpl_index_to_pay']:
                self.payoff = Constants.lottery_a_hi
            else:
                self.payoff = Constants.lottery_a_lo
        else:
            if self.random_draw <= self.participant.vars['mpl_index_to_pay']:
                self.payoff = Constants.lottery_b_hi
            else:
                self.payoff = Constants.lottery_b_lo

        # set payoff as global variable
        # ------------------------------------------------------------------------------------------------------------
        self.participant.vars['mpl_payoff'] = self.payoff

    # determine consistency
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_consistency(self):

        n = Constants.num_choices

        # replace A's by 1's and B's by 0's
        self.participant.vars['mpl_choices_made'] = [
            1 if j == 'A' else 0 for j in self.participant.vars['mpl_choices_made']
        ]

        # check for multiple switching behavior
        for j in range(1, n):
            choices = self.participant.vars['mpl_choices_made']
            self.inconsistent = 1 if choices[j] > choices[j - 1] else 0
            if self.inconsistent == 1:
                break

    # determine switching row
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_switching_row(self):

        # set switching point to row number of first 'B' choice
        if self.inconsistent == 0:
            self.switching_row = sum(self.participant.vars['mpl_choices_made']) + 1

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return {
        'lottery_a_lo': c(Constants.lottery_a_lo),
        'lottery_a_hi': c(Constants.lottery_a_hi),
        'lottery_b_lo': c(Constants.lottery_b_lo),
        'lottery_b_hi': c(Constants.lottery_b_hi)
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        return {
            'num_choices':  len(self.participant.vars['mpl_choices'])
        }


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form model
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    def get_form_fields(self):

        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]

        # provide form field associated with pagination or full list
        if Constants.one_choice_per_page:
            page = self.subsession.round_number
            return [form_fields[page - 1]]
        else:
            return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # specify info for progress bar
        total = len(self.participant.vars['mpl_choices'])
        page = self.subsession.round_number
        progress = page / total * 100

        if Constants.one_choice_per_page:
            return {
                'page':      page,
                'total':     total,
                'progress':  progress,
                'choices':   [self.player.participant.vars['mpl_choices'][page - 1]]
            }
        else:
            return {
                'choices':   self.player.participant.vars['mpl_choices']
            }

    # set player's payoff
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):

        # unzip indices and form fields from <mpl_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][0]
        index = indices[round_number - 1]

        # if choices are displayed sequentially
        # ------------------------------------------------------------------------------------------------------------
        if Constants.one_choice_per_page:

            # replace current choice in <choices_made>
            current_choice = getattr(self.player, form_fields[round_number - 1])
            self.participant.vars['mpl_choices_made'][index - 1] = current_choice

            # if current choice equals index to pay ...
            if index == self.player.participant.vars['mpl_index_to_pay']:
                # set payoff
                self.player.set_payoffs()

            # after final choice
            if round_number == Constants.num_choices:
                # determine consistency
                self.player.set_consistency()
                # set switching row
                self.player.set_switching_row()

        # if choices are displayed in tabular format
        # ------------------------------------------------------------------------------------------------------------
        if not Constants.one_choice_per_page:

            # replace choices in <choices_made>
            for j, choice in zip(indices, form_fields):
                choice_i = getattr(self.player, choice)
                self.participant.vars['mpl_choices_made'][j - 1] = choice_i

            # set payoff
            self.player.set_payoffs()
            # determine consistency
            self.player.set_consistency()
            # set switching row
            self.player.set_switching_row()


# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        if Constants.one_choice_per_page:
            return self.subsession.round_number == Constants.num_rounds
        else:
            return True

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # unzip <mpl_choices> into list of lists
        choices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])]
        indices = choices[0]

        # get index, round, and choice to pay
        index_to_pay = self.player.participant.vars['mpl_index_to_pay']
        round_to_pay = indices.index(index_to_pay) + 1
        choice_to_pay = self.participant.vars['mpl_choices'][round_to_pay - 1]

        if Constants.one_choice_per_page:
            return {
                'choice_to_pay':  [choice_to_pay],
                'option_to_pay':  self.player.in_round(round_to_pay).option_to_pay,
                'payoff':         self.player.in_round(round_to_pay).payoff,
            }
        else:
            return {
                'choice_to_pay':  [choice_to_pay],
                'option_to_pay':  self.player.option_to_pay,
                'payoff':         self.player.payoff
            }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
