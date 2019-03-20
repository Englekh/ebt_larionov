import domain_parcer as dp


class Problem:
    def __init__(self):
        self.name = ""
        self.domain = ""
        self.objects = dict()
        self.pred = dict()
        self.goal = ""


def get_objects(it):
    ans = dict()
    buf = []
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
            ans[it.wrd()] = set()
            for el in buf:
                ans[it.wrd()].add(el)
            buf.clear()
            if it.b_count >= count:
                it.next()

    return ans


def get_one(it):
    name = it.wrd()
    count = it.b_count
    it.next()
    buf = []
    while count == it.b_count:
        buf.append(it.wrd())
        it.next()
    buf.append(it.wrd())
    it.next()
    return name, buf


def get_prdeicates(it):
    ans = dict()
    counter = it.b_count
    it.next()
    while it.b_count >= counter:
        p = get_one(it)
        if not ans.get(p[0]):
            ans[p[0]] = []
        ans[p[0]].append(p[1])
    return ans


def parse_task(name):
    iter = dp.DomainIterator(name)
    ans = Problem()
    iter.next()
    iter.next()
    ans.name = iter.wrd()
    iter.next()
    iter.next()
    ans.domain = iter.wrd()
    iter.next()
    ans.objects = get_objects(iter)
    iter.next()
    ans.pred = get_prdeicates(iter)
    iter.next()
    iter.next()
    ans.goal = dp.get_preds1(iter)[0]
    return ans


if __name__ == '__main__':
    # f = open("domain.pddl", "r")
    #  parse_domain(f)
    parse_task("test_task.pddl")