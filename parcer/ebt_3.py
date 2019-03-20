import grounder as gr
import HTN as ht
import sys
import copy


def check_union(preds1, preds2):
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


class EbtElem:
    def __init__(self):
        self.name = ""
        self.num = -1
        self.parent = -1
        self.parentPos = -1
        self.processor = 0
        # 0 - line, 1 - parralel
        self.type = 0
        # 0 - none, 1 - line, 2 - paralel
        self.preWs = []
        self.postWs = []
        self.params = []
        self.precond = ([], [])
        self.effect = ([], [])
        self.arch = 1
        # 0 - ready, 1 - not ready
        self.sub = []

    def __str__(self):
        return "name " + str(self.name) + ":" + str(self.params) + str(self.type) + str(self.arch) + "\n" \
               + str(self.precond) + " " + str(self.effect) + "\n"

    def __repr__(self):
        return "name " + str(self.name) + ":" + str(self.params) + str(self.type) + str(self.arch) + "\n" \
               + str(self.precond) + " " + str(self.effect) + "\n"


class Visitor:
    def __init__(self, inWs, root):
        # -1 - start, len - fin
        self.list = []
        # making base root
        el = EbtElem()
        el.name = "MAIN"
        el.num = 0
        el.parent = -1
        el.parentPos = -1
        el.processor = 0
        el.type = 1
        el.preWs = inWs
        el.postWs = dict()
        el.params = []
        el.precond = root.precond
        el.effect = ([], [])
        el.arch = 1
        el.sub = []
        self.list.append(el)
        self.pos = 0
        self.num = 0

    def __getElem__(self):
        return self.list[self.num]

    def __goDeep__(self, ord):
        if ord != len(self.__getElem__().sub) and ord != -1:
            self.num = self.list[self.__getElem__().sub[ord]].num
            self.pos = -1
        elif ord == -1:
            self.pos = -1
        else:
            self.pos = len(self.__getElem__().sub)

    def __goUp__(self):
        self.pos = self.__getElem__().parentPos
        self.num = self.__getElem__().parent

    def next(self):
        if self.pos == -1:
            self.__goDeep__(0)
        else:
            if self.__getElem__().arch == 1:
                return False
            self.__goUp__()
            self.pos += 1
            self.__goDeep__(self.pos)
            if self.list[self.num].type == 0:
                self.pos = 0
        return True

    def prev(self):
        if self.__getElem__().type == 1 and self.pos == len(self.__getElem__().sub):
            self.__goDeep__(len(self.__getElem__().sub) - 1)
        else:
            if self.__getElem__().parent == -1:
                return False
            self.__goUp__()
            self.pos -= 1
            self.__goDeep__(self.pos)
            if self.list[self.num].type == 0:
                self.pos = 0
        return True

    def addStart(self, node):
        if self.pos == -1:
            self.__goUp__()
            if self.__getElem__().type == 0:
                # Making parralel
                el = EbtElem()
                el.name = "Paralel"
                el.num = len(self.list)
                el.parent = self.num
                el.parentPos = self.pos
                el.processor = 0
                el.type = 1
                el.preWs = self.list[self.getEl().sub[self.pos]].preWs
                el.params = []
                el.arch = 0
                el.sub = []
                el.sub.append(self.getEl().sub[self.pos])

                # Making new el
                n_el = EbtElem()
                n_el.name = node.name
                n_el.num = len(self.list) + 1
                n_el.parent = len(self.list)
                n_el.parentPos = 0
                n_el.processor = node.type -1
                n_el.params = node.params
                n_el.precond = node.precond
                n_el.effect = ([], [])
                n_el.arch = 1
                n_el.sub = []

                # changing prev
                prev = self.list[self.getEl().sub[self.pos]]
                prev.parent = n_el.parent
                prev.parentPos = 1

                # changing things
                self.list.append(el)
                self.list.append(n_el)
                self.getEl().sub[self.pos] = el.num
                el.sub.append(n_el.num)
                el.sub.append(prev.num)


            else:
                # Making new el
                n_el = EbtElem()
                n_el.name = node.name
                n_el.num = len(self.list)
                n_el.parent = self.num
                n_el.parentPos = 0
                n_el.processor = node.type - 1
                n_el.params = node.params
                n_el.precond = node.precond
                n_el.effect = ([], [])
                n_el.arch = 1
                n_el.sub = []

                self.__getElem__().sub.insert(0, n_el.num)
                for i in range(len(self.__getElem__().sub)):
                    self.list[self.__getElem__().sub[i]].parentPos = i
                self.list.append(n_el)
        else:
            # Making new el
            n_el = EbtElem()
            n_el.name = node.name
            n_el.num = len(self.list)
            n_el.parent = self.num
            n_el.parentPos = len(self.__getElem__().sub)
            n_el.processor = node.type - 1
            n_el.params = node.params
            n_el.precond = node.precond
            n_el.effect = ([], [])
            n_el.arch = 1
            n_el.sub = []

            self.__getElem__().sub.append(n_el.num)
            self.list.append(n_el)
            self.pos += 1

    def addEnd(self, node):
        self.__getElem__().effect = node.effect
        self.__getElem__().arch = 0

    def nowEl(self):
        ans = self.list[self.num]
        if self.pos == -1:
            ans.effect = ([], [])
        if self.pos == len(self.__getElem__().sub):
            ans.precond = ([], [])

    def redoAll(self):
        flag = True
        while(flag):
            flag = self.next()

    def nowWs(self):
        if self.pos == -1:
            return self.__getElem__().preWs
        else:
            return self.__getElem__().postWs

    def isEnd(self):
        return self.pos != -1

    def isParStart(self):
        return self.pos == -1 and self.__getElem__().type == 1 and self.__getElem__().processor == 1

    def fixAll(self):
        buf = self.__getElem__().preWs
        if self.isEnd():
            self.__getElem__().postWs = ht.apply_effects(buf, self.__getElem__().effect)
        while self.next():
            # print(self.pos, self.num)
            if self.isEnd():
                self.__getElem__().postWs = ht.apply_effects(buf, self.__getElem__().effect)
            else:
                self.__getElem__().preWs = buf

    def print(self, file,  num, base):
        file.write(base + str(self.list[num]))
        if self.list[num].type == 1:
            base += "||"
        base += "\t"
        for n in self.list[num].sub:
            self.print(file, n, base)
        if self.list[num].type == 1:
            base = base[:-2]
        base += base[0:-1]

    def print_self(self):
        print("======================================================\n", self.num, self.pos)
        for el in range(len(self.list)):
            print(el, self.list[el].name, self.list[el].params, self.list[el].parent, self.list[el].parentPos,
                  self.list[el].sub)




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
    print("ax_check\n", elem1, elem2, state, "\n===========================================\n", check_ax1(state, elem2),
          check_ax2(state, elem1, elem2), check_ax3(elem1, elem2))
    if check_ax1(state, elem2) and check_ax2(state, elem1, elem2) and check_ax3(elem1, elem2):
        return True
    return False


