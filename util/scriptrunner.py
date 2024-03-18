import util.driversetup as ds
from prov.graph import Graph

def runList(database, scriptList, saveToDisk, actions):#MODIFIED: ADDED actions argument, AMMENDED in webserver.py too
    '''
        Runs a list of scripts and gathers provenance on each one
    '''
    graph = Graph(database.generate_graph_id())
    for action in actions: #ADDED
    	graph.add_action(action) #ADDED
    database.start_capture(graph)
    for script in scriptList:
        run(database, script, saveToDisk)
    database.stop_capture(graph, saveToDisk)


def run(database, script, saveToDisk):
    try:
        print("running " + str(script))
        fileRead = open(script).read()
        exec(fileRead)
    except FileNotFoundError as e:
        print(e)
        print("Can't open " + str(script))
