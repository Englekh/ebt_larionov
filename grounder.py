import domain_parcer as dp
import task_parcer as tp

class AnsInfo:
    def __init__(self):
        self.types = dict()
        self.req = set()
        self.pred = set()
        self.tasks = dict()
        self.axioms = set()
        self.goal = ""


class PredDisc:
    def __init__(self, name):
        self.name = name
        self.subtype = set()
        self.elements = set()

    def __str__(self):
        return "( predicate: " + self.name + "pattern: " + str(self.subtype) + "active: " + str(self.elements) + ")"

    def __repr__(self):
        return "( predicate: " + self.name + "pattern: " + str(self.subtype) + "active: " + str(self.elements) + ")"


class TypeDisc:
    def __init__(self, name):
        self.name = name
        self.subtype = set()
        self.elements = set()

    def __str__(self):
        return "( type: " + self.name + "subtype: " + str(self.subtype) + "active: " + str(self.elements) + ")"

    def __repr__(self):
        return "( type: " + self.name + "subtype: " + str(self.subtype) + "active: " + str(self.elements) + ")"


def ground_files(domain_name, task_name):
    parsed_domain = dp.parse_domain(domain_name)
    parsed_task = tp.parse_task(task_name)
    ans = AnsInfo
    ready_predicates = dict();
    # all_predicates
    for pred in parsed_domain.pred:
        ready_predicates[pred.name] = PredDisc(pred.name)
        ready_predicates[pred.name].subtype = pred.params
        if parsed_task.pred.get(pred.name):
            ready_predicates[pred.name].elements = parsed_task.pred[pred.name]
        else:
            ready_predicates[pred.name].elements = set()
    fin_obj = dict()
    for obj in parsed_task.objects:
        fin_obj[obj] = TypeDisc(obj)
        fin_obj[obj].subtype = parsed_domain.types[obj]
        fin_obj[obj].elements = parsed_task.objects[obj]
    ans.types = fin_obj
    ans.pred = ready_predicates
    ans.goal = parsed_task.goal
    ans.tasks = parsed_domain.tasks
    ans.req = parsed_domain.req
    ans.axioms = parsed_domain.axioms
    return ans

if __name__ == '__main__':
    domain_name = input()
    task_name = input()
    ans = ground_files(domain_name, task_name)
    print("types: ", ans.types)
    print("predicates: ", ans.pred)
    print("goal: ", ans.goal)
    print("tasks: ", ans.tasks)
    print("req:",  ans.req)
    print("axioms:", ans.axioms)

