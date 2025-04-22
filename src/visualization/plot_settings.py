import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

colors = cycler(color=plt.get_cmap("tab10").colors)  # ["b", "r", "g"]

mpl.style.use("ggplot")
mpl.rcParams["figure.figsize"] = (19, 10)
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["axes.grid"] = True
mpl.rcParams["grid.color"] = "lightgray"
mpl.rcParams["axes.prop_cycle"] = colors
mpl.rcParams["axes.linewidth"] = 5
mpl.rcParams["xtick.color"] = "black"
mpl.rcParams["ytick.color"] = "black"
mpl.rcParams["font.size"] = 18
mpl.rcParams["figure.titlesize"] = 25
mpl.rcParams["figure.dpi"] = 100
mpl.rcParams["axes.labelweight"] = "normal"  # Makes axis labels not bold
