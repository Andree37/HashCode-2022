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
        skill_assigned = []
        contribs_assigned = set()
        skill_left = {}
        for ks, kv in self.skills.items():
            for lvl in kv:
                if ks not in contribs:
                    return None

                for c in contribs[ks]:
                    if c.name in contribs_assigned or c.project is not None:
                        continue
                    if c.skills.get(ks) and lvl <= c.skills.get(ks):
                        skill_assigned.append([(ks, lvl), c])
                        contribs_assigned.add(c.name)
                        break
                else:
                    if ks in skill_left:
                        skill_left[ks].append(lvl)
                    else:
                        skill_left[ks] = [lvl]

        for ks, kv in skill_left.items():
            for lvl in kv:
                for c in contribs[ks]:
                    if c.name in contribs_assigned or c.project is not None:
                        continue
                    # search if mentor exists
                    for _, mentor in skill_assigned:
                        # if the mentor has the skill and enough value to teach
                        if mentor.skills.get(ks) and mentor.skills.get(ks) > lvl:
                            # if the contributor has -1 skill than required or no skill at all and lvl = 1 which means he has 0 = 1-1
                            if (c.skills.get(ks) and c.skills.get(ks) - 1 == lvl) or (
                                not c.skills.get(ks) and lvl == 1
                            ):
                                skill_assigned.append([(ks, lvl), c])
                                contribs_assigned.add(c.name)
                                break
                else:
                    return None

        if len(skill_assigned) == len(self.skills):
            return skill_assigned

        else:
            return None

    """
    Starts the project, set contributors, start day and the skill each contributor will do.
    """

    def start(self, start_day, skill_assigned):
        self.contributors = [x[1] for x in skill_assigned]
        self.start_day = start_day
        for s, c in skill_assigned:
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


def print_output(projects):
    output = f"{len(projects)}\n"
    for proj in projects:
        output += proj.name + "\n"
        output += " ".join([contrib.name for contrib in proj.contributors]) + "\n"

    print(output)
    with open("outputs/" + sys.argv[1].split(".")[0][6:] + ".out.txt", "w+") as f:
        f.write(output)
    return output


def main():
    projects, contribs = read_from_file(sys.argv[1])

    def heuristic(proj, day):
        late = proj.best_before - (day + proj.duration)
        if late > 0:
            real_score = max(0, proj.score - late)
        else:
            real_score = proj.score

        return real_score

    day = 0

    ignore = set()
    completed_projects = []
    while len(projects) > len(completed_projects) and day < 25:
        projects.sort(key=lambda x: heuristic(x, day))

        for proj in projects:
            if proj.name in ignore:
                continue

            skills_assigned = proj.choose_contributors(contribs)
            if skills_assigned is not None:
                proj.start(day, skills_assigned)
                completed_projects.append(proj)
                ignore.add(proj.name)

        day += 1
        for proj in completed_projects:
            if proj.start_day + proj.duration == day:
                proj.complete_project()

    print_output(completed_projects)


main()
