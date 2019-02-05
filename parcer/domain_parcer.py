# excluding blank and comment lines
def get_line(f):
    line = f.readline()
    while line[0] == ";" or line.isspace():
        line = f.readline()
    return line

# main classes
# ==================================================


class DomainIterator:
    def __init__(self, name):
        self.f = open(name, "r")
        self.buf = get_line(self.f).split()
        self.b_count = 0
        self.pos = 0
        for s in self.buf[self.pos]:
            if s == '(':
                self.b_count += 1
            elif s == ')':
                self.b_count -= 1

    def next(self):
        if self.pos + 1 < len(self.buf):
            self.pos += 1
        else:
            self.pos = 0
            self.buf = get_line(self.f).split()

        for s in self.buf[self.pos]:
            if s == '(':
                self.b_count += 1
            elif s == ')':
                self.b_count -= 1

    def wrd(self):
        return self.buf[self.pos].lstrip("(").rstrip(")")


class Object:
    def __init__(self, nam, typ):
        self.name = nam
        self.type = typ

    def __str__(self):
        return "(" + str(self.name) + ", " + str(self.type) + ")"

    def __repr__(self):
        return "(" + str(self.name) + ", " + str(self.type) + ")"


class Predicate:
    def __init__(self, nam):
        self.name = nam
        self.params = set()

    def __str__(self):
        return str(self.name) + ': ' + str(self.params)

    def __repr__(self):
        return str(self.name) + ": " + str(self.params)


class Axiom:
    def __init__(self):
        self.params = set()
        self.postcond = set()

    def __str__(self):
        return "(" + str(self.params) + "|" + str(self.postcond) + ")"

    def __repr__(self):
        return "(" + str(self.params) + "|" + str(self.postcond) + ")"


class Task:
    def __init__(self, name):
        self.name = name
        self.type = 0
        self.subtype = 0
        self.params = set()
        # 0 - primitive, 1 - compound
        self.thing = []

    def __str__(self):
        return "(task -" + str(self.name) + "," + str(self.type) + ";" +\
               str(self.params) + "\n :" + str(self.thing) + ")"

    def __repr__(self):
        return "(task -" + str(self.name) + "," + str(self.type) + ";" +\
               str(self.params) + "\n :" + str(self.thing) + ")"


class Operator:
    def __init__(self, precond, effect):
        self.precond = precond
        self.effect = effect

    def __str__(self):
        return "oper - " + str(self.precond) + ";" + str(self.effect) + ")\n"

    def __repr__(self):
        return "oper - " + str(self.precond) + ";" + str(self.effect) + ")\n"




class Method:
    def __init__(self, precond, effect, params):
        self.params = params
        self.precond = precond
        self.subtask = effect

    def __str__(self):
        return "oper - " + str(self.precond) + ";" + str(self.subtask) + ")\n"

    def __repr__(self):
        return "oper - " + str(self.precond) + ";" + str(self.subtask) + ")\n"


class Domain:
    def __init__(self, nam):
        self.name = nam
        self.types = dict()
        self.req = set()
        self.pred = set()
        self.tasks = dict()
        self.axioms = set()

# ====================================
# main functions


def get_params_and_names(it):
    name = it.wrd()
    params = set()
    buf = []
    ans = Predicate(name)
    count = it.b_count
    it.next()
    while count <= it.b_count:
        if it.wrd() != "-":
            if not (it.wrd().isspace() or it.wrd() == ""):
                buf.append(it.wrd())
            it.next()
        else:
            it.next()
            while it.wrd().isspace() or it.wrd() == "":
                it.next()
            for el in buf:
                params.add(Object(el, it.wrd()))
            buf.clear()
            if it.b_count >= count:
                it.next()

    it.next()
    ans.params = params
    return ans


# main  ===============================
def get_requirements(it):
    ans = set()
    count = it.b_count
    it.next()
    while count == it.b_count:
        if not (it.wrd().isspace() or it.wrd() == ""):
            ans.add(it.wrd())
        it.next()
    if not (it.wrd().isspace() or it.wrd() == ""):
        ans.add(it.wrd())
    it.next()
    return ans


def get_predicates(it):
    ans = set()
    count = it.b_count
    it.next()
    while count <= it.b_count:
        ans.add(get_params_and_names(it))
    return ans


