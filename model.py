from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from random_agent import RandomAgent
from trash_agent import TrashAgent


class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height):
        self.num_agents = N
        self.num_trash = 20
        self.remaining_trash = self.num_trash
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True
        self.visited_cells = set()
        self.time_limit = 500
        self.current_steps = 0
        self.datacollector = DataCollector( 
            agent_reporters={
                "Pasos por Roomba": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0,
            },
            model_reporters={
                "Trash": lambda m: self.get_remaining(m) / self.num_trash * 100,
                "Cleaned": lambda m: self.get_remaining(m, getNormal=True) / self.num_trash * 100,
            }
        )

        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Añadir todas las roombas en la celda (1,1)
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            pos = pos_gen(1, 1)
            self.grid.place_agent(a, pos)

        # Añadir agentes basura
        for i in range(self.num_trash):
            a = TrashAgent(i+100, self) 
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)
        
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        if self.running:
            self.schedule.step()
            self.datacollector.collect(self)
            self.current_steps += 1

        # Terminar cuando se llegue al límite de tiempo
        if self.current_steps >= self.time_limit or self.get_remaining(self) == 0:
            self.running = False


    @staticmethod
    def get_remaining(model, getNormal=False):
        """
        Helper method to count remaining trash agents in a given model.
        """
        if getNormal:
            return model.num_trash - model.remaining_trash

        return model.remaining_trash
