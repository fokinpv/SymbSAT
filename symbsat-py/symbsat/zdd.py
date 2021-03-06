# pylint:disable=invalid-name
"""ZDDs."""
from collections import defaultdict
from functools import partialmethod

from symbsat.monom import Monom


class ZDD:

    __slots__ = ("monom_type", "root", "_lm", "_cache")

    class Node:

        __slots__ = ("var", "mul", "add", "_id")

        def __init__(self, var, m, a):
            self.var = var
            self.mul = m  # and
            self.add = a  # xor
            self._id = id(self)

        @property
        def id(self):
            return self._id

        def copy(self):
            if self.var < 0:
                return self
            return ZDD.Node(self.var, self.mul.copy(), self.add.copy())

        def is_zero(self):
            return self.var == -2

        def is_one(self):
            return self.var == -1

        def __str__(self):
            if self == ZDD._one:
                return "_one"
            if self == ZDD._zero:
                return "_zero"

            return "%s -> {%s} {%s}" % (self.var, self.mul, self.add)

        def __eq__(self, other):
            if self.var != other.var:
                return False
            elif self.is_zero() and other.is_zero():
                return True
            elif self.is_one() and other.is_one():
                return True
            else:
                return self.mul == other.mul and self.add == other.add

    ring = None
    _one = Node(-1, None, None)
    _zero = Node(-2, None, None)

    def __init__(self, monom_type, var=-1, monom=None):
        self.monom_type = monom_type
        self._lm = None
        self._cache = defaultdict(list)

        if monom is not None:
            if monom.is_one():
                self.setOne()
            elif monom.is_zero():
                self.setZero()
            else:
                self.root = self._create_node(
                    monom.vars[0], ZDD._one, ZDD._zero
                )
                for var_ in monom.vars[1:]:
                    self.root = self._mul(
                        self.root, self._create_node(var_, ZDD._one, ZDD._zero)
                    )
        elif var < 0:
            self.root = ZDD._zero
        else:
            self.root = self._create_node(var, ZDD._one, ZDD._zero)

    def __eq__(self, other):
        """Compare two ZDDs as their representation
        as the list of monomials in lex order
        """
        return list(self) == list(other)

    def _create_node(self, var, m, a):
        if m.is_zero():
            raise RuntimeError

        if var in self._cache:
            for cached in self._cache[var]:
                if cached.mul == m and cached.add == a:
                    return cached

        r = ZDD.Node(var, m, a)
        self._cache[var].append(r)
        return r

    def _add(self, i, j):

        if i.is_zero():
            return j
        if j.is_zero():
            return i
        if i == j:
            return ZDD._zero

        if i.is_one():
            r = self._create_node(j.var, j.mul, self._add(j.add, ZDD._one))
        elif j.is_one():
            r = self._create_node(i.var, i.mul, self._add(i.add, ZDD._one))
        else:
            if i.var < j.var:
                r = self._create_node(i.var, i.mul, self._add(i.add, j))
            elif i.var > j.var:
                r = self._create_node(j.var, j.mul, self._add(i, j.add))
            else:
                m = self._add(i.mul, j.mul)
                a = self._add(i.add, j.add)

                if m == ZDD._zero:
                    return a

                r = self._create_node(i.var, m, a)
        return r

    def _mul(self, i, j):

        if i.is_one():
            return j
        if i.is_zero() or j.is_zero():
            return ZDD._zero
        if j.is_one() or i == j:
            return i

        r = None
        if i.var < j.var:
            m = self._mul(i.mul, j)
            a = self._mul(i.add, j)

            if m.is_zero():
                return a

            r = self._create_node(i.var, m, a)
        elif i.var > j.var:
            m = self._mul(j.mul, i)
            a = self._mul(j.add, i)

            if m.is_zero():
                return a

            r = self._create_node(j.var, m, a)
        else:
            m1 = self._mul(i.add, j.mul)
            m2 = self._mul(i.mul, j.mul)
            m3 = self._mul(i.mul, j.add)
            ms_sum = self._add(m1, self._add(m2, m3))

            if ms_sum.is_zero():
                return self._mul(i.add, j.add)

            r = self._create_node(i.var, ms_sum, self._mul(i.add, j.add))
        return r

    def __add__(self, other):

        if isinstance(other, Monom):
            return self + ZDD(self.monom_type, monom=other)
        if isinstance(other, ZDD):
            r = ZDD(self.monom_type)
            r.root = self._add(self.root, other.root)
            r._cache = self._cache.copy()
            return r
        return NotImplemented

    def __mul__(self, other):

        if isinstance(other, Monom):
            return self * ZDD(self.monom_type, monom=other)
        if isinstance(other, ZDD):
            r = ZDD(self.monom_type)
            r.root = self._mul(self.root, other.root)
            r._cache = self._cache.copy()
            return r

        return NotImplemented

    def copy(self):
        r = ZDD(self.monom_type)
        r.root = self.root.copy()
        r._cache = self._cache.copy()
        r._lm = self._lm
        return r

    def zero(self):
        zdd_zero = ZDD(self.monom_type)
        zdd_zero.setZero()
        return zdd_zero

    def one(self):
        zdd_one = ZDD(self.monom_type)
        zdd_one.setOne()
        return zdd_one

    def setZero(self):
        self.root = ZDD._zero

    def setOne(self):
        self.root = ZDD._one

    def is_zero(self):
        return self.root.is_zero()

    def is_one(self):
        return self.root.is_one()

    def lm(self):
        if self.root.is_zero():
            return self.monom_type.zero()
        if self.root.is_one():
            return self.monom_type.one()

        if self._lm is None:
            monom = []
            i = self.root
            while i.var >= 0:
                monom.append(i.var)
                i = i.mul
            #  self._lm = Monom(vars=monom)
            self._lm = self.monom_type(vars=monom)
        return self._lm

    def __iter__(self):
        if self.root.is_zero():
            yield self.monom_type.zero()
        elif self.root.is_one():
            yield self.monom_type.one()
        else:
            monom, path = [], []
            i = self.root
            while i.var >= 0:
                monom.append(i.var)
                path.append(i)
                i = i.mul
            #  yield Monom(vars=monom)
            yield self.monom_type(vars=monom)
            while path:
                while path and path[-1].add.is_zero():
                    path.pop()
                    monom.pop()
                if path:
                    i = path.pop().add
                    monom.pop()
                    while i != ZDD._one:
                        monom.append(i.var)
                        path.append(i)
                        i = i.mul
                    if monom == []:
                        yield self.monom_type.one()
                        break
                    #  yield Monom(vars=monom)
                    yield self.monom_type(vars=monom)

    def __str__(self):
        return " + ".join(map(str, self))


def make_zdd_type(monom_type):
    class _ZDD(ZDD):
        __init__ = partialmethod(ZDD.__init__, monom_type)

    return _ZDD


def view(zdd):
    import string

    try:
        import graphviz as gv
    except ImportError:
        print("Install graphviz 'pip install graphviz'")

    def gv_node(graph, node):
        if node.is_zero():
            graph.node("0", shape="box")
            return "0"
        if node.is_one():
            graph.node("1", shape="box")
            return "1"
        graph.node(
            "{}".format(node.id), label=string.ascii_lowercase[node.var]
        )
        return "{}".format(node.id)

    stack = [zdd.root]
    graph = gv.Digraph()
    edges = set()

    while stack:
        node = stack.pop()

        if node.mul:
            head = gv_node(graph, node)
            tail = gv_node(graph, node.mul)
            if ("mul", head, tail) not in edges:
                graph.edge(head, tail, style="solid")
                edges.add(("mul", head, tail))
            stack.append(node.mul)

        if node.add:
            head = gv_node(graph, node)
            tail = gv_node(graph, node.add)
            if ("add", head, tail) not in edges:
                graph.edge(head, tail, style="dashed")
                edges.add(("add", head, tail))
            stack.append(node.add)

    graph.view()
