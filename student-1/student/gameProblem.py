## v2.11
## Javier Huertas (2017-18)
## Alejandro Cervantes (2017-18)
## To be used with python2.7
## Open source. Distributed as-is

'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
   
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None


    #
    # SOLUCION AL PROBLEMA BASICO
    #
    # --------------- Metodos Comunes a todo problema SearchProblem -----------------
    
    
    def actions(self, state):
        
        '''Returns a LIST of the actions that may be executed in this state
        '''

	arriba=list(state[0])
	arriba[1]=arriba[1]+1

	derecha=list(state[0])
	derecha[0]=derecha[0]+1

	abajo=list(state[0])
	abajo[1]=abajo[1]-1


	izquierda=list(state[0])
	izquierda[0]=izquierda[0]-1

	acciones = ['North', 'South', 'East', 'West']

	if(self.POSITIONS.get("sea")):

		if arriba[1] >= self.CONFIG['map_size'][1] or tuple(arriba) in self.POSITIONS.get("sea"):
				acciones.remove('North')
	
		if abajo[1] < 0 or tuple(abajo) in self.POSITIONS.get("sea"):
				acciones.remove('South')
	
		if derecha[0] >= self.CONFIG['map_size'][0] or tuple(derecha) in self.POSITIONS.get("sea"):
				acciones.remove('East')
		
		if izquierda[0] < 0 or tuple(izquierda) in self.POSITIONS.get("sea"):
				acciones.remove('West')
	            
		return acciones

	if arriba[1] >= self.CONFIG['map_size'][1]:
			acciones.remove('North')
	
	if abajo[1] < 0:
			acciones.remove('South')
	
	if derecha[0] >= self.CONFIG['map_size'][0]:
			acciones.remove('East')
		
	if izquierda[0] < 0:
			acciones.remove('West')
	
	return acciones
    

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''

	if(action == 'North'):
		nueva_posicion=(state[0][0],state[0][1]+1)		
		nuevas_metas=state[1]
		if nueva_posicion in state[1]:
			a = list(state[1])
			a.remove(nueva_posicion)
			nuevas_metas = tuple(a)
		state_final=(nueva_posicion,nuevas_metas)
	
	if(action == 'South'):
		nueva_posicion=(state[0][0],state[0][1]-1)		
		nuevas_metas=state[1]
		if nueva_posicion in state[1]:
			b = list(state[1])
			b.remove(nueva_posicion)
			nuevas_metas = tuple(b)
		state_final=(nueva_posicion,nuevas_metas)

	if(action == 'East'):
		nueva_posicion=(state[0][0]+1,state[0][1])		
		nuevas_metas=state[1]
		if nueva_posicion in state[1]:
			c = list(state[1])
			c.remove(nueva_posicion)
			nuevas_metas = tuple(c)
		state_final=(nueva_posicion,nuevas_metas)

	if(action == 'West'):
		nueva_posicion=(state[0][0]-1,state[0][1])		
		nuevas_metas=state[1]
		if nueva_posicion in state[1]:
			d = list(state[1])
			d.remove(nueva_posicion)
			nuevas_metas = tuple(d)
		state_final=(nueva_posicion,nuevas_metas)

        return state_final

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        return state == self.GOAL

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
	coste=1

        return coste	

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''

	heuristica=(abs(state[0][0] - self.AGENT_START[0]) +  abs(state[0][1] -  self.AGENT_START[1]) + len(state[1]))
	
        return heuristica


    def setup (self):
        initial_state = (self.AGENT_START, tuple(self.POSITIONS.get("goal")))
        final_state= (self.AGENT_START, tuple())
        algorithm= astar
            
        return initial_state,final_state,algorithm


        
    
    # --------------- NO TOCAR DESDE AQUI  -----------------
    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        
        # Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
        if self.mapInitialization(map,positions,conf,aiBaseName):
    
            initial_state,final_state,algorithm = self.setup()
            
            self.INITIAL_STATE=initial_state
            self.GOAL=final_state
            self.ALGORITHM=algorithm
            super(GameProblem,self).__init__(self.INITIAL_STATE)
            
            return True
        else:
            return False
        
    # END initializeProblem 


    def mapInitialization(self,map,positions,conf,aiBaseName):
        # Creates lists of positions from the configured map
        # The initial position for the agent is obtained from the first and only aiBaseName tile
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf

        if 'agentInit' in conf.keys():
            self.AGENT_START = tuple(conf['agentInit'])
        else:                    
            if aiBaseName in self.POSITIONS.keys():
                if len(self.POSITIONS[aiBaseName]) == 1:
                    self.AGENT_START = self.POSITIONS[aiBaseName][0]
                else:
                    print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(aiAgentName,mapaPosiciones[aiAgentName]))
                    return False
            else:
                print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(aiBaseName))
                return False
        
        return True
    

