import gym
import math
from gym_zgame.envs.model.City import City
import json
import numpy as np
import ZGameHumanPlay, ZGameMachinePlay, ZGameMachineTrain
import pandas as pd
import matplotlib.pyplot as plt
import os
from gym_zgame.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS
import seaborn as sns
import matplotlib.gridspec as gridspec

import pandas as pd

class IndividualAnalyzer:

    def __init__(self, filename):
        self.all_data = pd.read_json(filename, lines=True)
        self.all_data = pd.DataFrame(self.all_data)

        self.dep_record = self.all_data['deployments']

        self.games_list = []
        self.game_info = []
        self.DEP_NAMES = {}



    def get_categories(self):
        categories = list(self.all_data.columns)
        print(categories)

    def get_category_data(self, category):
        category_data = self.all_data[category]
        category_data.head()
        print(category_data)

    def get_rewards(self):
        rewards = self.all_data['reward']
        print(rewards)
        return rewards

    # gets frequency of deployment usage
    def get_actions_count(self):
        actions = self.all_data['deployments']
        print(actions)
        actions_count = {}
        i = 0
        for i in range(len(DEPLOYMENTS)):
            actions_count.update({i:0})
        for deployments in actions:
            for dep in deployments:
                if dep in actions_count.keys():
                    actions_count[dep] += 1
        actions_data = pd.DataFrame(actions_count, index=['# of uses'])
        actions_data = pd.DataFrame.sort_index(actions_data, 1)
        dep_names = []
        for dep in DEPLOYMENTS:
            for i in actions_count.keys():
                if i == dep.value:
                    dep_names.append(dep.name)
        y_values = []
        for i in actions_count.values():
            y_values.append(i)
        # plots # of uses of each deployment in one game
        plt.bar(dep_names, y_values)
        plt.xlabel('Deployment used')
        plt.ylabel('# of uses')
        plt.title('Deployment Usage')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

        return actions_count

    def get_dep_counts(self):
        actions = self.dep_record
        # print('hi')
        # print(actions)
        actions_count = {}
        i = 0
        for i in range(len(DEPLOYMENTS)):
            actions_count.update({i: 0})
        for dep_list in actions:
            # print(dep_list)
            for dep in dep_list:
                if dep in actions_count.keys():
                    actions_count[dep] += 1
        return actions_count

    def get_actions_trend(self):
        # fig, axs = plt.subplots(1, sharex=True, sharey=True)
        # plt.suptitle('Deployment Usage Over Time')
        steps = list(range(len(self.all_data['deployments'])))
        actions = self.all_data['deployments']
        print(actions)
        print(self.get_dep_counts())
        # print(actions)
        # print(actions.keys())
        x_vals = steps
        # print(x_vals)
        y_vals_1 = []
        y_vals_2 = []

        for dep_list in actions.values:
            if len(dep_list) == 1:
                dep_list.append(0)
            y_vals_1.append(dep_list[0])
            y_vals_2.append(dep_list[1])



        # axs.scatter(x_vals, y_vals_1)
        # axs.scatter(x_vals, y_vals_2)

        # plt.xlabel('Step Number')
        # plt.ylabel('Deployment Type')

        # start with a square Figure

        fig = plt.figure(figsize=(8, 8))


        # plt.axis('off')
        plt.suptitle('Deployment Usage')


        # Add a gridspec with two rows and two columns and a ratio of 2 to 7 between
        # the size of the marginal axes and the main axes in both directions.
        # Also adjust the subplot parameters for a square plot.
        gs = fig.add_gridspec(2, 2, width_ratios=(7, 2), height_ratios=(2, 7),
                              left=0.12, right=0.9, bottom=0.2, top=1.11,
                              wspace=0.05, hspace=0.05)


        axs = fig.add_subplot(gs[1, 0])

        ax_histy = fig.add_subplot(gs[1, 1], sharey=axs)

        # axs.tick_params(
        #     axis='x',  # changes apply to the x-axis
        #     which='both',  # both major and minor ticks are affected
        #     bottom=False,  # ticks along the bottom edge are off
        #     top=False,  # ticks along the top edge are off
        #     labelbottom=False)  # labels along the bottom edge are off


        axs.set_xlabel('Step Number')
        axs.set_ylabel('Deployment Number')



        # use the previously defined function
        self.scatter_hist(x_vals, y_vals_1, y_vals_2, axs, ax_histy)


        # plt.show()

    def scatter_hist(self, x, y, y2, axs, ax_histy):
        # no labels
        # fig, axs = plt.subplots(1, sharex=True, sharey=True)

        ax_histy.tick_params(axis="y", labelleft=True)
        ax_histy.grid(b=True, which='major', color='#999999', linestyle='-')
        ax_histy.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

        # the scatter plot:
        axs.scatter(x, y)
        axs.scatter(x, y2)

        axs.set_xlim(0, 42)
        axs.set_ylim(0, 30)

        axs.grid(b=True, which='major', color='#999999', linestyle='-')
        # axs.grid(which='both', color='b', linestyle='-', linewidth=1)
        axs.minorticks_on()
        axs.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

        # now determine nice limits by hand:
        binwidth = 0.25
        xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
        lim = (int(xymax / binwidth) + 1) * binwidth

        bins = np.arange(0, lim + binwidth, binwidth)
        ax_histy.hist(y+y2, bins=bins, orientation='horizontal')
        print(y+y2)


        # data = np.column_stack((x_vals, y_vals_1))
        # data2 = np.column_stack((x_vals, y_vals_2))
        # df = pd.DataFrame(data, columns=["x", "y"])
        # df2 = pd.DataFrame(data2, columns=["x", "y"])
        #
        # pal = dict(y_vals_1="seagreen", y_vals_2="gray")
        # g = sns.FacetGrid(df)
        # g.map(plt.scatter, "x_vals", "pal")
        # g.add_legend();
        #
        # sns.jointplot(x="x", y="y", data=df);
        # sns.jointplot(x="x", y="y", data=df2)

        # gs = fig.add_gridspec(2, 2, width_ratios=(7, 2), height_ratios=(2, 7),
        #                       left=0.1, right=0.9, bottom=0.1, top=0.9,
        #                       wspace=0.05, hspace=0.05)
        # ax = fig.add_subplot(gs[1, 0])
        # ax_histx = fig.add_subplot(gs[0, 0], sharex=axs)
        # ax_histy = fig.add_subplot(gs[1, 1], sharey=axs)
        #
        # ax_histx.tick_params(axis=x_vals, labelbottom=True)
        # ax_histy.tick_params(axis=y_vals_1, labelleft=True)
        #
        # # the scatter plot:
        # ax.scatter(x, y)
        #
        # # now determine nice limits by hand:
        # binwidth = 0.25
        # xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
        # lim = (int(xymax / binwidth) + 1) * binwidth
        #
        # bins = np.arange(-lim, lim + binwidth, binwidth)
        # ax_histx.hist(x, bins=bins)
        # ax_histy.hist(y, bins=bins, orientation='horizontal')
        #
        # #
        # #
        # # plt.scatter(x_vals, y_vals, s=100, c='red')
        # # sns.jointplot(x=x_vals, y=y_vals_1, data=plt)



