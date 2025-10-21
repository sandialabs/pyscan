from functools import partial
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from multiprocessing import Manager, Process
import numpy as np
import os
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMainWindow, QFrame, \
    QGridLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QFileIconProvider, \
    QApplication
import sys
from time import sleep


def voltage_response(v1, v2):
    """
    Paraboloid function to optimize.
    """
    return (v1 - 4)**2 + (v2 - 6)**2


def run_scan(x, y):
    for _ in range(10):
        sleep(1)
        x.append(np.random.uniform(low=0., high=10.))
        y.append(np.random.uniform(low=0., high=10.))


def set_file_icon(item, fpath):
    fileInfo = QFileInfo(fpath)
    iconProvider = QFileIconProvider()
    icon = iconProvider.icon(fileInfo)
    item.setIcon(0, icon)


def compute_project_structure_tree(tree, base_path='.'):
    for f in os.listdir(base_path):
        f_path = os.path.join(base_path, f)
        tree_item = QTreeWidgetItem(tree, [os.path.basename(f)])
        if os.path.isdir(f_path):
            compute_project_structure_tree(tree_item, base_path=f_path)
        set_file_icon(tree_item, f_path)


class ApplicationWindow(QMainWindow):
    """
    PyQt5 main window
    """

    def __init__(self):

        # GUI Window
        super().__init__()
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle("Pyscan GUI")
        self.frame = QFrame(self)
        self.frame.setStyleSheet("QWidget { background-color: #eeeeec; }")

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("&new")
        file_menu.addAction("&open")
        file_menu.addAction("&save")
        file_menu.addAction("&exit")
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("&edit placeholder")
        options_menu = menu_bar.addMenu("&Options")
        options_menu.addAction("&options placeholder")
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction("&help placeholder")

        self.layout = QGridLayout()
        self.layout.setColumnStretch(1, 4)
        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        # Scan button
        self.scan_push = QPushButton()
        self.scan_push.setText("scan0")

        # Backup filetree
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel("Project Explorer")
        compute_project_structure_tree(self.file_tree)

        manager = Manager()

        self._x = manager.list()
        self._y = manager.list()

        # Matplotlib Figure
        self.fig_canvas = ApplicationFigureCanvas(self._x, self._y)

        self.layout.addWidget(self.scan_push, 0, 0, 1, 1)
        self.layout.addWidget(self.fig_canvas, 1, 1, 2, 1)
        self.layout.addWidget(NavigationToolbar2QT(self.fig_canvas, self), 0, 1, 1, 1)
        self.layout.addWidget(self.file_tree, 0, 2, 3, 1)

        self.show()

    def scan_callback(self):
        p = Process(target=run_scan, args=(self._x, self._y))
        p.start()


class ApplicationFigureCanvas(FigureCanvasQTAgg):
    """
    FigureCanvas Widget for live plot
    """

    def __init__(self, x, y):

        super().__init__(Figure(figsize=(5, 5), dpi=100))

        self._ax = self.figure.subplots()
        self._ax.set_xlim(0, 10)
        self._ax.set_ylim(0, 10)

        xmg, ymg = np.mgrid[0:10:.01, 0:10:.01]
        zmg = np.array(voltage_response(np.ravel(xmg), np.ravel(ymg)))
        zmg = zmg.reshape(xmg.shape)
        self._ax.pcolormesh(xmg, ymg, zmg, cmap='gist_heat')

        self._x = x
        self._y = y
        self._scatter = self._ax.scatter(self._x, self._y)

        self._ani = FuncAnimation(fig=self.figure,
                                  func=partial(self._update_canvas, scatter=self._scatter, x=self._x, y=self._y),
                                  frames=None, init_func=self._init_canvas, blit=True, save_count=100, interval=1e3)

    def _update_canvas(self, frame, scatter, x, y):
        scatter.set_offsets(np.c_[x, y])
        return scatter,

    def _init_canvas(self):
        return self._scatter,


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = ApplicationWindow()
    app.scan_push.clicked.connect(app.scan_callback)
    qapp.exec_()
