import time
from collections import defaultdict,deque
class Limiter:
    def __init__(self,limit=10,window=60): self.limit=limit; self.window=window; self.hits=defaultdict(deque)
    def allow(self,key):
        now=time.time(); q=self.hits[key]
        while q and now-q[0]>self.window: q.popleft()
        if len(q)>=self.limit:return False
        q.append(now); return True
limiter=Limiter(10,60)
