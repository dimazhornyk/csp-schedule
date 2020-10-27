from display import print_pretty_matrix
from utils import set_up_variables, set_up_domains, get_constraints, classroom_manager, subject_collision_check, \
    groups_collision_check

DOMAINS = "DOMAINS"
VARIABLES = "VARIABLES"
CONSTRAINTS = "CONSTRAINTS"
FAILURE = "FAILURE"


def is_complete(assignment):
    return False not in (assignment.values())


def select_unassigned_variable(variables, assignment):
    for var in variables:
        for slot in var:
            for pair in slot:
                if assignment[pair] is False:
                    return var


def is_consistent(slot, constraints):
    for constraint_violated in constraints:
        if not constraint_violated(slot):
            return False
    return True


def init_assignment(csp):
    assignment = {}
    for pair in csp[DOMAINS]:
        assignment[pair] = False

    return assignment


def MRV(assignment, _):
    unused_classes, _ = get_unused_classes_and_teachers(assignment)
    sorted_unused_classes = sorted(unused_classes, key=lambda el: el.subject.total_groups)
    return sorted_unused_classes[0]


def power_heuristic(assignment, _):
    unused_classes, teachers_map = get_unused_classes_and_teachers(assignment)
    sorted_unused_classes = sorted(unused_classes, key=lambda elem: teachers_map[elem.subject.teacher])
    return sorted_unused_classes[0]


def least_constraining_value(assignment, _):
    unused_classes, teachers_map = get_unused_classes_and_teachers(assignment)
    sorted_unused_classes = sorted(unused_classes, key=lambda elem: teachers_map[elem.subject.teacher], reverse=True)
    return sorted_unused_classes[0]


def constraint_propagation(assignment, slot):
    unused_classes, _ = get_unused_classes_and_teachers(assignment)
    # set classrom each one in unused_classes if no classroom found then skip class
    domain = [*unused_classes, *slot]
    # domain->filter each constraint return domain' => new slot



def forward_checking(assignment, slot):
    unused_classes, _ = get_unused_classes_and_teachers(assignment)
    appropriate_classes = list(
        filter(lambda c: subject_collision_check([*slot, c]) and groups_collision_check([*slot, c]), unused_classes))
    return appropriate_classes[0]


def get_unused_classes_and_teachers(assignment):
    unused_classes = list(filter(lambda key: not assignment[key], assignment))
    teachers_map = {}
    for c in unused_classes:
        if c.subject.teacher in teachers_map:
            teachers_map[c.subject.teacher] += 1
        else:
            teachers_map[c.subject.teacher] = 1
    return unused_classes, teachers_map


def backtracking(assignment, csp, heuristic, num_of_epochs):
    get_next_slot, set_slot = get_next_time_slot(csp[VARIABLES])
    get_classroom = classroom_manager()

    for i in range(num_of_epochs):
        if is_complete(assignment):
            return csp[VARIABLES], i

        slot = get_next_slot()
        class_ = heuristic(assignment, slot)
        classroom = get_classroom(slot, class_.subject.num_of_students)
        slot.append(class_)
        class_.classroom = classroom

        if is_consistent(slot, csp[CONSTRAINTS]):
            assignment[class_] = True
            set_slot(slot)
        else:
            assignment[class_] = False
    return csp[VARIABLES], num_of_epochs


def get_next_time_slot(variables):
    i, j = 0, 0

    def update_indexes_return_value():
        nonlocal i, j
        if i == 5:
            i = 0
        if j == 6:
            j = 0
        res = variables[i][j].copy()
        i, j = i + 1, j + 1
        return res

    def set_time_slot(value):
        nonlocal i, j
        variables[i - 1][j - 1] = value

    return update_indexes_return_value, set_time_slot


csp = {
    VARIABLES: set_up_variables(),
    DOMAINS: set_up_domains(),
    CONSTRAINTS: get_constraints()
}
for_pretty, epochs = backtracking(assignment=init_assignment(csp), csp=csp, heuristic=forward_checking,
                                  num_of_epochs=1000)
print_pretty_matrix(for_pretty)
print(f'Num of epochs: {epochs}')
