class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []
        # detect_cycle_map:{key:uuid, value: next_activity}
        self.call_map = {}
        self.total_cnt = -1
        self.click_cnt = 0
    
    def add_call_map(self, uuid, next_activity):
        self.call_map[uuid] = next_activity
    
    def is_all_children_finish(self, target_activity):
        if self is None:
            return True
        for ele in self.children:
            if ele.value == target_activity:
                if ele.click_cnt == ele.total_cnt:
                    return True
                else:
                    return False
        return True


    def find_ancestor(self, activity_name):
        cur = self
        par = cur.parent
        while par is not None:
            if par.value == activity_name:
                return True
            cur = par
            par = cur.parent
        # print(cur.value)
        return False

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

if __name__ == "__main__":
    root = Node("A")
    b = Node("B")
    c = Node("C")
    # d = Node("D")
    # e = Node("E")
    root.add_child(b)
    b.add_child(c)
    c.add_child(root)
    print(c.find_ancestor())
