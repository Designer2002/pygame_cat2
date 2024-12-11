class Tree:
    def __init__(self, leaf):
        self.leaf = leaf
        self.lchild = None
        self.rchild = None

    def get_leafs(self):
        if self.lchild is None and self.rchild is None:
            yield self
        else:
            if self.lchild is not None:
                yield from self.lchild.get_leafs()
            if self.rchild is not None:
                yield from self.rchild.get_leafs()

    def get_level(self, level, queue):
        if queue is None:
            queue = []
        if level == 1:
            queue.push(self)
        else:
            if self.lchild is not None:
                self.lchild.get_level(level - 1, queue)
            if self.rchild is not None:
                self.rchild.get_level(level - 1, queue)
        return queue


    def paint(self, c):
        self.leaf.paint(c)
        if self.lchild is not None:
            self.lchild.paint(c)
        if self.rchild is not None:
            self.rchild.paint(c)



