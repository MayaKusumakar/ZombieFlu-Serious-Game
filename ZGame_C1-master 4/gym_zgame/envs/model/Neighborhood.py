import random
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS
from gym_zgame.envs.enums.NPC_STATES import NPC_STATES_DEAD, NPC_STATES_ZOMBIE, NPC_STATES_FLU
from gym_zgame.envs.model.NPC import NPC
import json


class Neighborhood:

    def __init__(self, id, location, adj_locations, num_init_npcs, city, config_file = 'city_config.json'):

        self.FILENAME = config_file
        self.city = city
        self.id = id
        self.location = location
        self.NPCs = []
        self.num_npcs = len(self.NPCs)
        self.num_alive = 0
        self.num_dead = 0
        self.num_ashen = 0
        self.num_human = 0
        self.num_zombie_bitten = 0
        self.num_zombie = 0
        self.num_healthy = 0
        self.num_incubating = 0
        self.num_flu = 0
        self.num_immune = 0
        self.num_moving = 0
        self.num_active = 0
        self.num_sickly = 0
        self.baseDensity = random.uniform(0, 2)
        self.current_density = 0
        self.income = 0
        self.sanitation = 0
        self.adj_locations = adj_locations
        self.SPAWN_CHANCES = {}
        self.INCOME_THRSHLD = {}
        self.TRANS_PROBS = {}
        self.SANITATION_CONST = 1
        self._init_config(self.FILENAME)
        self._npc_init(num_init_npcs)
        self.archive_deployments = []
        # Transition probabilities
        self.trans_probs = self.compute_baseline_trans_probs()
        # Keep summary stats up to date for ease

        self.update_summary_stats()
        self.orig_alive, self.orig_dead = self._get_original_state_metrics()

        self.current_deployments = []

    def _init_config(self, filename):
        with open(filename) as file:
            data = json.load(file)
        self.SPAWN_CHANCES.update(data["spawn_chances"])
        self.TRANS_PROBS.update(data["trans_probs"])
        self.SANITATION_CONST = self.TRANS_PROBS['sanitation_const']

    def get_num_npcs(self):
        return len(self.NPCs)

    def add_to_archives(self, dep):
        self.archive_deployments.append(dep)

    def _npc_init(self, num_npcs):
        init_npcs = []
        for _ in range(num_npcs):
            npc = NPC()
            zombie_chance = random.uniform(0, 1)
            flu_chance = random.uniform(0, 1)
            if npc.income > 200000:
                zombie_chance /= self.SPAWN_CHANCES["income_multiplier"]
                flu_chance /= self.SPAWN_CHANCES["income_multiplier"]
            elif npc.income < 100000:
                zombie_chance *= self.SPAWN_CHANCES["income_multiplier"]
                flu_chance *= self.SPAWN_CHANCES["income_multiplier"]
            if zombie_chance >= self.SPAWN_CHANCES["zombie"]:
                npc.state_zombie = NPC_STATES_ZOMBIE.ZOMBIE
            if flu_chance >= self.SPAWN_CHANCES["flu"]:
                npc.state_flu = NPC_STATES_FLU.FLU
            init_npcs.append(npc)
        self.add_NPCs(init_npcs)

    def _get_original_state_metrics(self):
        og_alive = 0
        og_dead = 0
        og_alive += self.num_alive
        og_dead += self.num_dead
        return og_alive, og_dead

    def compute_baseline_trans_probs(self):
        self.update_summary_stats()
        trans_probs = {
            'burial': (self.num_active / self.num_dead) * self.TRANS_PROBS["burial"] if self.num_dead > 0 else 0,  # dead -> ashen
            'recover': self.TRANS_PROBS["burial"],  # flu -> flu immune
            'pneumonia': self.TRANS_PROBS["burial"],  # flu -> dead
            'incubate': self.TRANS_PROBS["burial"],  # incubating -> flu
            'fumes': self.num_dead * self.TRANS_PROBS["burial"],  # healthy -> incubating
            'cough': self.num_flu / self.num_moving if self.num_moving > 0 else 0,  # healthy -> incubating
            'mutate': self.TRANS_PROBS["burial"],  # immune -> healthy
            'turn': self.TRANS_PROBS["burial"],  # zombie bitten -> zombie
            'devour': (self.num_zombie / self.num_moving) * self.TRANS_PROBS["burial"] if self.num_moving > 0 else 0,  # human -> dead
            'bite': (self.num_zombie / self.num_moving) * (1 - self.TRANS_PROBS["burial"]) if self.num_moving > 0 else 0,  # human -> zombie bitten
            'fight_back': self.num_active * self.TRANS_PROBS["burial"],  # zombie -> dead
            'collapse': self.TRANS_PROBS["burial"],  # zombie -> dead
            'rise': self.TRANS_PROBS["burial"]  # dead -> zombie
        }
        trans_probs['fumes'] = min(trans_probs['fumes']/self.sanitation, 1) if self.sanitation > 1 else 0
        trans_probs['cough'] = min(trans_probs['cough']/self.sanitation, 1) if self.sanitation > 1 else 0
        trans_probs['mutate'] = min(trans_probs['mutate'] / self.sanitation, 1) if self.sanitation > 1 else 0
        return trans_probs

    def add_NPC(self, NPC):
        self.NPCs.append(NPC)
        self.update_summary_stats()

    def add_NPCs(self, NPCs):
        self.NPCs.extend(NPCs)
        self.update_summary_stats()

    def remove_NPC(self, NPC):
        if NPC in self.NPCs:
            self.NPCs.remove(NPC)
            self.update_summary_stats()
        else:
            print('WARNING: Attempted to remove NPC that did not exist in neighborhood')

    def remove_NPCs(self, NPCs):
        for NPC in NPCs:
            self.remove_NPC(NPC)

    def clean_all_bags(self):
        for npc in self.NPCs:
            npc.clean_bag(self.location)

    def add_deployment(self, deployment):
        self.current_deployments.append(deployment)
        self.archive_deployments.append(deployment)

    def add_deployments(self, deployments):
        self.current_deployments.extend(deployments)
        self.archive_deployments.extend(deployments)
    
    def remove_deployment(self, deployment):
        self.current_deployments.remove(deployment)
    
    def remove_deployments(self, deployments):
        for d in deployments:
            if d in self.current_deployments:
                self.current_deployments.remove(d)

    def get_current_deps(self):
        deps = self.current_deployments
        dep_values = []
        for dep in deps:
            dep_values.append(dep.value)
        return dep_values

    def get_dep_history(self):
        return self.archive_deployments

    def destroy_deployments_by_type(self, dep_types):
        updated_deps = [dep for dep in self.current_deployments if dep not in dep_types]
        self.current_deployments = updated_deps

    def update_summary_stats(self):
        self.num_npcs = len(self.NPCs)
        num_alive = 0
        num_dead = 0
        num_ashen = 0
        num_human = 0
        num_zombie_bitten = 0
        num_zombie = 0
        num_healthy = 0
        num_incubating = 0
        num_flu = 0
        num_immune = 0
        num_moving = 0
        num_active = 0
        num_sickly = 0
        income = 0
        for npc in self.NPCs:
            if npc.state_dead is NPC_STATES_DEAD.ALIVE:
                num_alive += 1
            if npc.state_dead is NPC_STATES_DEAD.DEAD:
                num_dead += 1
            if npc.state_dead is NPC_STATES_DEAD.ASHEN:
                num_ashen += 1
            if npc.state_zombie is NPC_STATES_ZOMBIE.HUMAN:
                num_human += 1
            if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN:
                num_zombie_bitten += 1
            if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE:
                num_zombie += 1
            if npc.state_flu is NPC_STATES_FLU.HEALTHY:
                num_healthy += 1
            if npc.state_flu is NPC_STATES_FLU.INCUBATING:
                num_incubating += 1
            if npc.state_flu is NPC_STATES_FLU.FLU:
                num_flu += 1
            if npc.state_flu is NPC_STATES_FLU.IMMUNE:
                num_immune += 1
            if npc.moving:
                num_moving += 1
            if npc.active:
                num_active += 1
            if npc.sickly:
                num_sickly += 1

        self.num_alive = num_alive
        self.num_dead = num_dead
        self.num_ashen = num_ashen
        self.num_human = num_human
        self.num_zombie_bitten = num_zombie_bitten
        self.num_zombie = num_zombie
        self.num_healthy = num_healthy
        self.num_incubating = num_incubating
        self.num_flu = num_flu
        self.num_immune = num_immune
        self.num_moving = num_moving
        self.num_active = num_active
        self.num_sickly = num_sickly
        self.update_income()
        self.update_density()
        self.update_sanitation()

        total_count_dead = self.num_alive + self.num_dead + self.num_ashen
        total_count_zombie = self.num_human + self.num_zombie_bitten + self.num_zombie
        total_count_flu = self.num_healthy + self.num_incubating + self.num_flu + self.num_immune
        assert (self.num_npcs == total_count_dead)
        assert (self.num_npcs == total_count_zombie)
        assert (self.num_npcs == total_count_flu)

    def update_income(self):
        total_income = 0
        for npc in self.NPCs:
            if npc.active:
                total_income += npc.income

        self.income = total_income/(100000*self.num_active) if self.num_active > 0 else 0

    def update_sanitation(self):
        income = self.income
        self.sanitation = self.SANITATION_CONST * (income / self.current_density) if self.current_density > 0 else 0

    def update_density(self):
        self.current_density = (9 * self.num_alive / self.city.get_num_npcs()) * self.baseDensity if self.city.get_num_alive() > 0 else self.baseDensity

    def get_data(self):
        self.update_summary_stats()
        neighborhood_data = {'id': self.id,
                             'location': self.location,
                             'num_npcs': self.num_npcs,
                             'num_alive': self.num_alive,
                             'num_dead': self.num_dead,
                             'num_ashen': self.num_ashen,
                             'num_human': self.num_human,
                             'num_zombie_bitten': self.num_zombie_bitten,
                             'num_zombie': self.num_zombie,
                             'num_healthy': self.num_healthy,
                             'num_incubating': self.num_incubating,
                             'num_flu': self.num_flu,
                             'num_immune': self.num_immune,
                             'num_moving': self.num_moving,
                             'num_active': self.num_active,
                             'num_sickly': self.num_sickly,
                             'original_alive': self.orig_alive,
                             'original_dead': self.orig_dead,
                             'deployments': self.current_deployments,
                             'density': self.current_density,
                             'income': self.income,
                             'sanitation': self.sanitation}
        return neighborhood_data


if __name__ == '__main__':
    nb = Neighborhood('CENTER', LOCATIONS.CENTER, (LOCATIONS.N, LOCATIONS.S, LOCATIONS.W, LOCATIONS.E), 10)
    print(nb.num_npcs)
