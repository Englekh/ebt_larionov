import grounder as gr
import HTN as ht
import sys
import copy

elId = 0

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
        self.processor = 0
        # 0 - line, 1 - parralel
        self.type = 0
        # 0 - none, 1 - line, 2 - paralel
        self.params = []
        self.precond = ([], [])
        self.effect = ([], [])
        self.arch = 0
        # 0 - start , 1 end
        self.id = -1

    def __str__(self):
        return "name " + str(self.name) + ":" + str(self.params) + str(self.type) + str(self.arch) + "\n" \
               + str(self.precond) + " " + str(self.effect) + "\n"

    def __repr__(self):
        return "name " + str(self.name) + ":" + str(self.params) + str(self.type) + str(self.arch) + "\n" \
               + str(self.precond) + " " + str(self.effect) + "\n"


def apply_new(ans_ef, new_ef):
    # true to true
    for pred in new_ef[0]:
        counter = 0
        for el in ans_ef[0]:
            if pred.name == el.name:
                i = 0
                flag = 0
                while i < len(pred.params):
                    if el.params[i] != pred.params[i]:
                        flag = 1
                    i += 1
                if flag == 0:
                    counter = 1
        if counter == 0:
            ans_ef[0].append(pred)

    # false to false
    for pred in new_ef[1]:
        counter = 0
        for el in ans_ef[1]:
            if pred.name == el.name:
                i = 0
                flag = 0
                while i < len(pred.params):
                    if el.params[i] != pred.params[i]:
                        flag = 1
                    i += 1
                if flag == 0:
                    counter = 1
        if counter == 0:
            ans_ef[1].append(pred)

    # true to false
    for pred in new_ef[0]:
        counter = 0
        pos = []
        for el in ans_ef[1]:
            if pred.name == el.name:
                i = 0
                flag = 0
                while i < len(pred.params):
                    if el.params[i] != pred.params[i]:
                        flag = 1
                    i += 1
                if flag == 0:
                    pos.append(counter)
            counter += 1
        for c in range(0, len(pos)):
            ans_ef[1].pop(pos[c] - c)


    # false to true
    for pred in new_ef[1]:
        counter = 0
        pos = []
        for el in ans_ef[0]:
            if pred.name == el.name:
                i = 0
                flag = 0
                while i < len(pred.params):
                    if el.params[i] != pred.params[i]:
                        flag = 1
                    i += 1
                if flag == 0:
                    pos.append(counter)
            counter += 1
        for c in range(0, len(pos)):
            ans_ef[0].pop(pos[c] - c)


def build_effects(node):
    if node.type == 0:
        return node.effect
    ef = ([], [])
    for sub in node.subtasks:
        apply_new(ef, build_effects(sub))
    node.effect = ef
    return ef
# ===============================================


class SequenceManager:
    def __init__(self, ws):
        self.worldStates = []
        self.worldStates.append(ws)
        self.wsBuf = []
        self.seq = []
        self.buf = []

    def add(self, el):
        nEl = EbtElem()
        nEl.effect = el.effect
        nEl.name = el.name
        nEl.precond = el.precond
        nEl.params = el.params
        nEl.type = 0
        nWs = copy.deepcopy(self.nowWs())
        ht.apply_effects(nWs, el.effect)
        self.seq.append(nEl)
        self.wsBuf.clear()

    def addStart(self, el, typ):
        nEl = EbtElem()
        nEl.effect = el.effect
        nEl.name = el.name
        nEl.precond = el.precond
        nEl.params = el.params
        nEl.type = typ
        nEl.arch = 0
        nWs = copy.deepcopy(self.nowWs())
        ht.apply_effects(nWs, el.effect)
        self.seq.append(nEl)
        self.wsBuf.clear()

    def addEnd(self, el, typ):
        nEl = EbtElem()
        nEl.effect = el.effect
        nEl.name = el.name
        nEl.precond = el.precond
        nEl.params = el.params
        nEl.type = typ
        nEl.arch = 1
        nWs = copy.deepcopy(self.nowWs())
        ht.apply_effects(nWs, el.effect)
        self.seq.append(nEl)
        self.wsBuf.clear()

    def lastEl(self):
        return self.buf[-1]

    def nextEl(self):
        return self.seq[-1]

    def nowWs(self):
        return self.worldStates[-1]

    def undo(self):
        if len(self.buf) == 0:
            return -1
        self.buf.append(self.seq.pop())
        self.wsBuf.append(self.worldStates.pop())
        return 1

    def redo(self):
        if len(self.buf) == 0:
            return -1
        if len(self.wsBuf) > 0:
            self.seq.append(self.buf.pop())
            self.worldStates.append(self.wsBuf.pop())
        else:
            self.seq.append(self.buf.pop())
            nWs = copy.deepcopy(self.nowWs())
            ht.apply_effects(nWs, self.seq[-1].effect)
            self.worldStates.append(nWs)
        return 1

    def redoAll(self):
        while len(self.buf) > 0:
            self.redo()

    def makeBackUp(self):
        ans = self.buf
        self.buf.clear()
        self.wsBuf.clear()
        return ans

    def getBackUp(self, bList):
        self.buf.extend(bList)

    def printRes(self, fileName):
        file = open(fileName, "w")
        s = ""
        for el in self.seq:
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
        file.close()


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


def addProcessor(manager, type):
    tID = manager.lastEl().id
    while (manager.lastEl().id != tID)


def process_ebt(manager, node):
    processor = 0
    # =================================================================================================================
    # Preprocess
    world_state = copy.deepcopy(manager.nowWs())
    # remove redundant procedure
    if (ht.check_all_precond(world_state, node.effect[0])) and not ht.check_any_precond(world_state, node.effect[1]):
        node.subtasks.clear()
        return True
    # move back
    flag = 1
    while flag == 1 and manager.undo() != -1:
        el = manager.lastEl()
        if not check_axes(world_state, node, el):
            manager.redo()
            flag = 0
        elif el.type != 0 and el.arch == 0:
            apply_new(node.precond, el.precond)
    # swap
    while (len(manager.buf) > 0) and (manager.lastEl().type != 0 and manager.arch == 0):
        manager.redo()
    # =================================================================================================================
    # adding start

    if len(manager.buf) != 0:
        if manager.lastEl().type == 2:
            manager.undo()
        elif manager.lastEl().type == 1:

    backUp = manager.makeBackUp()
    # =================================================================================================================
    for c in node.subtasks:
        if not process_ebt(manager, c):
            return False

    manager.addEnd(node)
    manager.getBackUp(backUp)
    manager.redoAll()
    return True


if __name__ == '__main__':
    domain_name = sys.argv[1]
    task_name = sys.argv[2]
    ans = gr.ground_files(domain_name, task_name)
    ini = copy.deepcopy(ans.init_state)
    root = ht.ansTask()
    for task in ans.tasks:
        e = ht.htn_search(ini, task)[2]
        root.subtasks.append(e)
        root.precond[0].extend(e.precond[0])
        root.precond[1].extend(e.precond[1])
    root.name = "MAIN"
    root.type = 1
    build_effects(root)
    print(root)
    #tree is build
    tree = SequenceManager(ans.init_state)
    process_ebt(tree, root)
    #tree.printRes("output.txt")
