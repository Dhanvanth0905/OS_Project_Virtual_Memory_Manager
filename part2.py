# import struct


def pageFaultHandler(pageNumber, tlb, pageTable, physicalMemory):
    if int(pageNumber) < 256:
        for i in range(256):
            if i in physicalMemory.keys():
                continue
            else:
                frameNumber = str(i)
                break

        backStore = open("BACKING_STORE.bin", "rb")
        physicalMemory[int(frameNumber)] = []

        for i in range(256):
            backStore.seek(int(pageNumber)*256+i)
            data = str(int.from_bytes(backStore.read(1), byteorder='big', signed=True))
            # data = struct.unpack("B", backStore.read(1))
            # physicalMemory[int(pageNumber)].insert(i, str(data))
            physicalMemory[int(frameNumber)].insert(i, data)

        backStore.close()
        print('Found page \"' + str(pageNumber) + '\" has data: ')
        print(physicalMemory[int(frameNumber)])
        print('in the backing store!\n')

    else:
        print('Page \"' + pageNumber + '\" is out of bound!')
        return

    updateTLB(pageNumber, frameNumber, tlb)
    updatePageTable(pageNumber, frameNumber, pageTable)


def updateTLB(pageNumber, frameNumber, tlb):
    # remove list[0], append new item at the end
    if len(tlb) < 16:
        tlb.append([pageNumber, frameNumber])
    else:
        # FIFO
        tlb.pop(0)
        tlb.append([pageNumber, frameNumber])

    print('Successfully update TLB with pageNumber: ' + str(pageNumber) + ', frameNumber: ' + str(frameNumber) + '!')


def updatePageTable(pageNumber, frameNumber, pageTable):
    # remove list[0], append new item at the end
    if len(pageTable) < 256:
        pageTable.append([pageNumber, frameNumber])
    else:
        pageTable.pop(0)
        pageTable.append([pageNumber, frameNumber])

    print('Successfully update pageTable table with pageNumber: ' + str(pageNumber) + ', frameNumber: ' + str(frameNumber) + '!')


def updateTLBCounter(latestEntryIndex, tlb):
    # remove list[latestEntryIndex], append new item at the end
    latestEntry = tlb[latestEntryIndex]
    tlb.pop(latestEntryIndex)
    tlb.append(latestEntry)

    print('Successfully update TLB with new sequence using LRU!')


def updatepageTableCounter(latestEntryIndex, pageTable):
    # remove list[latestEntryIndex], append new item at the end
    latestEntry = pageTable[latestEntryIndex]
    pageTable.pop(latestEntryIndex)
    pageTable.append(latestEntry)

    print('Successfully update page table with new sequence using LRU!')


def readPhysicalMemory(frameNumber, offset, physicalMemory):
    if (int(frameNumber) < 256) and (int(offset) < 256):
        data = physicalMemory[int(frameNumber)][int(offset)]
        print('Successfully read frameNumber \"' + str(frameNumber) + '\" offset \"' + str(offset) + '\"\'s data ')
        print(data)
        print('in the physical memory!\n')
        return data
    else:
        print('Frame number or offset is out of bound')


