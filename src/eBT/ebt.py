import eBT.grounder as gr
import eBT.HTN as ht
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


def applyLemma2(ans_ef, new_ef):
    params = set()
    for el in ans_ef[0]:
        for par in el.params:
            params.add(par)
    for el in ans_ef[1]:
        for par in el.params:
            params.add(par)
    n_new_ef = ([], [])
    for el in new_ef[0]:
        flag = False
        for p in el.params:
            if p in params:
                flag = True
        if flag:
            n_new_ef[0].append(el)
    for el in new_ef[1]:
        flag = False
        for p in el.params:
            if p in params:
                flag = True
        if flag:
            n_new_ef[1].append(el)
    apply_new(ans_ef, n_new_ef)


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
        self.preWs = dict()
        self.postWs = dict()
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

    def __goDeepNext__(self, ord):
        if ord != len(self.__getElem__().sub) and ord != -1:
            self.num = self.list[self.__getElem__().sub[ord]].num
            self.pos = -1
        elif ord == -1:
            self.pos = -1
        else:
            self.pos = len(self.__getElem__().sub)

    def __goDeepPrev__(self, ord):
        if ord != len(self.__getElem__().sub) and ord != -1:
            self.num = self.list[self.__getElem__().sub[ord]].num
            self.pos = len(self.list[self.num].sub)
        elif ord == -1:
            self.pos = -1
        else:
            self.pos = len(self.__getElem__().sub)

    def __goUp__(self):
        if self.__getElem__().parent != -1:
            self.pos = self.__getElem__().parentPos
            self.num = self.__getElem__().parent

    def next(self):
        if self.pos == -1:
            self.__goDeepNext__(0)
        else:
            if self.__getElem__().arch == 1:
                return False
            self.__goUp__()
            self.pos += 1
            self.__goDeepNext__(self.pos)
            if self.list[self.num].type == 0:
                self.pos = 0
        return True

    def prev(self):
        if self.__getElem__().type == 1 and self.pos == len(self.__getElem__().sub):
            self.__goDeepPrev__(len(self.__getElem__().sub) - 1)
        else:
            if self.__getElem__().parent == -1:
                return False
            self.__goUp__()
            self.pos -= 1
            self.__goDeepPrev__(self.pos)
            if self.list[self.num].type == 0:
                self.pos = 0
        return True

    def addStart(self, node):
        if self.pos == -1:
            self.__goUp__()
            if (self.__getElem__().processor == 1) and (self.pos != 0):
                self.__goUp__()
                self.pos += 1
                self.__goDeepNext__(self.pos)
                self.addStart(node)
                return True
            if self.__getElem__().processor == 0:
                # Making parralel
                el = EbtElem()
                el.name = "Paralel"
                el.num = len(self.list)
                el.parent = self.num
                el.parentPos = self.pos
                el.processor = 1
                el.type = 1
                el.preWs = self.list[self.__getElem__().sub[self.pos]].preWs
                el.postWs = dict()
                el.params = []
                el.arch = 0
                el.sub = []

                # Making new el
                n_el = EbtElem()
                n_el.name = node.name
                n_el.num = len(self.list) + 1
                n_el.parent = len(self.list)
                n_el.parentPos = 0
                n_el.preWs = el.preWs
                n_el.postWs = dict()
                n_el.processor = node.type - 1
                n_el.params = node.params
                n_el.precond = node.precond
                n_el.effect = ([], [])
                n_el.arch = 1
                n_el.sub = []
                if node.type == 0:
                    n_el.type = 0
                else:
                    n_el.type = 1
                # changing prev
                prev = self.list[self.__getElem__().sub[self.pos]]
                prev.parent = n_el.parent
                prev.parentPos = 1

                # changing things
                self.list.append(el)
                self.list.append(n_el)
                self.__getElem__().sub[self.pos] = el.num
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
                n_el.preWs = self.__getElem__().preWs
                n_el.postWs = dict()
                if node.type == 0:
                    n_el.type = 0
                else:
                    n_el.type = 1

                self.__getElem__().sub.insert(0, n_el.num)
                self.list.append(n_el)
                for i in range(len(self.__getElem__().sub)):
                    self.list[self.__getElem__().sub[i]].parentPos = i
        else:
            # Making new el
            n_el = EbtElem()
            n_el.name = node.name
            n_el.num = len(self.list)
            n_el.parent = self.num
            n_el.parentPos = len(self.__getElem__().sub)
            n_el.processor = node.type - 1
            n_el.params = node.params
            n_el.preWs = self.__getElem__().postWs
            n_el.postWs = dict()
            n_el.precond = node.precond
            n_el.effect = ([], [])
            n_el.arch = 1
            n_el.sub = []
            if node.type == 0:
                n_el.type = 0
            else:
                n_el.type = 1

            self.__getElem__().sub.append(n_el.num)
            self.list.append(n_el)
        self.num = len(self.list) - 1
        self.pos = -1

    def addEnd(self, node):
        self.__getElem__().effect = node.effect
        self.__getElem__().arch = 0

    def nowEl(self):
        ans = copy.deepcopy(self.list[self.num])
        if self.pos == -1:
            ans.effect = ([], [])
        if self.pos == len(self.__getElem__().sub):
            ans.precond = ([], [])
        return ans

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
        self.prev()
        buf = copy.deepcopy(self.nowWs())
        self.next()
        if self.isEnd():
            ht.apply_effects(buf, self.__getElem__().effect[0])
            ht.apply_not_effects(buf, self.__getElem__().effect[1])
            self.__getElem__().postWs = buf
            buf = self.__getElem__().postWs
        else:
            self.__getElem__().preWs = buf
            buf = copy.deepcopy(buf)
        while self.next():
            # print(self.pos, self.num)
            if self.isEnd():
                ht.apply_effects(buf, self.__getElem__().effect[0])
                ht.apply_not_effects(buf, self.__getElem__().effect[1])
                self.__getElem__().postWs = buf
                buf = self.__getElem__().postWs
            else:
                self.__getElem__().preWs = buf

    def print(self, file, num, base):
        file.write(base + str(self.list[num].name) + str(self.list[num].params) + "\n")
        if self.list[num].type == 1 and self.list[num].processor == 1:
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
    if check_ax1(state, elem2) and check_ax2(state, elem1, elem2) and check_ax3(elem1, elem2):
        return True
    return False


