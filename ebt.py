import grounder as gr
import HTN as ht
import sys
import copy


def check_union (preds1, preds2):
    for el1 in preds1:
        for el2 in preds2:
            if el1.name == el2.name:
                counter = 0
                for i in range(len(el1.params)):
                    if el1.params[i] != el2.params[i]:
                        counter += 1
                if counter == 0:
                    return True
    return False


class EbtElem:
    def __init__(self):
        self.name = ""
        self.type = 0
        # 0 - none, 1 - line, 2 - paralel
        self.params = []
        self.precond = ([], [])
        self.effect = ([], [])
        self.arch = 0
        # 0 - start , 1 end

    def __str__(self):
        return "name " + str(self.name) + ":" + str(self.params) + str(self.type) + str(self.arch) + "\n" \
               + str(self.precond) + " " + str(self.effect) + "\n"

    def __repr__(self):
        return "name " + str(self.name) + ":" + str(self.params) + str(self.type) + str(self.arch) + "\n" \
               + str(self.precond) + " " + str(self.effect) + "\n"




def addlist(list, task):
    if task.type == 0:
        n_elem = EbtElem()
        n_elem.name = task.name
        n_elem.params = task.params
        n_elem.precond = task.precond
        n_elem.effect = task.effect
        list.append(n_elem)
    else:
        n_elem = EbtElem()
        n_elem.type = 1
        n_elem.name = task.name
        n_elem.params = task.params
        n_elem.precond = task.precond
        n_elem.effect = ([], [])
        list.append(n_elem)
        for sub in task.subtasks:
            addlist(list, sub)
        n_elem = EbtElem()
        n_elem.type = 1
        n_elem.name = task.name
        n_elem.params = []
        n_elem.precond = task.subtasks[len(task.subtasks) - 1].effect
        n_elem.effect = ([], [])
        n_elem.arch = 1
        list.append(n_elem)


def check_ax1(state, elem2):
    if (ht.check_all_precond(state, elem2.precond[0])) and\
            not (ht.check_any_precond(state, elem2.precond[1])):
        return True
    return False


def check_ax2(state, elem1, elem2):
    n_state = copy.deepcopy(state)
    ht.apply_effects(n_state, elem2.effect[0])
    ht.apply_not_effects(n_state, elem2.effect[1])
    if (ht.check_all_precond(n_state, elem1.precond[0])) and\
            not (ht.check_any_precond(n_state, elem1.precond[1])):
        return True
    return False


def check_ax3(elem1, elem2):
    if not (check_union(elem1.precond[0], elem2.precond[1])) and \
            not (check_union(elem1.precond[1], elem2.precond[0])):
        return True
    return False


def check_axes(state, elem1, elem2):
    print("ax_check\n", elem1, elem2, state, "\n===========================================\n", check_ax1(state, elem2), check_ax2(state, elem1, elem2), check_ax3(elem1, elem2))
    if check_ax1(state, elem2) and check_ax2(state, elem1, elem2) and check_ax3(elem1, elem2):
        return True
    return False


def addElem(end, elem, state):
    buf = []
    flag = True
    if (elem.type == 2 and elem.arch == 1) or (elem.type == 1 and elem.arch == 1):
        end.append(elem)
        n_state = copy.deepcopy(state[len(state) - 1])
        ht.apply_effects(n_state, elem.effect[0])
        ht.apply_not_effects(n_state, elem.effect[1])
        state.append(n_state)
    else:
        while len(end) > 0 and flag:
            n_elem = end[len(end) - 1]
            st = state[len(state) - 2]
            if check_axes(st, n_elem, elem):
                buf.append(n_elem)
                end.pop()
                state.pop()
            else:
                flag = False

        if len(buf) > 0:
            el = buf.pop()
            if (el.type == 2) and (el.arch == 0):
                end.append(el)
                n_state = copy.deepcopy(state[len(state) - 1])
                ht.apply_effects(n_state, el.effect[0])
                ht.apply_not_effects(n_state, el.effect[1])
                state.append(n_state)

                end.append(elem)
                n_state = copy.deepcopy(state[len(state) - 1])
                ht.apply_effects(n_state, elem.effect[0])
                ht.apply_not_effects(n_state, elem.effect[1])
                state.append(n_state)
                precs = elem.effect

                el = buf.pop()
                while not (el.type == 2) and (el.arch == 1):
                    end.append(el)
                    n_state = copy.deepcopy(state[len(state) - 1])
                    ht.apply_effects(n_state, el.effect[0])
                    ht.apply_not_effects(n_state, el.effect[1])
                    state.append(n_state)
                    el = buf.pop()

                el.precond[0].extend(precs[0])
                el.precond[1].extend(precs[1])
                end.append(el)
                n_state = copy.deepcopy(state[len(state) - 1])
                ht.apply_effects(n_state, el.effect[0])
                ht.apply_not_effects(n_state, el.effect[1])
                state.append(n_state)

            else:
                n_state = copy.deepcopy(state[len(state) - 1])
                n = EbtElem()
                n.type = 2
                n.arch = 0
                n.name = "paralel_start"
                end.append(n)
                state.append(n_state)

                end.append(elem)
                n_state = copy.deepcopy(state[len(state) - 1])
                ht.apply_effects(n_state, elem.effect[0])
                ht.apply_not_effects(n_state, elem.effect[1])
                state.append(n_state)

                end.append(el)
                n_state = copy.deepcopy(state[len(state) - 1])
                ht.apply_effects(n_state, el.effect[0])
                ht.apply_not_effects(n_state, el.effect[1])
                state.append(n_state)

                n_state = copy.deepcopy(state[len(state) - 1])
                n = EbtElem()
                n.type = 2
                n.arch = 1
                n.name = "paralel_end"
                end.append(n)
                state.append(n_state)

            while len(buf) > 0:
                n_elem = buf.pop()
                end.append(n_elem)
                n_state = copy.deepcopy(state[len(state) - 1])
                ht.apply_effects(n_state, n_elem.effect[0])
                ht.apply_not_effects(n_state, n_elem.effect[1])
                state.append(n_state)
        else:
            end.append(elem)
            n_state = copy.deepcopy(state[len(state) - 1])
            ht.apply_effects(n_state, elem.effect[0])
            ht.apply_not_effects(n_state, elem.effect[1])
            state.append(n_state)


def make_ebt(list, init):
    state = []
    state.append(init)
    end = []
    # print(list)
    while len(list) > 0:
            addElem(end, list.pop(0), state)
    return end


if __name__ == '__main__':
    domain_name = sys.argv[1]
    task_name = sys.argv[2]
    ans = gr.ground_files(domain_name, task_name)
    ini = copy.deepcopy(ans.init_state)
    root = ht.ansTask()
    for task in ans.tasks:
        e = ht.htn_search(ini, task)[2];
        root.subtasks.append(e)
        root.precond[0].extend(e.precond[0])
        root.precond[1].extend(e.precond[1])
    root.name = "MAIN"
    root.type = 1
    list = []
    addlist(list, root)
    file = open("output.txt", "w")
    print(list)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    res = make_ebt(list, ans.init_state)
    s = ""
    isPar = 0
    for el in res:
        if el.type == 0:
            file.write(s + str(el.name) + " " + str(el.params) + "\n")
        elif el.type == 1:
            if el.arch == 0:
                file.write(s + str(el.name) + " " + str(el.params) + " {\n")
                s += "\t"
            else:
                s = s[:-1]
                file.write(s + "}\n")
        else:
            if el.arch == 0:
                file.write(s + "||" + "\n")
                s += "=\t"
            else:
                s = s[:-2]
