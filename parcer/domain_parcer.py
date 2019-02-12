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
        self.line_count = 1
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
            self.line_count += 1
            self.buf = get_line(self.f).split()

        for s in self.buf[self.pos]:
            if s == '(':
                self.b_count += 1
            elif s == ')':
                self.b_count -= 1

    def wrd(self):
        return self.buf[self.pos].lstrip("(").rstrip(")")

    def cwrd(self):
        return self.buf[self.pos]


class Object:
    def __init__(self, nam, typ):
        self.name = nam
        self.type = typ

    def __str__(self):
        return "(" + str(self.name) + ", " + str(self.type) + ")"

    def __repr__(self):
        return "(" + str(self.name) + ", " + str(self.type) + ")"


class LongPredicate:
    def __init__(self, nam):
        self.name = nam
        self.params = []

    def __str__(self):
        return str(self.name) + ': ' + str(self.params)

    def __repr__(self):
        return str(self.name) + ": " + str(self.params)


class ShortPredicate:
    def __init__(self, nam):
        self.name = nam
        self.params = []

    def __str__(self):
        return str(self.name) + ': ' + str(self.params)

    def __repr__(self):
        return str(self.name) + ": " + str(self.params)


class Axiom:
    def __init__(self):
        self.params = []
        self.postcond = []

    def __str__(self):
        return "(" + str(self.params) + " | " + str(self.postcond) + ")"

    def __repr__(self):
        return "(" + str(self.params) + " | " + str(self.postcond) + ")"


class Task:
    def __init__(self, name):
        self.name = name
        self.params = []
        self.type = 0
        # 0 - primitive, 1 - compound
        self.things = []

    def __str__(self):
        return "(task -" + str(self.name) + "," + str(self.type) + ";" +\
               str(self.params) + "\n :" + str(self.things) + ")"

    def __repr__(self):
        return "(task -" + str(self.name) + "," + str(self.type) + ";" +\
               str(self.params) + "\n :" + str(self.things) + ")"


class Operator:
    def __init__(self, name):
        self.name = name
        self.precond = []
        self.effect = []

    def __str__(self):
        return "oper - " + str(self.precond) + ";" + str(self.effect) + ")\n"

    def __repr__(self):
        return "oper - " + str(self.precond) + ";" + str(self.effect) + ")\n"


class Method:
    def __init__(self, name):
        self.name = name
        self.type = 0
        self.priority = 0
        # 0 - line, 1 - parralel
        self.precond = []
        self.subtask = []

    def __str__(self):
        return "Method - " + str(self.precond) + ";" + str(self.subtask) + ")\n"

    def __repr__(self):
        return "Method - " + str(self.precond) + ";" + str(self.subtask) + ")\n"


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


def get_name_and_params(it):
    name = it.wrd()
    params = []
    buf = []
    ans = LongPredicate(name)
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
                params.append(Object(el, it.wrd()))
            buf.clear()
            if it.b_count >= count:
                it.next()

    it.next()
    ans.params = params
    return ans


# main  ===============================
def get_requirements(it):
    ans = []
    count = it.b_count
    it.next()
    while count == it.b_count:
        if not (it.wrd().isspace() or it.wrd() == ""):
            ans.append(it.wrd())
        it.next()
    if not (it.wrd().isspace() or it.wrd() == ""):
        ans.append(it.wrd())
    it.next()
    return ans


def get_types(it):
    count = it.b_count
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
    if len(buf) > 0:
        if not (it.wrd().isspace() or it.wrd() == ""):
            buf.append(it.wrd())
    for el in buf:
        if not ans.get(el):
            ans[el] = set()
    it.next()

    for obj in archetypes:
        if len(ans[obj]) > 0:
            for el in ans:
                if obj in ans[el]:
                    ans[el].update(ans[obj])
    return ans


def get_predicates(it):
    ans = set()
    count = it.b_count
    it.next()
    while count <= it.b_count:
        ans.add(get_name_and_params(it))
    return ans


def get_short(it):
    ans = ShortPredicate("")
    ans.name = it.wrd()
    count = it.b_count
    it.next()
    while count == it.b_count:
        if not (it.wrd().isspace() or it.wrd() == ""):
            ans.params.append(it.wrd())
        it.next()
    if not (it.wrd().isspace() or it.wrd() == ""):
        ans.params.append(it.wrd())
    if it.b_count > 0:
        it.next()
    return ans


def get_preds1(it):
    if it.wrd() == "not":
        count = it.b_count
    else:
        count = it.b_count - 1
    pred = []
    npred = []
    while count <= it.b_count:
        if it.wrd().isspace() or it.wrd() == "":
            it.next()
        else:
            if it.wrd() == "not":
                it.next()
                npred.append(get_short(it))
            else:
                pred.append(get_short(it))
    it.next()
    return pred, npred


def get_axiom(it):
    it.next()
    ans = Axiom()
    ans.params = get_preds1(it)[0]
    ans.postcond = get_preds1(it)[0]
    return ans


def get_base_tasks(it):
    it.next()
    ans = dict()
    count = it.b_count
    while count <= it.b_count:
        nt = get_name_and_params(it)
        ans[nt.name] = Task(nt.name)
        ans[nt.name].params = nt.params
    return ans


def get_operator(it, dct):
    it.next()
    nm = it.wrd()
    it.next()
    on = it.wrd()
    it.next()
    oper = Operator(on)
    oper.name = on
    oper.precond = get_preds1(it)

    oper.effect = get_preds1(it)
    dct[nm].type = 0
    dct[nm].things.append(oper)
    return 0


def get_method(it, dct):
    it.next()
    nm = it.wrd()
    it.next()
    on = it.wrd()
    it.next()
    method = Method(on)
    if it.wrd() == "ordered":
        method.type = 0
    else:
        method.type = 1
    it.next()
    method.priority = int(it.wrd())
    it.next()
    method.precond = get_preds1(it)
    method.subtask = get_preds1(it)[0]
    dct[nm].type = 1
    dct[nm].things.append(method)
    return 0


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
        if iter.wrd() == ":tasks":
            ans.tasks = get_base_tasks(iter)
        # ===============================
        if iter.wrd() == ":-":
            ans.axioms.add(get_axiom(iter))
        # ===============================
        if iter.wrd() == ":operator":
            get_operator(iter, ans.tasks)
        # ===============================
        if iter.wrd() == ":method":
            get_method(iter, ans.tasks)
        if (iter.wrd().isspace() or iter.wrd() == "") and iter.b_count > 0:
            iter.next()
    return ans


if __name__ == '__main__':
    # f = open("domain.pddl", "r")
    #  parse_domain(f)
    parse_domain("test_domain.pddl")


