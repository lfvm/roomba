from model import RandomModel, TrashAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer

COLORS = {"Trash": "#00AA00", "Cleaned": "#880000"}


def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N":5, "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Pasos por Roomba", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()],
)

server = ModularServer(RandomModel, [grid, pie_chart, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()