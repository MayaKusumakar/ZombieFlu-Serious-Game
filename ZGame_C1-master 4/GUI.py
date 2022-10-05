import json
import uuid
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAY_TYPE import PLAY_TYPE
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS
from tkinter import *
import gym_zgame.envs.model.City
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

class GUI(Frame):

    def __init__(self, zgame, master):
        super(GUI, self).__init__(master)
        self.env = zgame.env
        self.neighborhoods, self.fear, self.resources, self.orig_alive, self.orig_dead, self.score, self.total_score = self.env.city.getNeiborhoods()
        self.GAME_ID = zgame.GAME_ID
        self.turn = zgame.turn
        self.max_turns = zgame.max_turns
        self.DATA_LOG_FILE_NAME = zgame.DATA_LOG_FILE_NAME
        self.grid()
        self.env.reset()
        self.list_active = []
        self.list_sickly = []
        self.list_dead = []
        self.list_zombie = []
        self.xlist = []
        self.graphed = False
        self.legend = False
        self.appended = False
        self.ar1 = -1
        self.ar2 = -1
        self.create_widgets()


    def set1A(self):
        self.ar1 = 0

    def set1R(self):
        self.ar1 = 1

    def set2A(self):
        self.ar2 = 0

    def set2R(self):
        self.ar2 = 1

    def create_widgets(self):
        self.graphed = False
        self.legend = False
        self.appended = False

        # cmd line UI
        # print(self.env.render(mode='human'))

        # left frame (titles and tables)
        left = Frame(self)
        left.grid(row=0, column=0)

        title = Frame(left, bg="red")
        title.grid(row=0, column=0)

        tables = Frame(left, bg="blue", width=21)
        tables.grid(row=1, column=0)

        graphs = Frame(left, bg="green")
        graphs.grid(row=2, column=0)

        # print title "ZGAME"
        Label(title, text="ZGAME", font='Chalkduster 35', justify=LEFT, width=22).grid(row=0, column=0, padx=(6, 7),
                                                                                       pady=(6, 7))

        # print 3 by 3 tables of neighborhoods
        self.grid3by3(tables)

        # print 3 buttons for graphs and informations
        Button(graphs, text = "Show graph", command = lambda : self.check_graph(left, tables, graphs), width=27, height = 2, highlightbackground="green")\
            .grid(row = 0, column = 0, columnspan = 2, padx = (5,2), pady = 4)

        Button(graphs, text = "Show legend", command = lambda : self.check_legend(left, tables, graphs), width=27, height = 2, highlightbackground="green")\
            .grid(row = 0, column = 2, columnspan = 2, padx = (2,4), pady = 4)

        right = Frame(self, bg='#86b8b0',padx=10,pady=37)
        right.grid(row=0, column=1)
        # GLOBAL INFO
        str = ' Turn: {0} of {1}'.format(self.turn, self.max_turns) \
              + '\n Fear: {}'.format(self.fear) \
              + '\n Resources: {}'.format(self.resources)
        Label(right, text=str, justify=LEFT, bg='#b886af').grid(row=3, column=2, columnspan=4, rowspan=3, padx=10,
                                                                pady=10, ipadx=10, ipady=10)

        str = 'Turn Score: {0} (Total Score: {1})'.format(self.score, self.total_score) \
              + '\nLiving at Start: {}'.format(self.orig_alive) \
              + '\nDead at Start: {}'.format(self.orig_dead)
        Label(right, text=str, justify=LEFT, bg='#b886af').grid(row=6, column=2, rowspan=3, columnspan=4, padx=10,
                                                                pady=10, ipadx=10, ipady=10)
        Label(right, text="Deployments", bg='#e32770').grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        Label(right, text="Locations", bg='#e32770').grid(row=0, column=1, columnspan=1, padx=10, pady=10, ipadx=5,
                                                          ipady=5)
        loc_str = ""
        for i in range(9):
            if i == 8:
                loc_str += "{0} - {1}".format(LOCATIONS(i).value, LOCATIONS(i).name)
            else:
                loc_str += "{0} - {1}\n".format(LOCATIONS(i).value, LOCATIONS(i).name)

        Label(right, text=loc_str, justify=LEFT, bg='#dfcec2').grid(row=1, column=1, rowspan=10, columnspan=1, padx=10,
                                                                    pady=10, ipadx=5, ipady=5)
        Label(right, text=self.getDeps(), justify=LEFT, bg='#dfcec2').grid(row=1, column=0, rowspan=24, padx=10,
                                                                           pady=10,
                                                                           ipadx=5, ipady=5)

        Label(right, text="Location 1", bg='#5e817b').grid(row=14, column=2, columnspan=2, rowspan=2, padx=10, pady=10,
                                                           ipadx=5, ipady=5)
        self.loc1 = Entry(right, bg='#5e817b')
        self.loc1.grid(row=14, column=4, columnspan=2, rowspan=2, padx=10, pady=10)

        Label(right, text="Deployment 1", bg='#5e817b').grid(row=16, column=2, columnspan=2, rowspan=2, padx=10,
                                                             pady=10, ipadx=5, ipady=5)
        self.dep1 = Entry(right, bg='#5e817b')
        self.dep1.grid(row=16, column=4, columnspan=2, rowspan=2, padx=10, pady=10)

        Label(right, text="Location 2", bg='#5e817b').grid(row=18, column=2, columnspan=2, rowspan=2, padx=10, pady=10,
                                                           ipadx=5, ipady=5)
        self.loc2 = Entry(right, bg='#5e817b')
        self.loc2.grid(row=18, column=4, columnspan=2, rowspan=2, padx=10, pady=10)

        Label(right, text="Deployment 2", bg='#5e817b').grid(row=20, column=2, columnspan=2, rowspan=2, padx=10,
                                                             pady=10, ipadx=5, ipady=5)
        self.dep2 = Entry(right, bg='#5e817b')
        self.dep2.grid(row=20, column=4, columnspan=2, rowspan=2, padx=10, pady=10)

        self.next = Button(right, text="Next step", command=self.check_update, height=2, width=45, bg='#b8ac86')
        self.next.grid(row=24, column=1, columnspan=8, rowspan=2, padx=10, pady=10)

        Button(right, text="Quit", command=self.quit, height=2, width=25, bg='#b8ac86').grid(row=0, column=3,
                                                                                             columnspan=2, rowspan=1,
                                                                                             padx=10, pady=10)
        v = IntVar()
        x = IntVar()
        self.ar1 = -1
        self.ar2 = -1
        Radiobutton(right, bg='#5e817b', variable=v, value=1, text="Add", padx=20, command=self.set1A,
                    indicatoron=0, width=5).grid(column=1, row=14, rowspan=2, padx=10, pady=10, ipadx=5, ipady=5)
        Radiobutton(right, bg='#5e817b', variable=v, value=2, text="Remove", padx=20, command=self.set1R,
                    indicatoron=0, width=5).grid(column=1, row=16, rowspan=2, padx=10, pady=10, ipadx=5, ipady=5)
        Radiobutton(right, bg='#5e817b', variable=x, value=3, text="Add", padx=20, command=self.set2A,
                    indicatoron=0, width=5).grid(column=1, row=18, rowspan=2, padx=10, pady=10, ipadx=5, ipady=5)
        Radiobutton(right, bg='#5e817b', variable=x, value=4, text="Remove", padx=20, command=self.set2R,
                    indicatoron=0, width=5).grid(column=1, row=20, rowspan=2, padx=10, pady=10, ipadx=5, ipady=5)

    def grid3by3(self, frame):

        active = 0
        dead = 0
        sickly = 0
        zombie = 0

        nbh_c = None
        nbh_n = None
        nbh_s = None
        nbh_e = None
        nbh_w = None
        nbh_ne = None
        nbh_nw = None
        nbh_se = None
        nbh_sw = None
        for nbh in self.neighborhoods:
            nbh_c = nbh if nbh.location is LOCATIONS.CENTER else nbh_c
            nbh_n = nbh if nbh.location is LOCATIONS.N else nbh_n
            nbh_s = nbh if nbh.location is LOCATIONS.S else nbh_s
            nbh_e = nbh if nbh.location is LOCATIONS.E else nbh_e
            nbh_w = nbh if nbh.location is LOCATIONS.W else nbh_w
            nbh_ne = nbh if nbh.location is LOCATIONS.NE else nbh_ne
            nbh_nw = nbh if nbh.location is LOCATIONS.NW else nbh_nw
            nbh_se = nbh if nbh.location is LOCATIONS.SE else nbh_se
            nbh_sw = nbh if nbh.location is LOCATIONS.SW else nbh_sw
            active += nbh.num_active
            dead += nbh.num_dead
            sickly += nbh.num_sickly
            zombie += nbh.num_zombie
        if (not self.appended):
            self.xlist.append(self.turn)
            self.list_active.append(active)
            self.list_dead.append(dead)
            self.list_sickly.append(sickly)
            self.list_zombie.append(zombie)

        # printing information for NW
        self.oneblock(frame, nbh_nw, 1, 0, (10, 5), (10, 5), '#00cccc')

        # printing information for N
        self.oneblock(frame, nbh_n, 1, 1, 5, (10, 5), "#00ff80")

        # printing information for NE
        self.oneblock(frame, nbh_ne, 1, 2, (5, 10), (10, 5), "#00cccc")

        # printing information for W
        self.oneblock(frame, nbh_w, 2, 0, (10, 5), 5, "#00ff80")

        # printing information for C
        self.oneblock(frame, nbh_c, 2, 1, 5, 5, "#00cccc")

        # printing information for E
        self.oneblock(frame, nbh_e, 2, 2, (5, 10), 5, "#00ff80")

        # printing information for SW
        self.oneblock(frame, nbh_sw, 3, 0, (10, 5), (5, 10), "#00cccc")

        # printing information for S
        self.oneblock(frame, nbh_s, 3, 1, 5, (5, 10), "#00ff80")

        # printing information for SE
        self.oneblock(frame, nbh_se, 3, 2, (5, 10), (5, 10), "#00cccc")

        self.appended = True

    # prints info for one block and button that leads to drawing pie chart
    def oneblock(self, frame, nbh, row_index, col_index, padx_value, pady_value, color):
        Label(frame,
              text="Active: {0} \nSickly: {1} \nZombies: {2} \nDead: {3} "
                   "\nLiving at Start: {4} \nDead at Start: {5} \nDeployments: {6} \nSanitation: {7}" \
              .format(self.env.city.mask_visible_data(nbh, nbh.num_active).name,
                      self.env.city.mask_visible_data(nbh, nbh.num_sickly).name,
                      self.env.city.mask_visible_data(nbh, nbh.num_zombie).name,
                      self.env.city.mask_visible_data(nbh, nbh.num_dead).name,
                      nbh.orig_alive,
                      nbh.orig_dead,
                      nbh.get_current_deps(),
                      int(nbh.sanitation)), justify=LEFT, width=19, height=10, bg=color
              ).grid(row=row_index, column=col_index, sticky=N + E + W + S, padx=padx_value, pady=pady_value)

        Button(frame, command=lambda: self.pieButtons(frame, nbh, row_index, col_index, padx_value, pady_value, color),
               text="i", highlightbackground=color
               ).grid(row=row_index, column=col_index, sticky=E + N, padx=padx_value, pady=pady_value)

    # draws pie chart and button to exit out of pie chart
    def pieButtons(self, frame, nbh, row_index, col_index, padx_value, pady_value, color):
        fig = Figure(figsize=(4, 4), dpi=35)
        fig.patch.set_facecolor(color)
        subplot = fig.add_subplot(111)
        pieSizes = [nbh.num_dead, nbh.num_sickly, nbh.num_active, nbh.num_zombie]
        subplot.pie(pieSizes, shadow=True, startangle=90)
        subplot.axis('equal')
        pie2 = FigureCanvasTkAgg(fig, frame)
        pie2.get_tk_widget().grid(row=row_index, column=col_index, sticky=N + E + S + W, padx=padx_value,
                                  pady=pady_value)

        Button(frame, command=lambda: self.oneblock(frame, nbh, row_index, col_index, padx_value, pady_value, color),
               text="X", highlightbackground=color
               ).grid(row=row_index, column=col_index, sticky=E + N, padx=padx_value, pady=pady_value)

    def check_graph(self, left, tables, graphs):
        if (self.graphed):
            Label(tables, bg="blue", width=21, height=21).grid(row=1, column=0, rowspan=3, columnspan=3, sticky=N + E + W + S)
            self.grid3by3(tables)
            Button(graphs, text="Show graph", command=lambda: self.check_graph(left, tables, graphs), width=27, height=2,
                   highlightbackground="green") \
                .grid(row=0, column=0, columnspan=2, padx=(5, 2), pady=4)
            self.graphed = False
        else:
            self.graph(tables)
            Button(graphs, text="Exit graph", command=lambda: self.check_graph(left, tables, graphs), width=27, height=2,
                   highlightbackground="green" , fg="red") \
                .grid(row=0, column=0, columnspan=2, padx=(5, 2), pady=4)
            Button(graphs, text="Show legend", command=lambda: self.check_legend(left, tables, graphs), width=27,
                   height=2, highlightbackground="green") \
                .grid(row=0, column=2, columnspan=2, padx=(2, 4), pady=4)
            self.legend = False
            self.graphed = True

    def graph(self, frame):
        fig = Figure(figsize=(4, 4), dpi=35)

        subplot = fig.add_subplot(111)
        subplot.plot(self.xlist,self.list_active, "go-")
        subplot.plot(self.xlist,self.list_sickly, "o-", color='#f7941b')
        subplot.plot(self.xlist,self.list_dead, "ro-")
        subplot.plot(self.xlist,self.list_zombie, "bo-")
        subplot.get_yaxis().set_visible(False)

        graph = FigureCanvasTkAgg(fig, frame)
        graph.get_tk_widget().grid(row=1, column=0, rowspan=3, columnspan=3, sticky=N + E + W + S, padx=10, pady=10)

    def check_legend(self, left, tables, graphs):
        if (self.legend):
            Label(tables, bg = "blue", width = 21, height = 21).grid(row = 1, column = 0, rowspan = 3, columnspan = 3, sticky = N+E+W+S)
            self.grid3by3(tables)
            Button(graphs, text="Show legend", command=lambda: self.check_legend(left, tables, graphs), width=27,
                   height=2, highlightbackground="green") \
                .grid(row=0, column=2, columnspan=2, padx=(2, 4), pady=4)
            self.legend = False

        else:
            self.info_display(tables)
            Button(graphs, text="Exit legend", command=lambda: self.check_legend(left, tables, graphs), width=27,
                   height=2, highlightbackground="green" , fg="red") \
                .grid(row=0, column=2, columnspan=2, padx=(2, 4), pady=4)
            Button(graphs, text="Show graph", command=lambda: self.check_graph(left, tables, graphs), width=27,
                   height=2,
                   highlightbackground="green") \
                .grid(row=0, column=0, columnspan=2, padx=(5, 2), pady=4)
            self.graphed = False
            self.legend = True



    def info_display(self, frame):
        im = Image.open("graph_legend.png")
        im.thumbnail((600, 600))
        ph = ImageTk.PhotoImage(im)

        label = Label(frame, image = ph, width = 10, height = 10)
        label.grid(row=1, column=0, rowspan=3, columnspan=3, sticky=N + E + W + S, padx=10, pady=10)
        label.image = ph

    # function for quitting the gamme
    def quit(self):
        self.winfo_children()[0].quit()

    # check if all inputs are set before updating the GUI and Zgame Env
    def check_update(self):

        try:
            location_1 = int(self.loc1.get())
            deployment_1 = int(self.dep1.get())
            location_2 = int(self.loc2.get())
            deployment_2 = int(self.dep2.get())

        except:
            self.next['text'] = "Invalid Input"
            self.next['fg'] = "red"
        else:
            if (int(self.loc1.get()) > 8 or int(self.loc1.get()) < 0):
                self.next['text'] = "Invalid Location 1 Input"
                self.next['fg'] = "red"
            elif (int(self.dep1.get()) > 29 or int(self.dep1.get()) < 0):
                self.next['text'] = "Invalid Deployment 1 Input"
                self.next['fg'] = "red"
            elif (int(self.loc2.get()) > 8 or int(self.loc2.get()) < 0):
                self.next['text'] = "Invalid Location 2 Input"
                self.next['fg'] = "red"
            elif (int(self.dep2.get()) > 29 or int(self.dep2.get()) < 0):
                self.next['text'] = "Invalid Deployment 2 Input"
                self.next['fg'] = "red"
            elif (self.ar1 == -1 or self.ar2 == -1):
                self.next['text'] = "Select Add or remove"
                self.next['fg'] = "red"
            elif self.ar1 == 1 and (deployment_1 not in self.env.city.neighborhoods[location_1].current_deployments
                                    or deployment_1 == 0):
                self.next['text'] = "Invalid input for removal"
                self.next['fg'] = "red"
            elif self.ar2 == 1 and (deployment_2 not in self.env.city.neighborhoods[location_2].current_deployments
                                    or deployment_2 == 0):
                self.next['text'] = "Invalid input for removal"
                self.next['fg'] = "red"
            else:
                self.update()




    # update the GUI to next step
    def update(self):
        # self.env.print_player_action_selections()
        location_1 = int(self.loc1.get())
        deployment_1 = int(self.dep1.get())
        location_2 = int(self.loc2.get())
        deployment_2 = int(self.dep2.get())
        actions = self.env.encode_raw_action(add_1=self.ar1,
                                             location_1=LOCATIONS(location_1),
                                             deployment_1=DEPLOYMENTS(deployment_1),
                                             add_2=self.ar2,
                                             location_2=LOCATIONS(location_2),
                                             deployment_2=DEPLOYMENTS(deployment_2))
        observation, reward, done, info = self.env.step(actions)

        self.neighborhoods, self.fear, self.resources, self.orig_alive, self.orig_dead, self.score, self.total_score = self.env.city.getNeiborhoods()

        # Write action and stuff out to disk.
        data_to_log = {
            'game_id': str(self.GAME_ID),
            'step': self.turn,
            'actions': actions,
            'reward': reward,
            'game_done': done,
            'game_info': {k.replace('.', '_'): v for (k, v) in info.items()},
            'raw_state': observation
        }
        with open(self.DATA_LOG_FILE_NAME, 'a') as f_:
            f_.write(json.dumps(data_to_log) + '\n')

        # Update counter
        self.turn += 1
        if done:
            self.quit()

        # self.env.render(mode='human')
        self.create_widgets()

    def getDeps(self):
        deps = ["None", "Quarantine: Open", "Quarantine: Fenced", "Bite Center: Disinfect"]
        deps.append("Bite Center: Amputate")
        deps.append("Zombie Cure Center: FDA Approved")
        deps.append("Zombie Cure Center: Experimental")
        deps.append("Optional Flu Vaccine")
        deps.append("Mandatory Flu Vaccine")
        deps.append("Kiln: With Oversight")
        deps.append("Kiln: No Questions Asked")
        deps.append("Broadcast: Don't Panic")
        deps.append("Broadcast: Call to Arms")
        deps.append("Sniper Tower: Professional")
        deps.append("Sniper Tower: Free Range")
        deps.append("Pheromones: Brains")
        deps.append("Pheromones: Meat")
        deps.append("BSL-4 Lab: Regulated")
        deps.append("BSL-4 Lab: Unregulated")
        deps.append("Rally Point: PSA")
        deps.append("Rally Point: Evacuation")
        deps.append("Firebomb: Useless")
        deps.append("Firebomb: Barrage")
        deps.append("Social Distancing: Signs")
        deps.append("Social Distancing: Celebrity Recommendation")
        deps.append("Flu Testing Center: Optional")
        deps.append("Flu Testing Center: Mandatory")
        deps.append("Supply Depot")
        deps.append("Factory")
        deps.append("Volunteer Recruitment")
        dep_str = ""
        for i in range(len(deps)):
            if i == 29:
                dep_str += "{0} - {1}".format(i, deps[i])
            else:
                dep_str += "{0} - {1}\n".format(i, deps[i])
        return dep_str
