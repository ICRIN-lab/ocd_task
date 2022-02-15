from task_template import TaskTemplate
from psychopy import visual, gui, data, event, core
import time
import os
import glob, pandas
import random

from screeninfo import get_monitors
screen = get_monitors()[0]

# if that raises an error, put this first
# from os import environ
# environ['DISPLAY'] = ':0.0'

width = screen.width
height = screen.height

class Toc(TaskTemplate):
    yes_key_name = "espace"
    yes_key_code = "space"
    no_key_name = "n"
    quit_code = "q"
    keys = [no_key_name, "space", yes_key_name, quit_code]

    launch_example = True
    next = f"Pour passer à l'instruction suivante, appuyez sur la touche {yes_key_name}"

    instructions = [f"Dans ce mini-jeu, appuyez sur la touche {yes_key_name} pour répondre oui,"
                    f"à la question. Utilisez la touche : '{no_key_name}' "
                    "Placez votre index sur la touche espace s'il-vous-plaît"]

    csv_headers = ['no_trial', 'id_candidate', 'result',  'ans_candidate', 'good_ans', 'correct',
                   'practice', 'reaction_time', 'time_stamp']




    def __init__(self, csv_folder='csv', launch_example=None):
            self.win = visual.Window(
            size=[width, height],  # if needed, change the size in corcondance with your monitor
            fullscr=False,
            units="pix",
            screen=0,
            allowStencil=False,
            monitor='testMonitor',
            color=self.bg,
            colorSpace='rgb'
        )

    def task(self, no_image=0,no_trial=0, exp_start_timestamp=0, trial_start_timestamp=0, practice=False):
        keyboard_pressed = False,


        image_stim = visual.ImageStim(self.win, image='img/test.png',
        #units="height",

        size=(height, ),
        #pos=(0, 0),
        #ori=0,
        mask=None)

        #text_stim = visual.TextStim(
        #self.win,
        #text="Showing image from file",
        #height=height,
        #wrapWidth=0.8,
        #pos=(0.0, 0)

        image_stim1 = visual.ImageStim(self.win, image='img/test1.png',
        #units="height",
        size=(height, ),
        #pos=(0, 0),
        #ori=0,
        mask=None)
        image_stim2 = visual.ImageStim(self.win, image='img/test2.png',
        #units="height",
        size=(height, ),
        pos=(0, 0),
        ori=0,
        mask=None)

        image_stim.draw()
        #text_stim.draw()
        self.win.flip()
        core.wait(1)

        self.create_visual_text("Question A1 oui ou non").draw()
        self.win.flip()
        resp1a, rt1a = self.get_response_with_time()

        self.create_visual_text("Question A2 oui ou non").draw()
        self.win.flip()
        resp2a, rt2a = self.get_response_with_time()

        self.create_visual_text("Question A3 oui ou non").draw()
        self.win.flip()
        resp3a, rt3a = self.get_response_with_time()


        image_stim1.draw()
        #text_stim.draw()
        self.win.flip()
        core.wait(2)


        self.create_visual_text("Question B1 oui ou non").draw()
        self.win.flip()
        resp1b, rt1b = self.get_response_with_time()

        self.create_visual_text("Question B2 oui ou non").draw()
        self.win.flip()
        resp2b, rt2b = self.get_response_with_time()

        self.create_visual_text("Question B3 oui ou non").draw()
        self.win.flip()
        resp3b, rt3b = self.get_response_with_time()

        image_stim2.draw()
        #text_stim.draw()
        self.win.flip()
        core.wait(3)

        self.create_visual_text("Question C1 oui ou non").draw()
        self.win.flip()
        resp1c, rt1c = self.get_response_with_time()

        self.create_visual_text("Question C2 oui ou non").draw()
        self.win.flip()
        resp2c, rt2c = self.get_response_with_time()

        self.create_visual_text("Question C3 oui ou non").draw()
        self.win.flip()
        resp3c, rt3c = self.get_response_with_time()

        listea = [i for i in range(0,4)]

        #{lambda x: resp}

        #self.update_csv(no_trial, self.participant, result, resp, good_ans, good_answer,
        #practice, round(rt, 2), round(time.time() - exp_start_timestamp, 2))

        quit_experiment(self)





exp = Toc()
exp.start()