if __name__ == '__main__':
    a = IndividualAnalyzer('machine_log.json')
    # a.get_rewards()
    # a.get_category_data('deployments')
    # a.get_categories()
    # a.get_actions_count()
    a.get_actions_trend()



# import matplotlib.pyplot as plt
# plt.ion()
# class DynamicUpdate():
#     #Suppose we know the x range
#     min_x = 0
#     max_x = 10
#
#     def on_launch(self):
#         #Set up plot
#         self.figure, self.ax = plt.subplots()
#         self.lines, = self.ax.plot([],[], 'o')
#         #Autoscale on unknown axis and known lims on the other
#         self.ax.set_autoscaley_on(True)
#         self.ax.set_xlim(self.min_x, self.max_x)
#         #Other stuff
#         self.ax.grid()
#         ...
#
#     def on_running(self, xdata, ydata):
#         #Update data (with the new _and_ the old points)
#         self.lines.set_xdata(xdata)
#         self.lines.set_ydata(ydata)
#         #Need both of these in order to rescale
#         self.ax.relim()
#         self.ax.autoscale_view()
#         #We need to draw *and* flush
#         self.figure.canvas.draw()
#         self.figure.canvas.flush_events()
#
#     #Example
#     def __call__(self):
#         import numpy as np
#         import time
#         self.on_launch()
#         xdata = []
#         ydata = []
#         for x in np.arange(0,10,0.5):
#             xdata.append(x)
#             ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
#             self.on_running(xdata, ydata)
#             time.sleep(1)
#         return xdata, ydata
#
# d = DynamicUpdate()
# d()




