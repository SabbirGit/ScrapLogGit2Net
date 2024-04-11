# Module to export the collaboration network to different SNA tool formats 
# First implementation to uciNet for WebKit SNA ACM SIG MIS paper - on this file 
# Second implementation to GraphML (VISIONE) for OpenStack SNA - Open Journal special issue  - using the exportgraphml form


from __future__ import absolute_import
from __future__ import print_function
import sys
import re
import csv
from datetime import * 

import exportGraphml

# Replace '@' and '.' by "AT" and "DOT" 
def clearDotsAndAts(contribEmail):

    #print ("clearing Strings From Dots and Ats from: [" + contribEmail+ "]")

    pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
 
    if (pattern.search(contribEmail)== None):
        print ("ERROR Contributor have an invalidName")
        exit()
    
    tmp= re.sub('\.','DOT' ,contribEmail)
    tmp= re.sub('\@','AT' ,tmp)

    return tmp

# Create a Network file (uciNet style) in raw text 
def createNetworkFile(tuplesList , outFileName):
    
    print ("")    
    print(("Writing network on file:[" + outFileName + "]"))

    f = open(outFileName, 'w')

    f.write('#File generated by scrapLog.py for research purposes \n')
    f.write('#Network connections by scrapping the changelog [' + sys.argv[1] + '] on ' + str(datetime.now()) + '\n')

    for connection in tuplesList:
        for author in connection[0]:
            f.write(clearDotsAndAts(author) + "\t")
        f.write('\n')

    f.write('END \n')
      

# Create a Atributes file (uciNet style) in raw text 
def createAtributesFile(logData , outFileName):
    
    print ("")    
    print(("Writing atributes on file:[" + outFileName + "]"))

    f = open(outFileName, 'w')

    f.write('#File generated by scrapLog.py for research purposes \n')
    f.write('#Node atributes by scrapping the changelog [' + sys.argv[1] + '] on ' + str(datetime.now()) + '\n')

    f.write('NAME\tAFFILIATION\n')

    for change in logData:
        f.write(clearDotsAndAts(change[0][1]))
        f.write('\t')
        f.write(change[0][2])
        f.write('\n')

    f.write('END \n')
      

# Create a Network file (uciNet style) in CSV file for spreedsheet software
def createNetworkFileCSV(tuplesList , outFileName):
    
    print ("")    
    print(("Writing network on file (.CSV):[" + outFileName + "]"))


    csvfile = open(outFileName, 'w')
    #csvfile = open(outFileName, 'wb')
    

    atribWriter = csv.writer(csvfile, dialect='excel', delimiter=' ') 
    
    # Print headers
    #csvfile.write('#File generated by scrapLog.py for research purposes \n')
    #csvfile.write('#Network connections by scrapping the changelog [' + sys.argv[1] + '] on ' + str(datetime.now()) + '\n')

    atribWriter.writerow(["NODE", "NODE"])
    for connection in tuplesList:
        tmp= []
        for author in connection[0]:
            tmp.append(clearDotsAndAts(author))

        atribWriter.writerow(tmp)


    csvfile.close()

    # Success 
    print((str(len(tuplesList)) +" network relationships writen down :[" + outFileName + "]"))

# Create a Atributes file (uciNet style) in CSV file for spreadsheat software
def createAtributesFileCSV(logData , outFileName):
    
    print ("")    
    print(("Writing atributes on file (.CSV):[" + outFileName + "]"))



    csvfile= open(outFileName, 'w')
    #csvfile= open(outFileName, 'wb')
    atribWriter = csv.writer(csvfile, dialect='excel',delimiter=' ')    
    
    # Print option file headers
    #atribWriter.writerow(['#File generated by scrapLog.py for research purposes'])
    #atribWriter.writerow(['#Node atributes by scrapping the changelog ['+ sys.argv[1] + '] on ' + str(datetime.now())])

    atribWriter.writerow(['NAME','AFFILIATION'])

    for change in logData:
        atribWriter.writerow([clearDotsAndAts(change[0][1]), change[0][2]])

    csvfile.close()       

    # Success 
    print((str(len(logData)) +" node atributes writen down :[" + outFileName + "]"))



############### By core companies #############
# As in http://blog.bitergia.com/2013/02/06/report-on-the-activity-of-companies-in-the-webkit-project/ 
# All coreCompanies + bot + core 

coreCompanies = ['apple', 'google', 'nokia', 'rim', 'igalia', 'intel', 'samsung', 'inf' , 'adobe' , 'torchmobile']

coreCompaniesColor =  []


# Create a Network file  (grouped by core companies) (uciNet style) in CSV file for spreedsheet software
def createNetworkByCoreCompaniesFileCSV(tuplesList , outFileName):
    print ("")    
    print(("Writing network (grouped by core companies) on file (.CSV):[" + outFileName + "]"))


    csvfile = open(outFileName, 'w')
    #csvfile = open(outFileName, 'wb')
    

    atribWriter = csv.writer(csvfile, dialect='excel', delimiter=' ') 
    atribWriter.writerow(["NODE", "NODE"])

    # Its equal right ? Just the the atributes change
    for connection in tuplesList:
        tmp= []
        for author in connection[0]:
            tmp.append(clearDotsAndAts(author))

        atribWriter.writerow(tmp)
   
    csvfile.close()



