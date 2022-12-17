import twitterNetwork
import youTubeNetwork
import sixNetwork
import netflixNetwork
import originExtractor
import cnnNetwork

twitterDictionary = twitterNetwork.logDictionary
youTubeDictionary = youTubeNetwork.logDictionary
sixDictionary = sixNetwork.logDictionary
netflixDictionary = netflixNetwork.logDictionary
cnnDictionary = cnnNetwork.logDictionary
curDictionary = netflixDictionary
curHostName = "netflix.com"

def extractInformation(logDictionary):

    entries = logDictionary["log"]["entries"]
    resourceTypes = []
    protocols = []
    hostnames = []
    times = []
    requestURLs = []
    responseCORSheader = []
    numberOfCORSRequests = 0
    print("Number of requests")
    print(len(entries))
    #print(len(logDictionary["log"]["entries"]))

    for entry in entries:

        resourceTypes.append(entry["_resourceType"])
        times.append(float(entry["time"]))

        url = entry["request"]["url"]
        requestURLs.append(url)

        protocols.append(originExtractor.get_protocol(url))

        hostnames.append(originExtractor.get_hostname(url,''))
        isCORS = False
        for header in entry["request"]["headers"]:
            if header["name"].lower() == "sec-fetch-site" and header["value"] == "cross-site":
                responseCORSheader.append(1)
                numberOfCORSRequests += 1
                isCORS = True

        if not isCORS:
            #print(requestURLs[-1])
            responseCORSheader.append(0)

    print("Number of CORS Requests")
    print(numberOfCORSRequests)
    return resourceTypes, protocols, hostnames, times, requestURLs, responseCORSheader


def getTimesByResourceTypes(resourceTypes, times, responseCORSheader):
    typesTime = dict() # {type: list of times it took to complete request that rendered type}
    types = dict() # {type: amount of type}
    typeTimeAverage = dict() # {type: averageTime}
    typePercentage = dict()
    print("numCors")
    numCORS = 0
    for i in range(len(responseCORSheader)):
        #checking if cors
        if responseCORSheader[i] == 1:
            numCORS += 1
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

    print(numCORS)
    for resourceType in typesTime:
        typeTimeAverage[resourceType] = sum(typesTime[resourceType])/types[resourceType]
        typePercentage[resourceType] = types[resourceType]/numCORS
    
    return typesTime, types, typeTimeAverage, typePercentage





resourceTypes, protocols, hostnames, times, requestURLs, responseCORSheader = extractInformation(curDictionary)


typesTime, types, typeTimeAverage, typePercentage = getTimesByResourceTypes(resourceTypes, times, responseCORSheader)

def getProtocolBasedCORS(responseCORSheader, protocols, protocol):
    count = 0

    for i in range(len(responseCORSheader)):
        if responseCORSheader[i] == 1 and protocols[i] != protocol:
            count += 1

    return count

def getHostnameBasedCORS(responseCORSheader, hostnames, hostname):
    count = 0

    for i in range(len(responseCORSheader)):
        if responseCORSheader[i] == 1 and hostnames[i] != hostname:
            count += 1

    return count



print(types)
print(typeTimeAverage)
print(getProtocolBasedCORS(responseCORSheader, protocols,"https"))
print(getHostnameBasedCORS(responseCORSheader, hostnames, curHostName))
print("Percentage of CORS requests dedictated to render a resource Type")
print(typePercentage)