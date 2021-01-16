import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import numpy as np
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class graphConclude():
    def __init__(self, _upper):
        #self._QMainWindow = QMainWindow
        #self.setupUi(self)

        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        _upper.ConcHistoryGraph.addWidget(self.canvas)
        #self._form_class.ConcHistoryGraph.addWidget(self.canvas)
        self.plotConcHistoryGraph()

    def plotConcHistoryGraph(self):
        x = np.arange(0, 100, 1)
        y = np.sin(x)

        ax = self.fig.add_subplot(111)
        ax.plot(x, y, label="label")
        ax.set_xlabel("x_axis")
        ax.set_xlabel("y_axis")

        ax.set_title("my graph")
        ax.legend()
        self.canvas.draw()