def preProcessNode(visitor, node):
    world_state = copy.deepcopy(visitor.nowWs())
    # remove redundant procedure
    if (ht.check_all_precond(world_state, node.effect[0])) and not ht.check_any_precond(world_state, node.effect[1]):
        # print("deleted", world_state, "\n", node.effect)
        node.subtasks.clear()
        return True
    # moveback the node front
    flag = 1
    w_bool = (flag == 1) and (visitor.prev())
    while w_bool:
        if visitor.__getElem__().type == 0:
            visitor.prev()
            ws = copy.deepcopy(visitor.nowWs())
            visitor.next()
        else:
            ws = copy.deepcopy(visitor.nowWs())
        if not check_axes(ws, visitor.nowEl(), node):
            visitor.next()
            flag = 0
        elif (visitor.nowEl().type != 0) and (visitor.pos == -1):
            applyLemma2(node.precond, visitor.nowEl().precond)
        w_bool = flag == 1 and visitor.prev()
    # visitor.next()
    while (visitor.isEnd() or visitor.isParStart()) and visitor.__getElem__().arch != 1:
        visitor.next()

    visitor.addStart(node)
    visitor.fixAll()
    return True


def postProcessNode(visit, node):
    visit.addEnd(node)
    visit.fixAll()
    return True


def process_ebt(visitor, node):
    visitor.print_self()
    if not preProcessNode(visitor, node):
        return False
    for c in node.subtasks:
        if not process_ebt(visitor, c):
            return False
    if not postProcessNode(visitor, node):
        return False
    return True


def first_process(visitor, node):
    for c in node.subtasks:
        if not process_ebt(visitor, c):
            return False


def eBT_start(d_name, t_name):
    domain_name = d_name
    task_name = t_name
    ans = gr.ground_files(domain_name, task_name)
    ini = copy.deepcopy(ans.init_state)
    ini2 = copy.deepcopy(ini)
    root = ht.ansTask()
    print("task grounded")
    for task in ans.tasks:
        e = ht.htn_search(ini, task)[2]
        root.subtasks.append(e)
        root.precond[0].extend(e.precond[0])
        root.precond[1].extend(e.precond[1])
    root.name = "MAIN"
    root.type = 1
    print("HTN solution found")
    build_effects(root)
    # print(root)
    # tree is build
    tree = Visitor(ini2, root)
    file = open("ans.txt", "w")
    tree.print(file, 0, "")
    file.close()
    print("eBt is ready")


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
    print(first_process(tree, root))
    file = open("ans.txt", "w")
    tree.print(file, 0, "")
    file.close()
