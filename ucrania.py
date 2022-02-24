from astar import AStar
from copy import deepcopy
import sys


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.project = None
        self.skill = None

    def can_participate(self, project):
        for k, v in project.skills.items():
            return self.skills.get(k) and v >= self.skills.get(k)

    def add_project(self, project, skill):
        if self.can_participate(project) and not self.project:
            self.project = project
            self.skill = skill

    def complete_project(self):
        skill_name, level = self.skill
        if skill_name not in self.skills:
            self.skills[skill_name] = 1

        elif level >= self.skills[skill_name]:
            self.skills[skill_name] += 1

        self.project = None
        self.skill = None


class Project:
    def __init__(self, name, duration, score, best_before, skills):
        self.name = name
        self.start_day = -1
        self.duration = duration
        self.score = score
        self.best_before = best_before
        self.skills = skills
        self.contributors = []

    def learning_scale(self, contributor, skill):
        total = 0
        skill_name, level = self.skill
        if skill_name not in self.skills or level >= self.skills[skill_name]:
            total += 1

        return total

    def complete_project(self):
        for c in self.contributors:
            c.complete_project()

    def in_time(self, day):
        return self.best_before >= day + self.duration

    def choose_contributors(self, contribs):
        skill_assigned = {}
        skill_left = {}
        for ks, kv in self.skills.items():
            for lvl in kv:
                if ks not in contribs:
                    return None

                for c in contribs[ks]:
                    if c in skill_assigned.values() or c.project is not None:
                        continue
                    if c.skills.get(ks) and lvl <= c.skills.get(ks):
                        skill_assigned[(ks, lvl)] = c
                        break
                else:
                    if ks in skill_left:
                        skill_left[ks].append(lvl)
                    else:
                        skill_left[ks] = [lvl]

        for ks, kv in skill_left.items():
            for lvl in kv:
                for c in contribs[ks]:
                    if c in skill_assigned.values() or c.project is not None:
                        continue
                    # search if mentor exists
                    for mentor in skill_assigned.values():
                        # if the mentor has the skill and enough value to teach
                        if mentor.skills.get(ks) and mentor.skills.get(ks) > lvl:
                            # if the contributor has -1 skill than required or no skill at all and lvl = 1 which means he has 0 = 1-1
                            if (c.skills.get(ks) and c.skills.get(ks) - 1 == lvl) or (
                                not c.skills.get(ks) and lvl == 1
                            ):
                                skill_assigned[(ks, lvl)] = c
                                break
                else:
                    skill_left[ks] = lvl
        if len(skill_assigned.keys()) == len(self.skills):
            return skill_assigned

        else:
            return None

    """
    Starts the project, set contributors, start day and the skill each contributor will do.
    """

    def start(self, start_day, skill_assigned):
        self.contributors = skill_assigned.values()
        self.start_day = start_day
        for s, c in skill_assigned.items():
            c.skill = s
            c.project = self


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level


def read_from_file(input_path):
    with open(input_path) as f:
        lines = f.readlines()

        n_contrib, n_proj = lines[0].strip().split(" ")
        n_contrib = int(n_contrib)
        n_proj = int(n_proj)
        projects = []
        contribs = []

        i = 1
        while i < len(lines) and n_contrib != 0:

            line = lines[i]
            name, n_skills = line.strip().split(" ")
            n_skills = int(n_skills)
            skills = {}

            for skill in lines[i + 1 : i + 1 + n_skills]:
                skill_name, level = skill.strip().split(" ")
                skills[skill_name] = int(level)

            contribs.append(Contributor(name, skills))
            n_contrib -= 1

            i += n_skills + 1

        while i < len(lines) and n_proj != 0:
            line = lines[i]
            name, duration, score, best_before, n_skills = line.strip().split(" ")
            n_skills = int(n_skills)
            skills = {}

            for skill in lines[i + 1 : i + 1 + n_skills]:
                skill_name, level = skill.strip().split(" ")
                level = int(level)
                if skill_name in skills:
                    skills[skill_name].append(level)
                else:
                    skills[skill_name] = [level]

            projects.append(
                Project(name, int(duration), int(score), int(best_before), skills)
            )
            n_proj -= 1

            i += n_skills + 1

        contribs_dict = {}
        for c in contribs:
            for skill in c.skills:
                if skill in contribs_dict:
                    contribs_dict[skill].append(c)
                else:
                    contribs_dict[skill] = [c]

        return projects, contribs_dict


class Context:
    def __init__(self, time_step, collaborators, projects, new_skills, new_score, new_busy_developers):
        self.time_step = time_step
        self.collaborators = collaborators
        self.projects = projects
        self.new_skills = new_skills
        self.new_score = new_score
        self.new_busy_developers = new_busy_developers


class Solver(AStar):
    def __init__(self):
        pass


    def heuristic_cost_estimate(self, current, goal):
        # number of skill improvements that would be had if current context was chosen
        current_skills_to_gain = - current.new_skills
        current_skills_to_gain_scale_factor = (goal.time_step - current.time_step / goal.time_step)
        current_skills_to_gain *= current_skills_to_gain_scale_factor

        # amount of score to be gained if current context was chosen
        current_score_to_gain = - current.new_score

        # number of collaborators that would have been busy if current context was chosen
        current_busy_collaborators = - current.new_busy_developers
        
        return  0.80 * current_skills_to_gain + \
                0.15 * current_score_to_gain + \
                0.05 * current_busy_collaborators


    def distance_between(self, n1, n2):
        return 1


    def neighbors(self, node):
        neighbors = []
        next_time_step = node.time_step + 1

        # criar um context para cada assignment possivel de projetos
        for a in None:
            new_collaborators = deepcopy(node.collaborators)
            new_projects = deepcopy(node.projects)

            # make transition

            # stuff used in heuristic
            new_skills = 
            new_score = 
            new_busy_collaborators = 

            new_context = Context(
                next_time_step,
                new_collaborators,
                new_projects,
                new_skills,
                new_score,
                new_busy_collaborators
            )

            neighbors.append(new_context)
        
        return neighbors
    

    def is_goal_reached(self, current, goal):
        return len(current.projects) == 0 and current.calculate_score_to_gain() > max_activity_score


def solve_ukrain0e(collaborators, projects):
    start = Context(0, collaborators, projects, float("-inf"), float("-inf"), float("-inf"))
    goal = Context(float("inf"), collaborators, projects, float("inf"), float("inf"), float("inf"))
    path = list(Solver().astar(start, goal))


projects, contribs = read_from_file(sys.argv[1])
max_activity_score = 1
#solve_ukraine()
print("why are u like dis")
