from operator import concat
from task_template import TaskTemplate
from psychopy import visual, gui, data, event, core
import time
import os
import glob, pandas
import random
from screeninfo import get_monitors
from PIL import Image




screen = get_monitors()[0]


width = screen.width
height = screen.height




def size(no_image1):

    image = Image.open(f'img/test{no_image1}.png')
    imgwidth, imgheight = image.size

    if imgwidth > width:
        while imgwidth > width :
            imgwidth = imgwidth*0.9
            imgheight = imgheight*0.9
    if imgheight > height:
        while imgheight > height :
            imgwidth = imgwidth*0.9
            imgheight = imgheight*0.9

    return  imgwidth, imgheight

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


class Toc(TaskTemplate):
    trials = 1000
    yes_key_name = "a"
    yes_key_code = "a"
    no_key_name = "p"
    quit_code = "q"
    keys = [no_key_name, "space", yes_key_name, quit_code]

    next = f"Pour passer à l'instruction suivante, appuyez sur la touche {yes_key_name}"

    instructions = [f"Dans ce mini-jeu, appuyez sur la touche '{yes_key_name}' pour répondre oui ou pour selectionner la réponse de gauche \n\n"
                    f"appuyez sur la touche '{no_key_name}' pour répondre non ou pour selectionner la réponse de droite"]

    csv_headers = ['id_candidate', 'no_image', 'no_trial','question', 'result', 'ans_candidate','good_ans',
                   'reaction_time', 'time_stamp']




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
            exp_info = {'participant': '', "date": data.getDateStr()}
            gui.DlgFromDict(exp_info, title='Subliminal Priming Task', fixed=["date"])
            self.participant = exp_info["participant"]
            self.no_trial = 0
            self.no_image = 1
            file_name = exp_info['participant'] + '_' + exp_info['date']
            self.dataFile = open(f"{csv_folder}/{file_name}.csv", 'w')
            self.dataFile.write(", ".join(self.csv_headers))
            self.dataFile.write("\n")

    def init(self):
        self.no_trial = 0
        self.no_image = 1






    def task(self, no_trial, exp_start_timestamp, trial_start_timestamp, practice=False,no_image=1, qretry=[1,2]):
        yes_key_name = "p"
        no_key_name  = "a"

        qretry = range(0,32)
        no_image = self.no_image

        keyboard_pressed = True

        #diocq est un variable qui contient un dictionnaire structuré comme suit :
        # les clés correspondent au numéro des images
        # les valeurs sont des listes qui contiennent 3 éléments ou plus :
        # - integer : le type d'image (0 : image simple avec question(s), 1: 5 images d'affilés, 2: images pour les 7 différences)
        # - integer ou float : le nombre de seconde où l'image apparait
        # - Une ou plusieurs liste de string de 2 élements qui contiennent la question et la touche de la bonne réponse.

        dicoq = {

        1 : [0,3,
        ["Combien y a-t-il de personnes sur cette photo ? \n\n 9 / 15",
         yes_key_name],

        ["Combien y a-t-il de cafetières sur la photo ? \n\n 7 / 2",
        no_key_name],

        ],

        2 : [0,3,
        ["Combien y a-t-il de personnes sur cette photo ? \n\n 4 / 8",
        yes_key_name],

        ],

        3 : [0,6,
        ["Combien y a-t-il de personnes assises sur cette photo ? \n\n 2 / 4",
        yes_key_name],

        ["Combien y a-t-il de personnes cette photo ? \n\n 12 / 22",
        yes_key_name],

        ["Avez-vous vu une personne habillé d'une robe blanche ?",
        yes_key_name],
        ],

        4 : [0,3,
        ["Combien y a-t-il de personnes sur cette photo ? \n\n 4 / 3",
        no_key_name],

        ["Avez-vous vu une corde à sauter ?",
        yes_key_name],],




        5 : [0,2,
        ["Combien y a-t-il de personnes sur cette photo ? \n\n 4 / 3",
        yes_key_name],

        ["Avez-vous vu une balle sur cette photo ?",
        yes_key_name],


        ["Avez-vous vu une corde à sauter ?",
        yes_key_name],
        ],



        6 : [0,3,
        ["Toutes les personnes sont-elles habillées en blanc ?",
        no_key_name],

        ["Combien y a-t-il de personnes cette photo ? \n\n 20 / 40",
        yes_key_name],

        ],


        7 : [0,6,
        ["Combien y a-t-il de personnes diplomées photo ? \n\n 39 / 82",
        yes_key_name],


        ["Avez-vous vu une personne habillé d'une robe blanche ?",
        no_key_name],
        ],



        8 : [0,3,
        ["Combien y a-t-il de drapeaux cette photo ? \n\n 4 / 5",
        yes_key_name],

        ["Les drapeaux sont-ils tous plantés à la même profondeur ?",
        no_key_name],

        ],



        9 : [0,5,
        ["Avez-vous vu un téléphone sur cette photo ? \n\n",
        yes_key_name],

        ["De quelle couleure est ce téléphone ? \n\n noir / rose",
        no_key_name],

        ["Le téléphone était-il décroché ?",
        yes_key_name],
        ],


        10 : [0,4,
        ["Combien y a-t-il de femmes en bas à gauche de l'image ? \n\n 2 / 4",
        no_key_name],

        ["Avez-vous vu un point rouge sur cette photo ?",
        yes_key_name],

        ],


        11 : [0,3,
        ["Tout les personnages ont-ils un casque ?",
        no_key_name],

        ["Combien y a-t-il de personnages sur cette photos ? \n\n 55 / 201",
        yes_key_name],

        ],



        12 : [0,4,
        ["Combien y a-t-il de personnages sur cette photos ? \n\n 1 / 2",
        yes_key_name],

        ["Avez-vous vu des taches de peinture sur du véhicule ? ",
        yes_key_name],

        ["Avez-vous vu des pots de peinture sur le capot du véhicule ?",
        yes_key_name],
        ],



        13 : [0,2,
        ["Combien y a-t-il de personnages sur cette photo ? \n\n  2 / 4",
        yes_key_name],

        ],



        14 : [0,8,
        ["Combien y a-t-il de personnages sur cette photo ? \n\n 2 / 3",
        no_key_name],

        ["La pièce est-elle rangée ? ",
        no_key_name],

        ["Combien y a-t-il de posters sur les murs ? \n\n 9 / 21",
        yes_key_name],

        ["Avez-vous remarqué des vêtements qui ne sont pas pliés ?",
        yes_key_name],
        ],



        15 : [0,8,
        ["Avez-vous vu des mouchoirs usagés ?",
        yes_key_name],

        ["Avez-vous vu une éponge ?",
        yes_key_name],

        ["Avez-vous vu des serviettes usagées ?",
        yes_key_name],

        ["Les rebords de la fenêtre sont-ils propres ?",
        no_key_name]
        ],


        16 : [0,8,
        ["Avez-vous vu une pile de livre sur la droite de l'image ? \n\n",
        yes_key_name],

        ["Avez-vous vu un ceintre sur la gauche de l'image? \n\n ",
        yes_key_name],

        ],




        17 : [0,8,
        ["Combien y a-t-il de tasses sur cette photo ? \n\n 21 / 4",
        no_key_name],

        ["Avez-vous vu du linge sale sur cette photo ? ",
        yes_key_name],

        ["Avez-vous vu des restes alimentaires sur cette photo ?",
        yes_key_name],
        ],


        18 : [0,4,
        ["Combien avez-vous vu de penguins sur cette photo ? \n\n  24 / 12",
        no_key_name],
        ],


        19 : [0,5,
        ["Combien avez-vous vu d'humains sur cette photo ? \n\n  2 / 4" ,
        yes_key_name],

        ["Combien avez vous vu de moutons sur cette photo ? \n\n une cinquantaine / une dizaine",
        yes_key_name],
        ],


        20 : [0,5,
        ["Il y a plus de 7 tentacules visibles  \n\n  Vrai / Faux", yes_key_name],
        ["il y a autant de tentacules de part et d autre du clocher \n\n  Vrai / Faux", yes_key_name]
        ],


        21 : [0,6,
        ["Il y a autant de grands arbres a gauche qu a droite \n\n  Vrai / Faux", no_key_name],
        ["la caleche est tiree par deux chevaux \n\n  Vrai / Faux", no_key_name],
        ["on peut apercevoir un clocher \n\n  Vrai / Faux ", no_key_name]
        ],


        22 : [0,4,
        ["Les toits sont bleus \n\n  Vrai / Faux", yes_key_name]
        ],


        23 : [0,7,
        ["Il y a 5 bateaux \n\n  Vrai / Faux", yes_key_name],
        ["Il y a  des bateaux a 2 voiles \n\n  Vrai / Faux ", yes_key_name],
        ["Tous les protagonistes portent des couvres chefs \n\n  Vrai / Faux", no_key_name],
        ["On peut voir un chien \n\n  Vrai / Faux", no_key_name]
        ],


        24 : [0,4,
        ["Toutes les lunes sont dans le même sens \n\n  Vrai / Faux", yes_key_name]
        ],


        25 : [0,8,
        ["Les tapis sont \n\n  de biais / alignés", yes_key_name],
        ["Il y a une brosse a dent pres du lit \n\n  Vrai / Faux", no_key_name],
        ["L armoire est \n\n ouverte / fermee", no_key_name]
        ],


        26 : [0,4,
        ["Il y a \n\n plus de 10 pommes / moins de 10 pommes", no_key_name]
        ],


        27 : [0,4,
        ["Les costumes sont ideniques \n\n  Vrai / Faux", yes_key_name]
        ],

        28 : [0,4,
        ["Les elephants sont symetriques \n\n  Vrai / Faux", no_key_name]
        ],

        29 : [0,4,
        ["Les toits sont a la meme hauteur \n\n  Vrai / Faux", no_key_name]
        ],

        30 : [0,4,
        ["Le deuxieme elephant porte  \n\n  une pyramide / un cone ", yes_key_name]
        ],

        31 : [0,6,
        ["Il y a plus de 30 papillons  \n\n  Vrai / Faux ", no_key_name]
        ]



        }

        if dicoq[no_image][0] == 0 :


            imgwidth, imgheight = size(no_image)


            image_stim = visual.ImageStim(self.win, image=f'img/test{no_image}.png',
            units="pix",

            size=(imgwidth, imgheight),
            #pos=(0, 0),
            #ori=0,
            mask=None)
            image_stim.draw()
            #text_stim.draw()
            self.win.flip()
            core.wait(dicoq[no_image][1])

        elif dicoq[no_image][0] == 1 :

            for i in ['a','b','c','d','e'] :
                imgwidth, imgheight = size(f'{no_image}{i}')

                image_stim = visual.ImageStim(self.win, image=f'img/test{no_image}{i}.png',
                units="pix",

                size=(imgwidth, imgheight),
                mask=None)
                image_stim.draw()
                self.win.flip()
                core.wait(dicoq[no_image][1])





        elif dicoq[no_image][0] == 2 :

            im1 = Image.open(f'img/test{no_image}a.png')
            im2 = Image.open(f'img/test{no_image}b.png')

            get_concat_h(im1,im2).save(f'img/test{no_image}c.png')

            imgwidth, imgheight = size(f'{no_image}c')

            image_stim = visual.ImageStim(self.win, image=f'img/test{no_image}c.png',
            units="pix",

            size=(imgwidth, imgheight),
            #pos=(0, 0),
            #ori=0,
            mask=None)
            image_stim.draw()
            #text_stim.draw()
            self.win.flip()
            core.wait(dicoq[no_image][1])


        else :
            print('test')


        if dicoq[no_image][0] == 1 :
            imgwidth, imgheight = size(f'{no_image}q')

            text_stim= visual.TextStim(self.win, text='Avez-vous vu cette image dans la série précédente ?',
            pos=(0, -0.80),
            units='norm')
            image_stim = visual.ImageStim(self.win, image=f'img/test{no_image}q.png',
            units="pix",
            size=(imgwidth*0.8, imgheight*0.8),
            pos=(0, 30),
            ori=0,
            mask=None)
            image_stim.draw()
            text_stim.draw()
            self.win.flip()
            resp, rt = self.get_response_with_time()


            if resp == dicoq[no_image][2]:

                result = 1


                self.update_csv(self.participant, no_image, self.no_trial, 'Avez-vous vu cette image dans la série précédente ?', result , resp,
                dicoq[no_image][2], round(rt,  2), round(time.time() - exp_start_timestamp, 2))


            else :
                result = 0

                self.update_csv(self.participant, no_image, self.no_trial, 'Avez-vous vu cette image dans la série précédente ?', result, resp,
                dicoq[no_image][2], round(rt, 2), round(time.time() - exp_start_timestamp, 2))


        for i in range(2,len(dicoq[no_image])):

            self.create_visual_text(dicoq[no_image][i][0]).draw()
            self.win.flip()
            resp, rt = self.get_response_with_time()


            if resp == dicoq[no_image][i][1]:

                result = 1


                self.update_csv(self.participant, no_image, self.no_trial, str(dicoq[no_image][i][0]).replace('\n\n',''), result , resp,
                dicoq[no_image][i][1], round(rt,  2), round(time.time() - exp_start_timestamp, 2))


            else :
                result = 0

                self.update_csv(self.participant, no_image, self.no_trial, str(dicoq[no_image][i][0]).replace('\n\n',''), result, resp,
                dicoq[no_image][i][1], round(rt, 2), round(time.time() - exp_start_timestamp, 2))




        if no_image in qretry :

            self.create_visual_text("Voulez vous revoir l'image,"
            "et répondre à nouveau "
            f"aux questions ?\n\n  {yes_key_name} pour passer à la question suivante  \n\n {no_key_name} pour revoir").draw()
            self.win.flip()
            resp, rt = self.get_response_with_time()



            if resp == yes_key_name :

                self.create_visual_text("Image suivante").draw()
                self.win.flip()
                self.no_image += 1

            else :
                print('respawn')
                self.no_trial += 1



            self.update_csv(self.participant, no_image, self.no_trial, 'Retry','0',resp, '0',
                             round(rt, 2), round(time.time() - exp_start_timestamp, 2))

        else:

            self.no_image += 1
            self.no_trial = 0

            if self.no_image > len(dicoq) :
                self.create_visual_text("Fin de la tâche").draw()
                self.win.flip()
                exit()

            self.create_visual_text("Image suivante").draw()
            self.win.flip()














exp = Toc(csv_folder="csv")
exp.start()
