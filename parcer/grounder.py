import domain_parcer as dp
import task_parcer as tp
import sys


class GrounderAns:
    def __init__(self):
        self.tasks = []
        self.init_state = []
        self.types = []
        self.axioms = []


class TreeTask:
    def __init__(self):
        self.run = 0
        self.name = ""
        self.type = 0
        # 0 -primitive, 1-compound
        self.methods = []
        self.operator = []
        self.params = []

    def __str__(self):
        return "task " + str(self.name) + ' methods:\n' + str(self.methods)

    def __repr__(self):
        return "task " + str(self.name) + " methods:\n" + str(self.methods)


class TreeMethod:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 - line, 1 - parralel
        self.f_predcond = []
        self.t_predcond = []
        self.subtasks = []

    def __str__(self):
        return "method " + str(self.name) + ' subtasks: \n' + str(self.subtasks)

    def __repr__(self):
        return "method " + str(self.name) + ' subtasks: \n' + str(self.subtasks)


class TreePred:
    def __init__(self):
        self.name = ""
        self.params = []

    def __str__(self):
        return str(self.name) + ': ' + str(self.params)

    def __repr__(self):
        return str(self.name) + ": " + str(self.params)


class TreeOperator:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 -primitive, 1-compound
        self.f_predcond = []
        self.t_predcond = []
        self.f_effects = []
        self.t_effects = []

    def __str__(self):
        return "operator " + str(self.name) + '\n'

    def __repr__(self):
        return "operator " + str(self.name) + '\n'


def ground_task(task, params, taskDict):
    dic = dict()
    ans = TreeTask()
    for i in range(len(params)):
        dic[taskDict[task].params[i].name] = params[i]
        ans.params.append(params[i])
    ans.name = task
    if taskDict[task].type == 0:
        ans.type = 0
        op = TreeOperator()
        oper = taskDict[task].things[0]
        op.name = oper.name

        for pre in oper.precond[0]:
            p = TreePred()
            p.name = pre.name
            for par in pre.params:
                p.params.append(dic[par])
            op.t_predcond.append(p)

        for pre in oper.precond[1]:
            p = TreePred()
            p.name = pre.name
            for par in pre.params:
                p.params.append(dic[par])
            op.f_predcond.append(p)

        for eff in oper.effect[0]:
            p = TreePred()
            p.name = eff.name
            for par in eff.params:
                p.params.append(dic[par])
            op.t_effects.append(p)

        for eff in oper.effect[1]:
            p = TreePred()
            p.name = eff.name
            for par in eff.params:
                p.params.append(dic[par])
            op.f_effects.append(p)

        ans.operator = op
    else:
        ans.type = 1
        for m in taskDict[task].things:
            n_el = TreeMethod()
            n_el.name = m.name
            n_el.type = m.type
            for pre in m.precond[0]:
                p = TreePred()
                p.name = pre.name
                for par in pre.params:
                    p.params.append(dic[par])
                n_el.t_predcond.append(p)
            for pre in m.precond[1]:
                p = TreePred()
                p.name = pre.name
                for par in pre.params:
                    p.params.append(dic[par])
                n_el.f_predcond.append(p)
            for tsk in m.subtask:
                pars = []
                for el in tsk.params:
                    pars.append(dic[el])
                n_el.subtasks.append(ground_task(tsk.name, pars, taskDict))
            ans.methods.append(n_el)
    return ans


def ground_files(domain_name, task_name):
    parsed_domain = dp.parse_domain(domain_name)
    parsed_task = tp.parse_task(task_name)
    ans = GrounderAns()
    for el in parsed_task.goal:
        ans.tasks.append(ground_task(el.name, el.params, parsed_domain.tasks))
    ans.types = parsed_domain.types
    ans.axioms = parsed_domain.axioms
    ans.init_state = parsed_task.pred
    for pred in parsed_domain.pred:
        if not ans.init_state.get(pred.name):
           ans.init_state[pred.name] = []
    return ans


if __name__ == '__main__':
    domain_name = sys.argv[1]
    task_name = sys.argv[2]
    ans = ground_files(domain_name, task_name)

