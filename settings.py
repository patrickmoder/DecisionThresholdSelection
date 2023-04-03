from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=5)
SESSION_CONFIGS = [dict(name='ExperimentDecisionThreshold', num_demo_participants=12, app_sequence=['Decisions', 'choice_list', 'PostExperiment'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['scenario',
                      'payoff_r1', 'payoff_r2', 'payoff_r3', 'payoff_r4', 'payoff_r5', 'payoff_r6',
                      'payoff_r7', 'payoff_r8', 'payoff_r9', 'payoff_r10', 'payoff_r11', 'payoff_r12',
                      'payoff_r13', 'payoff_r14', 'payoff_r15', 'payoff_r16', 'payoff_r17', 'payoff_r18',
                      'th_select_r1', 'th_select_r2', 'th_select_r3', 'th_select_r4', 'th_select_r5', 'th_select_r6',
                      'th_select_r7', 'th_select_r8', 'th_select_r9', 'th_select_r10', 'th_select_r11', 'th_select_r12',
                      'th_select_r13', 'th_select_r14', 'th_select_r15', 'th_select_r16', 'th_select_r17', 'th_select_r18',
                      'realizations_r1_m1', 'realizations_r1_m2', 'realizations_r1_m3', 'realizations_r1_m4',
                      'realizations_r1_m5', 'realizations_r1_m6', 'realizations_r1_m7', 'realizations_r1_m8',
                      'realizations_r1_m9', 'realizations_r1_m10',
                      'realizations_r2_m1', 'realizations_r2_m2', 'realizations_r2_m3', 'realizations_r2_m4',
                      'realizations_r2_m5', 'realizations_r2_m6', 'realizations_r2_m7', 'realizations_r2_m8',
                      'realizations_r2_m9', 'realizations_r2_m10',
                      'realizations_r3_m1', 'realizations_r3_m2', 'realizations_r3_m3', 'realizations_r3_m4',
                      'realizations_r3_m5', 'realizations_r3_m6', 'realizations_r3_m7', 'realizations_r3_m8',
                      'realizations_r3_m9', 'realizations_r3_m10',
                      'realizations_r4_m1', 'realizations_r4_m2', 'realizations_r4_m3', 'realizations_r4_m4',
                      'realizations_r4_m5', 'realizations_r4_m6', 'realizations_r4_m7', 'realizations_r4_m8',
                      'realizations_r4_m9', 'realizations_r4_m10',
                      'realizations_r5_m1', 'realizations_r5_m2', 'realizations_r5_m3', 'realizations_r5_m4',
                      'realizations_r5_m5', 'realizations_r5_m6', 'realizations_r5_m7', 'realizations_r5_m8',
                      'realizations_r5_m9', 'realizations_r5_m10',
                      'realizations_r6_m1', 'realizations_r6_m2', 'realizations_r6_m3', 'realizations_r6_m4',
                      'realizations_r6_m5', 'realizations_r6_m6', 'realizations_r6_m7', 'realizations_r6_m8',
                      'realizations_r6_m9', 'realizations_r6_m10',
                      'realizations_r7_m1', 'realizations_r7_m2', 'realizations_r7_m3', 'realizations_r7_m4',
                      'realizations_r7_m5', 'realizations_r7_m6', 'realizations_r7_m7', 'realizations_r7_m8',
                      'realizations_r7_m9', 'realizations_r7_m10',
                      'realizations_r8_m1', 'realizations_r8_m2', 'realizations_r8_m3', 'realizations_r8_m4',
                      'realizations_r8_m5', 'realizations_r8_m6', 'realizations_r8_m7', 'realizations_r8_m8',
                      'realizations_r8_m9', 'realizations_r8_m10',
                      'realizations_r9_m1', 'realizations_r9_m2', 'realizations_r9_m3', 'realizations_r9_m4',
                      'realizations_r9_m5', 'realizations_r9_m6', 'realizations_r9_m7', 'realizations_r9_m8',
                      'realizations_r9_m9', 'realizations_r9_m10',
                      'realizations_r10_m1', 'realizations_r10_m2', 'realizations_r10_m3', 'realizations_r10_m4',
                      'realizations_r10_m5', 'realizations_r10_m6', 'realizations_r10_m7', 'realizations_r10_m8',
                      'realizations_r10_m9', 'realizations_r10_m10',
                      'realizations_r11_m1', 'realizations_r11_m2', 'realizations_r11_m3', 'realizations_r11_m4',
                      'realizations_r11_m5', 'realizations_r11_m6', 'realizations_r11_m7', 'realizations_r11_m8',
                      'realizations_r11_m9', 'realizations_r11_m10',
                      'realizations_r12_m1', 'realizations_r12_m2', 'realizations_r12_m3', 'realizations_r12_m4',
                      'realizations_r12_m5', 'realizations_r12_m6', 'realizations_r12_m7', 'realizations_r12_m8',
                      'realizations_r12_m9', 'realizations_r12_m10',
                      'realizations_r13_m1', 'realizations_r13_m2', 'realizations_r13_m3', 'realizations_r13_m4',
                      'realizations_r13_m5', 'realizations_r13_m6', 'realizations_r13_m7', 'realizations_r13_m8',
                      'realizations_r13_m9', 'realizations_r13_m10',
                      'realizations_r14_m1', 'realizations_r14_m2', 'realizations_r14_m3', 'realizations_r14_m4',
                      'realizations_r14_m5', 'realizations_r14_m6', 'realizations_r14_m7', 'realizations_r14_m8',
                      'realizations_r14_m9', 'realizations_r14_m10',
                      'realizations_r15_m1', 'realizations_r15_m2', 'realizations_r15_m3', 'realizations_r15_m4',
                      'realizations_r15_m5', 'realizations_r15_m6', 'realizations_r15_m7', 'realizations_r15_m8',
                      'realizations_r15_m9', 'realizations_r15_m10',
                      'realizations_r16_m1', 'realizations_r16_m2', 'realizations_r16_m3', 'realizations_r16_m4',
                      'realizations_r16_m5', 'realizations_r16_m6', 'realizations_r16_m7', 'realizations_r16_m8',
                      'realizations_r16_m9', 'realizations_r16_m10',
                      'realizations_r17_m1', 'realizations_r17_m2', 'realizations_r17_m3', 'realizations_r17_m4',
                      'realizations_r17_m5', 'realizations_r17_m6', 'realizations_r17_m7', 'realizations_r17_m8',
                      'realizations_r17_m9', 'realizations_r17_m10',
                      'realizations_r18_m1', 'realizations_r18_m2', 'realizations_r18_m3', 'realizations_r18_m4',
                      'realizations_r18_m5', 'realizations_r18_m6', 'realizations_r18_m7', 'realizations_r18_m8',
                      'realizations_r18_m9', 'realizations_r18_m10',
                      'payoff_lottery']
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


