from model import RandomModel, TrashAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

COLORS = {"Trash": "#f54242", "Cleaned": "#109130"}

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "#1c87eb",
                 "r": 0.5}

    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "#f54242"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2

    return portrayal

model_params = {
    "N": UserSettableParameter("slider", "N Roombas", 1, 1, 5, 1),
    "timeLimit": UserSettableParameter("slider", "Step Limit", 50, 50, 500, 10), 
    "width":10, 
    "height":10
}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Gráfica movimientos por roomba
bar_chart = BarChartModule(
    [{"Label":"Pasos por Roomba", "Color":"#1c87eb"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

# Gráfica porcentaje de basura limpiada
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()],
)

tree_chart = ChartModule(
    [{"Label": "Cleaned", "Color": COLORS["Cleaned"]}],
)

server = ModularServer(RandomModel, [grid, bar_chart, pie_chart, tree_chart], "Roomba", model_params)
                       
server.port = 8521 # The default
server.launch()