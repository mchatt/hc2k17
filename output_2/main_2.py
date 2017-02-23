import numpy
import sys
import getopt

class Input:
    V = 0
    E = 0
    R = 0
    C = 0
    X = 0
    videoSize = None
    endpointArray = None
    requestArray = None

class Output:
    nbCacheUsed = 0
    cacheContent = None # [ [1],[],[2,4] ][ [1],[],[2,4] ]

class endpoint:
    latencyDatacenter = 0
    numberConnectionToCache = 0
    latencyToCache = None # [[cacheid,latency],[cacheid,latency]]
    
def print_endpoint(e):
    print(e.latencyDatacenter)
    print(e.latencyToCache)

class request:
    videoId = 0
    endpointId = 0
    nbRequest = 0

def print_request(r):
    print(r.videoId)
    print(r.endpointId)
    print(r.nbRequest)

def possibleToAddVideo(iInput, videoId, cacheId, remainingSize):
    return (remainingSize[int(cacheId)] >= int(iInput.videoSize[int(videoId)]))

def compute(iInput):
    res = Output()
    res.cacheContent = [[] for i in range(iInput.C)]

    remainingSize = [iInput.X] * iInput.C
    
    for req in iInput.requestArray:
        for cache in iInput.endpointArray[req.endpointId].latencyToCache:
            cacheId = int(cache[0])
            if possibleToAddVideo(iInput, req.videoId, cacheId, remainingSize) and req.videoId not in res.cacheContent[cacheId]:
                remainingSize[cacheId] -= int(iInput.videoSize[req.videoId])
                res.cacheContent[cacheId].append(req.videoId)
                break
            else:
                continue

    res.nbCacheUsed = iInput.C - res.cacheContent.count([])
    return res

def parseInput(iInputFilePath):
    with open(iInputFilePath) as f:
        content = f.readlines()
    res = Input()
    # line 1
    l1s = content[0].split()
    res.X = int(l1s[0])
    res.E = int(l1s[1])
    res.R = int(l1s[2])
    res.C = int(l1s[3])
    res.X = int(l1s[4])
    #print(str(res.V)+' '+str(res.E)+' '+str(res.R)+' '+str(res.C)+' '+str(res.X))
    res.videoSize = content[1].split()
    i = 2
    res.endpointArray = []
    for x in range(0,res.E):
        e = endpoint()
        e.latencyDatacenter = int(content[i].split()[0])
        e.numberConnectionToCache = int(content[i].split()[1])
        i = i+1
        e.latencyToCache = []
        for y in range(0,e.numberConnectionToCache):
            e.latencyToCache.append(content[i].split())
            i = i+1
        e.latencyToCache.sort(key=lambda x: x[1])
        res.endpointArray.append(e)
        #print_endpoint(e)
    
    res.requestArray = []
    for x in range(0,res.R):
        r = request()
        r.videoId = int(content[i].split()[0])
        r.endpointId = int(content[i].split()[1])
        r.nbRequest = int(content[i].split()[2])
        i = i+1
        res.requestArray.append(r)
        #print_request(r)
    
    res.requestArray.sort(key=lambda x:float(x.nbRequest)/float(res.videoSize[x.videoId]), reverse=True)
    return res

def formatOutput(iOutput, iOutputFilePath):
    f = open(iOutputFilePath, 'w')
    f.write(str(iOutput.nbCacheUsed)+'\n')
    for cacheId, cache in enumerate(iOutput.cacheContent):
        if not cache :
            continue
        s = ' '.join(str(x) for x in cache)
        f.write(str(cacheId)+' '+s+'\n')
    f.close()

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   inp = parseInput(inputfile)
   output = compute(inp)
   formatOutput(output, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
