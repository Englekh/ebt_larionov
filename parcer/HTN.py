import grounder as gr
import sys
import copy


class ansTask:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 -primitive, 1-compound
        self.subtasks = []
        self.params = []
        self.precond = ([], [])
        self.effect = ([], [])
        self.arch = 0
        # 0 - line, 1 - parralel

    def __str__(self):
        if self.type == 1:
            return "task " + str(self.name) + ":" + str(self.params) + "\nprecond: " + str(self.precond) + \
                   "\neffect:" + str(self.effect) + ' subtasks:\n' + str(self.subtasks) + "\n"
        else:
            return "oper: " + str(self.name) + ":" + str(self.params) + "\nprecond: " + str(self.precond) + \
                   "\neffect:" + str(self.effect) + "\n"

    def __repr__(self):
        if self.type == 1:
            return "task " + str(self.name) + ":" + str(self.params) + "\nprecond: " + str(self.precond) + \
                   "\neffect:" + str(self.effect) + ' subtasks:\n' + str(self.subtasks) + "\n"
        else:
            return "oper: " + str(self.name) + ":" + str(self.params) + "\nprecond: " + str(self.precond) + \
                   "\neffect:" + str(self.effect) + "\n"


def check_precond(dic, oper):
    if not (dic.get(oper.name)):
        print("key not found", oper.name)
        return False
    for i in range(len(dic[oper.name])):
        counter = 0
        for j in range(len(dic[oper.name][i])):
            if dic[oper.name][i][j] != oper.params[j]:
                counter += 1
        if counter == 0:
            return True
    return False


def check_all_precond(dic, opers):
    for oper in opers:
        if not check_precond(dic, oper):
            return False
    return True


def check_any_precond(dic, opers):
    for oper in opers:
        if check_precond(dic, oper):
            return True
    return False


def apply_not_effects(dic, opers):
    for oper in opers:
        i = 0
        if not dic.get(oper.name):
            dic[oper.name] = []
        ran = len(dic[oper.name])
        while i < ran:
            counter = 0
            for j in range(len(dic[oper.name][i])):
                if dic[oper.name][i][j] != oper.params[j]:
                    counter += 1
            if counter == 0:
                dic[oper.name].pop(i)
                ran -= 1
            else:
                i += 1


def apply_effects(dic, opers):
    for oper in opers:
        i = 0
        if not dic.get(oper.name):
            dic[oper.name] = []
        ran = len(dic[oper.name])
        flag = 0
        while i < ran:
            counter = 0
            for j in range(len(dic[oper.name][i])):
                if dic[oper.name][i][j] != oper.params[j]:
                    counter += 1
            if counter == 0:
                flag = 1
            i += 1
        if flag == 0:
            dic[oper.name].append(oper.params)


def htn_search_m(predicates, method):
    buf = []
    sub = []
    i = 0
    while (0 <= i) and (i < len(method.subtasks)):
        buf.append(copy.deepcopy(predicates))
        ans = htn_search(predicates, method.subtasks[i])
        if ans[0]:
            sub.append(ans[2])
            buf.append(ans[1])
            i += 1
        else:
            i -= 1
            sub.pop()
            predicates = buf.pop()
    if i < 0:
        return False, [], []
    else:
        return True, predicates, sub


def htn_search(predicates, task):
    first = 0
    if task.run == 0:
        task.run = 1
    else:
        first = 1
    if task.type == 0:
        if first == 1:
            task.run = 0
            return False, [], []
        if check_all_precond(predicates, task.operator.t_predcond) and \
                not check_any_precond(predicates, task.operator.f_predcond):
            apply_effects(predicates, task.operator.t_effects)
            apply_not_effects(predicates, task.operator.f_effects)
            ans = ansTask()
            ans.name = task.operator.name
            ans.precond = (task.operator.t_predcond, task.operator.f_predcond)
            ans.effect = (task.operator.t_effects, task.operator.f_effects)
            ans.type = 0
            ans.params = task.params
            return True, predicates, ans
        else:
            return False, [], []
    counter = 0
    i = 0
    while i < len(task.methods):
        if check_all_precond(predicates, task.methods[i].t_predcond) and \
                not check_any_precond(predicates, task.methods[i].f_predcond):
            counter += 1
            if task.run == counter:
                mAns = htn_search_m(predicates, task.methods[i])
                if mAns[0]:
                    ans = ansTask()
                    ans.name = task.methods[i].name
                    ans.precond = (task.methods[i].t_predcond, task.methods[i].f_predcond)
                    ans.params = task.params
                    ans.type = 1
                    ans.subtasks = mAns[2]
                    ans.arch = task.methods[i].type
                    return True, mAns[1], ans
                task.run += 1
        i += 1
    task.run = 0
    return False, [], []


if __name__ == '__main__':
    domain_name = sys.argv[1]
    task_name = sys.argv[2]
    ans = gr.ground_files(domain_name, task_name)
    for task in ans.tasks:
        print(htn_search(ans.init_state, task)[2])
