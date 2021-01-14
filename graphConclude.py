import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import numpy as np
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

form_class = uic.loadUiType('analyze.ui')[0]

class graphConclude(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #self.setupUi(self)
        """
        
        self.cw.fig = plt.Figure()
        self.cw.canvas = FigureCanvas(self.fig)
        self.cw.ConcHistoryGraph.addWidget(self.canvas)
        self.cw.plotConcHistoryGraph()

    def plotConcHistoryGraph(self):
        x = np.arange(0, 100, 1)
        y = np.sin(x)

        ax = self.cw.fig.add_subplot(111)
        ax.plot(x, y, label="label")
        ax.set_xlabel("x_axis")
        ax.set_xlabel("y_axis")

        ax.set_title("my graph")
        ax.legend()
        self.cw.canvas.draw()
        """