def get_pred1(it):
    name = it.wrd()
    preds = []
    count = it.b_count
    it.next()
    while count == it.b_count:
        if not (it.wrd().isspace() or it.wrd() == ""):
            preds.append(it.wrd())
        it.next()
    if not (it.wrd().isspace() or it.wrd() == ""):
        preds.append(it.wrd())
    if it.b_count > 0:
        it.next()
    return name, preds


def get_preds1(it):
    if it.wrd() == "and":
        it.next()
    count = it.b_count
    pred = []
    npred = []
    while count <= it.b_count:
        if it.wrd() == "not":
            it.next()
            npred.append(get_pred1(it))
        else:
            pred.append(get_pred1(it))
    return pred, npred


def get_operator(it):
    it.next()
    task = get_params_and_names(it)
    precond = get_preds1(it)
    end = get_preds1(it)
    return task, precond, end


def get_preds2(it):
    print(it.wrd())
    if it.wrd() == ":ordered":
        type = 1
        it.next()
    else:
        type = 2
        it.next()
    count = it.b_count
    pred = []
    npred = []
    while count <= it.b_count:
        if it.wrd() == "not":
            it.next()
            npred.append(get_pred1(it))
        else:
            pred.append(get_pred1(it))
    return (pred, npred),  type


def get_method(it):
    it.next()
    task = get_params_and_names(it)
    precond = get_preds1(it)
    end = get_preds2(it)
    return task, precond[0], end, precond[1]


def get_types(it):
    count = it.b_count
    if it.wrd() == "and":
        return dict()
    it.next()
    ans = dict()
    buf = []
    archetypes = []
    while count == it.b_count:
        if it.wrd() != "-":
            if not (it.wrd().isspace() or it.wrd() == ""):
                buf.append(it.wrd())
            it.next()
        else:
            it.next()
            while it.wrd().isspace() or it.wrd() == "":
                it.next()
            for el in buf:
                if not ans.get(el):
                    ans[el] = set()
                ans[el].add(it.wrd())
            if not ans.get(it.wrd()):
                ans[it.wrd()] = set()
            archetypes.append(it.wrd())
            buf.clear()
            if it.b_count == count:
                it.next()
    for el in buf:
        if not ans.get(el):
            ans[el] = []
    it.next()

    for obj in archetypes:
        if len(ans[obj]) > 0:
            for el in ans:
                if obj in ans[el]:
                    ans[el].update(ans[obj])
    return ans


def get_axiom(it):
    it.next()
    ans = Axiom()
    ans.params = get_pred1(it)
    ans.postcond = get_preds1(it)
    return ans


def parse_domain(file):
    ans = Domain("")
    iter = DomainIterator(file)
    iter.next()
    while iter.b_count > 0:
        # ===============================
        if iter.wrd() == "domain":
            iter.next()
            ans.name = iter.wrd()
            iter.next()
        # ===============================
        if iter.wrd() == ":requirements":
            ans.req = get_requirements(iter)
        # ===============================
        if iter.wrd() == ":types":
            ans.types = get_types(iter)
        # ===============================
        if iter.wrd() == ":predicates":
            ans.pred = get_predicates(iter)
        # ===============================
        if iter.wrd() == ":-":
            ans.axioms.add(get_axiom(iter))
        # ===============================
        if iter.wrd() == ":operator":
            op = get_operator(iter)
            task = op[0].name
            ans.tasks[task] = Task(task)
            ans.tasks[task].type = 0
            ans.tasks[task].params = op[0].params
            ans.tasks[task].thing = Operator(op[1], op[2])
        # ===============================
        if iter.wrd() == ":method":
            op = get_method(iter)
            task = op[0].name
            if not ans.tasks.get(task):
                ans.tasks[task] = Task(task)
                ans.tasks[task].type = 1
            ans.tasks[task].subtype = op[3]
            ans.tasks[task].thing = Method(op[1], op[2], op[0].params)
        if (iter.wrd().isspace() or iter.wrd() == "") and iter.b_count > 0:
            iter.next()
    print(ans.req)

    return ans


if __name__ == '__main__':
    # f = open("domain.pddl", "r")
    #  parse_domain(f)
    parse_domain("test_domain2.pddl")
    #it = DomainIterator("gil.pddl")
    #print(get_operator(it))


