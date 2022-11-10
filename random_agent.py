from mesa import Agent
from trash_agent import TrashAgent

class RandomAgent(Agent):
    """
    Agente que se mueve de manera aleatoria
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0


    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, 
            include_center=True
        )

        trashNeighbor = self.get_neighbor_trash()
        unvisited_cell = self.get_unvisited_neighbor()
        
        if trashNeighbor:
            next_move = trashNeighbor

        elif unvisited_cell:
            next_move = unvisited_cell

        else:
            next_move = self.random.choice(possible_steps)

        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1


    
    
    def step(self):

        # Agregar celda actual a celdas visitadas
        self.model.visited_cells.add(self.pos)

        # Buscar basura en mi celda
        trash = self.get_trash_in_my_cell()
        
        # Si hay basura quitala
        if trash:
            self.remove_trash(trash)

        # Si no hay basura muevete
        else:
            self.move()
    


    def get_trash_in_my_cell(self) -> bool:

        # Obtener todas las celdas de mi alrededor y de mi celda
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=False, 
            include_center=True
        ) 
        
        # Buscar en mi celda actual 
        if len(neighbors) > 0:
            for n in neighbors:
                # Si el agente vecino está en mi celda y es basura
                if n.pos == self.pos and isinstance(n, TrashAgent):
                    return n

        return None
    

    def get_neighbor_trash(self): 
        
        # Checks for grid cells that are ocupied by a trash cell 
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True, 
            include_center=False
        ) 
        
        trash = None
        for n in neighbors:
            if isinstance(n, TrashAgent):
                trash = n.pos
                break
        
        return trash
    
    def get_unvisited_neighbor(self):

        neighbor_cells = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, 
            include_center=False
        )

        for cell in neighbor_cells:
            if not cell in self.model.visited_cells:
                return cell

        return None


    def remove_trash(self, trash):
        self.model.remaining_trash -= 1
        self.model.grid.remove_agent(trash)

        
