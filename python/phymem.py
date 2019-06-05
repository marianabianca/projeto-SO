# This is the only file you must implement

# This file will be imported from the main code. The PhysicalMemory class
# will be instantiated with the algorithm received from the input. You may edit
# this file as you which

# NOTE: there may be methods you don't need to modify, you must decide what
# you need...

class PhysicalMemory(object):
  ALGORITHM_AGING_NBITS = 8
  """How many bits to use for the Aging algorithm"""

  def __init__(self, algorithm):
    assert algorithm in {"fifo", "nru", "lru", "aging", "second-chance"}
    self.algorithm = algorithm

  def put(self, frameId):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    pass

  def evict(self):
    """Deallocates a frame from the physical memory and returns its frameId"""
    # You may assume the physical memory is FULL so we need space!
    # Your code must decide which frame to return, according to the algorithm
    pass

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    pass

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    pass

class FIFO(PhysicalMemory):
  def __init__(self):
    from Queue import Queue
    super(FIFO, self).__init__("fifo")

    self.queue = Queue()
  
  def put(self, frameId):
    self.queue.put(frameId)

  def evict(self):
    return self.queue.get()

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    pass

# Niveis de prioridade
# 3. referenced, modified
# 2. referenced, not modified
# 1. not referenced, modified
# 0. not referenced, not modified

class NRU(PhysicalMemory):
  def __init__(self):
    super(NRU, self).__init__("nru")
    self.frames = []
  
  #(frameID, referenced, modified, Nivel prioridade)
  def put(self, frameId):
    self.frames.append((frameId, False, False, 0))

  def evict(self):
    aux = min(self.frames, key=lambda x: x[3])
    self.frames.remove(aux)
    return aux[0]

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    prioridade = -1
    index = 0
    for i in range(len(self.frames)):
      index = i
      if(self.frames[i][0] == frameId):
        if(self.frames[i][1] and self.frames[i][2]):
          prioridade = 3
        elif(self.frames[i][1] and (not self.frames[i][2])):
          prioridade = 2
        elif ((not self.frames[i][1]) and self.frames[i][2]):
          prioridade = 1
        else:
          prioridade = 0 
        break
    self.frames[index]= (frameId, True, isWrite, prioridade)

class LRU(PhysicalMemory):
  def __init__(self):
    super(LRU, self).__init__("lru")
    self.lista = []
  
  def put(self, frameId):
    self.lista.append(frameId)

  def evict(self):
    return self.lista.pop(0)

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    if frameId in self.lista:
      self.lista.remove(frameId)
    self.lista.append(frameId)

class Aging(PhysicalMemory):
  def __init__(self):
    super(Aging, self).__init__("aging")
    self.frames = {}
  
  def put(self, frameId):
    self.frames[frameId] = "1"

  def evict(self):
    mn = ""
    for frame in self.frames:
      if mn == "" or int(self.frames[frame], 2) < int(self.frames[mn], 2):
        mn = frame
    
    self.frames.pop(mn)
    return mn

  def clock(self):
    for frame in self.frames:
      self.frames[frame] = "0" + self.frames[frame]

  def access(self, frameId, isWrite):
    self.frames[frameId] = "1" + self.frames[frameId]

class SecondChance(PhysicalMemory):
  def __init__(self):
    from Queue import Queue
    super(SecondChance, self).__init__("second-chance")
    self.frames = Queue()
    self.second_chance = {}

  def put(self, frameId):
    self.frames.put(frameId)
    self.second_chance[frameId] = 0

  def evict(self):
    while(True):
      frameId = self.frames.get()
      if(self.second_chance[frameId] == 0):
        self.frames.put(frameId)
        self.second_chance[frameId] = 1          
      else:
        self.second_chance.pop(frameId)
        return frameId

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    self.second_chance[frameId] = 0

