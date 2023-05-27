class Memory(object):

    def __init__(self):
        self.similarity_mem = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(Memory, "_instance"):
            Memory._instance = object.__new__(cls)
        return Memory._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Memory, '_instance'):
            Memory._instance = Memory(*args, **kwargs)
        return Memory._instance

    def query_simi_mem(self, key):
        if self.similarity_mem.get(key , False) == False:
            return None
        else:
            return self.similarity_mem.get(key)

    def update_simi_mem(self, key, val):
        self.similarity_mem[key] = val

    def get_similarity_mem(self):
        return self.similarity_mem