# Create a Atributes, grouped by core companies,  file (uciNet style) in CSV file for spreadsheat software
def createAtributesByCoreFileCSV(logData , outFileName):
    
    print ("")    
    print(("Writing atributes  (grouped by core companies) on file (.CSV):[" + outFileName + "]"))



    csvfile= open(outFileName, 'w')
    #csvfile= open(outFileName, 'wb')
    
    atribWriter = csv.writer(csvfile, dialect='excel',delimiter=' ')    
    
    # Print option file headers

    atribWriter.writerow(['NAME','AFFILIATION'])

    for change in logData:

        email = clearDotsAndAts(change[0][1])
        affiliation = change[0][2] 
        
        if affiliation in coreCompanies:
            atribWriter.writerow([email, affiliation])

        elif email == "webkit.review.bot@gmail.com":
            atribWriter.writerow([email, 'AutomatedBot'])
        elif affiliation not in coreCompanies:
            atribWriter.writerow([email, 'other'])
        else:
            print ("ERROR writing atributes grouped by company")
            exit()

    csvfile.close()


# export the grapth node and edges to GraphML format 
# Must be readable by Visione
def createGraphML(tuplesList,affiliations,outFileName):
    # iterator for nAf  

    print ("")    
    print(("\tExporting graph to file (.graphml):[" + outFileName + "]"))
    
    
    # verify arguments data
    ## verify tuplesList 
    
    if type(tuplesList) != list :
        print ("\tERROR collaboration tuplesList is not a list !!")
        exit()
    if len(tuplesList) < 1 :
        print ("\tERROR collaboration tuplesList is empty !!")
        exit()

    ## verify affiliations 
    #print ("\tCreateGraphMLaffiliations"+str(affiliations))
    
    if type(affiliations) != dict:
        print ("\tERROR affiliations are not a dictionary. Invalid format !!")
        exit()

    ## verify outFilename
    if type(outFileName) != str:
        print ("\tERROR outfilename must be a string")
        exit()
        
    if len(outFileName) < 5 :
        print ("\tERROR outfilename must be a long string. More than 5 caracters")
        exit()

    if outFileName[-8:] != ".graphML":
        print ("\tERROR outfilename must finish with .grapthML extenssion")
        exit()

    # open the export file 

    print ("")    
    print(("\tWriting grapthML file  (for VISIONE SNA tool or other ) on file:[" + outFileName + "]"))

    gfile= open(outFileName, 'w')

    
    # open XML headers 
    gfile.writelines(exportGraphml.graphml_header)
    
    # Add grapth atributes 

    gfile.writelines(exportGraphml.setNodeAntributeKey(0,"e-mail","string"))
    gfile.writelines(exportGraphml.setNodeAntributeKey(1,"color","string"))
    gfile.writelines(exportGraphml.setNodeAntributeKey(2,"affiliation","string"))
    

    # Open grapth 
    gfile.writelines(exportGraphml.graph_opener)
    
    # store the nodes id for each email/contributor
    tmpNodeId = {} 
    
    # interate over nodes
    nAf = 0
    for af in affiliations.items():
        email = af[0]
        afl = af[1]
        #print(exportGraphml.addNode(nAf,[(0,email),(1,"turquoise"),(2,afl)]))
        gfile.writelines(exportGraphml.addNode(nAf,[(0,email),(1,"turquoise"),(2,afl)]))
        tmpNodeId[email]=nAf
        nAf+=1


    # interate over the edges list and remove duplicates
    uniqueConnections = []
    
    for connection in tuplesList:
        #print ("connection="+str(connection))
        ((author1, author2)) = connection

        # Do not consider if author1 or author2 been already connected 1->2 or 2-< 1 
        if (author1, author2) not in uniqueConnections and (author2, author1) not in uniqueConnections:
            uniqueConnections.append((author1, author2))
        #else:
            #print(str((author1, author2)) + " already on the list of unique connections")
        
    #print(("uniqueConnections=[" + str(uniqueConnections) + "]"))

    # interate over the unique edges list 
    nTup = 0 
    for (emailFrom, emailTo) in uniqueConnections:
        nodeIdFrom = tmpNodeId[emailFrom]
        nodeIdTo = tmpNodeId[emailTo]
        #print((exportGraphml.addEdge("e"+str(nTup),nodeIdFrom,nodeIdTo)))
        gfile.writelines(exportGraphml.addEdge("e"+str(nTup),nodeIdFrom,nodeIdTo))
        nTup+=1 

        # There should be no arcs between the same mail/node/developer 
        if emailFrom == emailTo:
            print ("\t ERROR arc between the same mail/node/developer")
            print(("\t edge=["+str(edge)+"]"))
            sys.exit()
        # There should be no arcs between the same mail/node/developer 
        if nodeIdFrom == nodeIdTo:
            print ("\t ERROR arc between the same nodeid/developer")
            print(("\t edge=["+str(edge)+"]"))
            sys.exit()
            
    
    # Close grapth
    gfile.writelines(exportGraphml.graph_closer)

    # close XML document 
    gfile.writelines(exportGraphml.graphml_closer)

    # close the export file 
    gfile.close()

