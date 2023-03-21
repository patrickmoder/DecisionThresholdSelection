from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=5)
SESSION_CONFIGS = [dict(name='ExperimentDecisionThreshold', num_demo_participants=12, app_sequence=['Decisions', 'PostExperiment'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['payoff_r1', 'payoff_r2', 'payoff_r3', 'payoff_r4', 'payoff_r5', 'payoff_r6',
                      'payoff_r7', 'payoff_r8', 'payoff_r9', 'payoff_r10', 'payoff_r11', 'payoff_r12',
                      'payoff_r13',
                      'th_select_r1', 'th_opt_r1',
                      'realizations_r1_m1', 'realizations_r1_m2', 'realizations_r1_m3', 'realizations_r1_m4', 'realizations_r1_m5',
                      'realizations_r1_m6', 'realizations_r1_m7', 'realizations_r1_m8', 'realizations_r1_m9', 'realizations_r1_m10']
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


