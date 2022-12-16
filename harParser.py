import twitterNetwork
import youTubeNetwork
import sixNetwork
import originExtractor

twitterDictionary = twitterNetwork.logDictionary
youTubeDictionary = youTubeNetwork.logDictionary
sixDictionary = sixNetwork.logDictionary

curDictionary = sixDictionary
curHostName = "61040-fa22.github.io"

def extractInformation(logDictionary):

    entries = logDictionary["log"]["entries"]
    resourceTypes = []
    protocols = []
    hostnames = []
    times = []
    requestURLs = []
    responseCORSheader = []

    #print(len(logDictionary["log"]["entries"]))

    for entry in entries:

        resourceTypes.append(entry["_resourceType"])
        times.append(float(entry["time"]))

        url = entry["request"]["url"]
        requestURLs.append(url)

        protocols.append(originExtractor.get_protocol(url))

        hostnames.append(originExtractor.get_hostname(url,''))
        isCORS = False
        for header in entry["response"]["headers"]:
            if header["name"] == "access-control-allow-origin":
                responseCORSheader.append(1)
                isCORS = True

        if not isCORS:
            print(requestURLs[-1])
            responseCORSheader.append(0)

    return resourceTypes, protocols, hostnames, times, requestURLs, responseCORSheader


def getTimesByResourceTypes(resourceTypes, times, responseCORSheader):
    typesTime = dict() # {type: list of times it took to complete request that rendered type}
    types = dict() # {type: amount of type}
    typeTimeAverage = dict() # {type: averageTime}

    for i in range(len(responseCORSheader)):
        #checking if cors
        if responseCORSheader[i] == 1:
            resourceType = resourceTypes[i]
            time = times[i]

            #updating frequency of type
            if resourceType not in types:
                types[resourceType] = 0
            types[resourceType] += 1

            #adding time of new request according to resource type it fetches
            if resourceType not in typesTime:
                typesTime[resourceType] = []
            typesTime[resourceType].append(time)

    for resourceType in typesTime:
        typeTimeAverage[resourceType] = sum(typesTime[resourceType])/types[resourceType]

    
    return typesTime, types, typeTimeAverage





resourceTypes, protocols, hostnames, times, requestURLs, responseCORSheader = extractInformation(curDictionary)


typesTime, types, typeTimeAverage = getTimesByResourceTypes(resourceTypes, times, responseCORSheader)

def getProtocolBasedCORS(protocols, protocol):
    count = 0

    for word in protocols:
        if word != protocol:
            count += 1

    return count

def getHostnameBasedCORS(hostnames, hostname):
    count = 0

    for word in hostnames:
        print(word)
        if word != hostname:
            count += 1

    return count

print(types)
print(typeTimeAverage)
print(getProtocolBasedCORS(protocols,"https"))
print(getHostnameBasedCORS(hostnames, curHostName))