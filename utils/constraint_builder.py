from packages.constraint import Constraint
from utils import constants


def generate_all_pairs(elements):
    if len(elements) < 2:
        return []
    elif len(elements) == 2:
        return [(elements[0], elements[1])]
    else:
        new_pairs = []
        for elt in elements[1:]:
            new_pairs.append((elements[0], elt))
        return generate_all_pairs(elements[1:]) + new_pairs


def difference_constraints_builder(agents_number: int, meetings_number: int, agent_meetings: dict) -> list:
    difference_constraints = []
    for agent in range(1, agents_number + 1):
        variable_list = []
        for meeting in range(1, meetings_number + 1):
            variable = agent_meetings.get("a{}_m{}".format(agent, meeting))
            if variable is not None:
                variable_list.append(variable.name)
        for p in generate_all_pairs(variable_list):
            difference_constraints.append(Constraint(str(p[0]) + "-" + str(p[1]), constants.DIFFERENCE_CONSTRAINT,
                                                     list(p)))
    return difference_constraints


def equality_constraints_builder(agents_number: int, meetings_number: int, agent_meetings: dict) -> list:
    equality_constraints = []
    for meeting in range(1, meetings_number + 1):
        variable_list = []
        for agent in range(1, agents_number + 1):
            variable = agent_meetings.get("a{}_m{}".format(agent, meeting))
            if variable is not None:
                variable_list.append(variable.name)
        for p in generate_all_pairs(variable_list):
            equality_constraints.append(Constraint(str(p[0]) + "-" + str(p[1]), constants.EQUALITY_CONSTRAINT, list(p)))
    return equality_constraints


def constraint_builder(agents_number: int, meetings_number: int, agent_meetings: dict):
    return equality_constraints_builder(agents_number, meetings_number, agent_meetings) + difference_constraints_builder(agents_number, meetings_number, agent_meetings)