def preProcessNode(visitor, node):
    print(visitor.pos, visitor.num)
    visitor.prev()
    print(visitor.pos, visitor.num)
    print("pre process start", node.name)
    world_state = copy.deepcopy(visitor.nowWs())
    # remove redundant procedure
    if (ht.check_all_precond(world_state, node.effect[0])) and not ht.check_any_precond(world_state, node.effect[1]):
        # print("deleted", world_state, "\n", node.effect)
        node.subtasks.clear()
        return True
    # moveback the node front
    print("node not redundant")
    flag = 1
    print(visitor.pos, visitor.num)
    w_bool = flag == 1 and visitor.prev()
    print(w_bool)
    while w_bool:
        if not check_axes(visitor.nowWs(), visitor.nowEl(), node):
            flag = 0
        elif (visitor.nowEl().type != 0) and (visitor.pos == -1):
            apply_new(node.precond, visitor.nowEl().precond)
        w_bool = flag == 1 and visitor.prev()
        print(w_bool)
    print("went back")
    while visitor.isEnd() or visitor.isParStart():
        visitor.next()

    visitor.addStart(node)
    return True


def postProcessNode(visit, node):
    visit.addEnd(node)
    visit.fixAll()


def process_ebt(visitor, node):
    visitor.print_self()
    if not preProcessNode(visitor, node):
        return False
    for c in node.subtasks:
        if not process_ebt(visitor, c):
            return False
    if not postProcessNode(visitor, node):
        return False


def first_process(visitor, node):
    for c in node.subtasks:
        if not process_ebt(visitor, c):
            return False


if __name__ == '__main__':
    domain_name = sys.argv[1]
    task_name = sys.argv[2]
    ans = gr.ground_files(domain_name, task_name)
    ini = copy.deepcopy(ans.init_state)
    ini2 = copy.deepcopy(ini)
    root = ht.ansTask()
    for task in ans.tasks:
        e = ht.htn_search(ini, task)[2]
        root.subtasks.append(e)
        root.precond[0].extend(e.precond[0])
        root.precond[1].extend(e.precond[1])
    root.name = "MAIN"
    root.type = 1
    build_effects(root)
    # print(root)
    # tree is build
    print(ini2)
    tree = Visitor(ini2, root)
    first_process(tree, root)
    file = open("ans.txt", "w")
    tree.print(file, 0, "")
    file.close()
