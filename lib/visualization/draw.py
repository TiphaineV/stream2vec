from lib.Stream import Stream
from lib.visualization.FigPrinter import FigPrinter
from IPython.display import Image


def draw(s, printer=FigPrinter):
    """
        Draws a given stream S. Simplified version of streamfig.
    """

    _printer = printer(alpha=s.T["alpha"], omega=s.T["omega"], streaming=False)
    for u in s.nodes():
        _printer.addNode(u)
    
    for l in s.E:
        _printer.addLink(l["u"], l["v"], l["b"], l["e"])

    _printer.save("test.fig")
    del _printer
    from subprocess import call
    call("fig2dev -Lpng test.fig > test.png", shell=True)
    return Image("test.png")

