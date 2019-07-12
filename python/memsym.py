import sys
from phymem import *

class VirtualMemory:
    def __init__(self, npages, nframes, physicalMemory, tlb_size):
        #this maps page_id to an entry such as (frame_id, mapped, r, m)
        self.page_table = {}
        self.phy_mem = physicalMemory
        self.__build_page_table__(npages)
        self.frame_counter = 0
        self.nframes = nframes
        self.frame2page = {}
        self.freeFrames = set(range(nframes))
        self.tlb = []
        self.tlb_size = tlb_size


    def __build_page_table__(self, npages):
        for i in range(npages):
            frame_id = -1
            mapped = False
            r = False
            m = False
            self.page_table[i] = (-1, mapped, r, m)

    def _adjust_tlb(self, page_id):
        if (page_id in self.tlb):
            self.tlb.remove(page_id)
        elif not (len(self.tlb) < self.tlb_size):
            self.tlb.pop(0)
        self.tlb.append(page_id)


    def access(self, page_id, write_mode):
        (frame_id, mapped, r, m) = self.page_table[page_id]
        
        in_tlb = 1 if (page_id in self.tlb) else 0

        if (in_tlb == 0): self._adjust_tlb(page_id)

        if mapped:
            self.phy_mem.access(frame_id, write_mode)
            self.page_table[page_id] = (frame_id, mapped, True, write_mode)
        else:
            if len(self.freeFrames) > 0:
                new_frame_id = self.freeFrames.pop()
                self.frame2page[new_frame_id] = page_id
                self.page_table[page_id] = (new_frame_id, True, True, write_mode)
                self.phy_mem.put(new_frame_id)
                self.phy_mem.access(new_frame_id, write_mode)
            else:
                evicted_frame = self.phy_mem.evict()
                # evicted_frame_id = evicted_frame
                evicted_frame_id = evicted_frame[0]
                io = evicted_frame[1]
                # assert type(evicted_frame_id) == int, "frameId returned by evict should be an int"
                page_id_out = self.frame2page.get(evicted_frame_id, None)
                assert page_id_out is not None, "frameId returned by evict should be allocated"

                #update page out
                self.page_table[page_id_out] = (-1, False, False, False)

                #allocate the new frame
                self.phy_mem.put(evicted_frame_id)
                #mudar mappeamento pagina in
                self.page_table[page_id] = (evicted_frame_id, True, True, write_mode)
                #update frame2page
                self.frame2page[evicted_frame_id] = page_id
                self.phy_mem.access(evicted_frame_id, write_mode)
                return (0 if in_tlb == 1 else 1, 0 if in_tlb == 1 else io, in_tlb)
        return (0, 0, in_tlb)

if __name__ == "__main__":

    # Usage: python $0 num_pages num_frames algo clock
    num_pages = int(sys.argv[1])
    num_frames = int(sys.argv[2])
    alg = sys.argv[3]
    clock = int(sys.argv[4])
    tlb_size = int(sys.argv[5])

    mapNameToClass = {
        "fifo": FIFO,
        "nru": NRU,
        "lru": LRU,
        "aging": Aging,
        "second-chance": SecondChance,
		"belady": Belady
    }

    # read workload from input file
    # workload = []
    # log_future = {}
    # time = 0
    # for line in sys.stdin.readlines():
    #     time += 1
    #     page_id, mode = line.split()
    #     page_id = int(page_id)
    #     try:
    #         log_future[page_id].append(time)
    #     except:
    #         log_future[page_id] = [time]

    #     workload.append((page_id, mode == "w"))

    workload = []
    log_future = {}
    time = 0
    for line in sys.stdin.readlines():
        time += 1
        page_id, mode = line.split()
        page_id = int(page_id)
        try:
            log_future[page_id].append(time)
        except:
            log_future[page_id] = deque([time])

        workload.append((page_id, mode == "w"))

    # setup simulation
    if alg == "belady":
        # phyMem = mapNameToClass[alg](log_future)
        phyMem = mapNameToClass[alg](log_future, workload)
    else:
        phyMem = mapNameToClass[alg]()
    vMem = VirtualMemory(num_pages, num_frames, phyMem, tlb_size)

    # fire
    count = 0
    fault_counter = 0
    io = 0
    tlb_counter = 0
    for load in workload:
        # call we fired clock (say, clock equals to 100) times, we tell the physical_mem to react to a clock event
        if count % clock == 0:
            phyMem.clock()
        count += 1
        page_id, acc_mode = load
        # accessed = vMem.access(page_id, acc_mode)
        # fault_counter += accessed
        accessed = vMem.access(page_id, acc_mode)
        fault_counter += accessed[0]
        io += accessed[1]
        tlb_counter += accessed[2]

    #TODO
    # collect results
    # write output
    print fault_counter, " ".join(sys.argv[1:]), io, tlb_counter
