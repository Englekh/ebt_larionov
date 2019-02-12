import domain_parcer as dp
import task_parcer as tp


class GrounderAns:
    def __init__(self):
        self.tasks = []
        self.init_state = []
        self.types = []


class TreeTask:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 -primitive, 1-compound
        self.methods = []
        self.operator = []


class TreeMethod:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 - line, 1 - parralel
        self.predcond = []
        self.subtasks = []


class TreePred:
    def __init__(self):
        self.name = ""
        self.preds = []


class TreeOperator:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 -primitive, 1-compound
        self.predcond = []
        self.effects = []


def ground_task (task, params, taskDict):
    dic = dict()
    for i in range(len(params)):
        dic[taskDict[task].params[i]] = params[i]
    ans = TreeTask()
    ans.name = task
    if taskDict[task].type == 0:
        ans.name = "doi"
        ans.type = 0
        op = TreeOperator()
        oper = taskDict[task].thigs[0]
        op.name = oper.name
        for pre in oper.precond:
            p = TreePred()
            p.name = pre.name
            for par in pre.params:
                p.preds.append(dic[par])
            op.predcond.append(p)
        for eff in oper.effect:
            p = TreePred()
            p.name = eff.name
            for par in eff.params:
                p.preds.append(dic[par])
            op.effects.append(p)
        ans.operator = op
    else:
        ans.type = 1
        for m in taskDict[task].things:
            n_el = TreeMethod()
            n_el.type = m.type
            for pre in m.precond:
                p = TreePred()
                p.name = pre.name
                for par in pre.params:
                    p.preds.append(dic[par])
                n_el.predcond.append(p)
            for tsk in m.subtask:
                pars = []
                for el in tsk.precond:
                    pars.append(dic[el])
                n_el.subtasks.append(ground_task(tsk.name, pars, taskDict))
            ans.methods.append(n_el)
    return ans


def ground_files(domain_name, task_name):
    parsed_domain = dp.parse_domain(domain_name)
    parsed_task = tp.parse_task(task_name)
    ans = GrounderAns()
    for el in parsed_task.goal:
        ans.tasks.append(ground_task(el.name, el.preds, parsed_domain.tasks))
    ans.types = parsed_domain.types
    ans.axioms = parsed_domain.axioms
    ans.init_state = parsed_task.pred
    return ans


if __name__ == '__main__':
    domain_name = input()
    task_name = input()
    ans = ground_files(domain_name, task_name)

