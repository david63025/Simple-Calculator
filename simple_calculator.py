#! /usr/bin/env python

#-----------------------------------------------------------------------#
#                                                                       #
# Copyright (C) 2013, David A. Hall                                     #
#                     Eureka, MO USA                                    #
# This program is free software. You can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License Version 2.     #
#   This program is distributed in the hope that it is useful,          #
#   but WITHOUT ANY WARRANTY IMPLIED OR OTHERWISE.                      #
#                                                                       #
#-----------------------------------------------------------------------#

from __future__ import division
import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = "0.3.0"
__author__ = "David Hall"
__last_update__ = "01 Dec 2014"


class SimpleCalc(QMainWindow):

    def __init__(self, parent=None):
        super(SimpleCalc, self).__init__(parent)
        self.setWindowTitle("Simple Calculator")
        self.setWindowIcon(QIcon("simple_calculator.xpm"))

        self.eng_units = {
            'p': '-12', 'n': '-09', 'u': '-06', 'm': '-03',
            'k': '03', 'M': '06', 'G': '09', 'T': '12'}
        self.units = (
            'p', 'n', 'u', 'm', '', 'k', 'M', 'G', 'T')
        self.display = (
            {'mode': 'eng', 'digits': 4})
            # Controls appearance of results in stack, doesn't change
            #   internal representation of a number. Full precision is
            #   maintained.
            # Available modes are fix, eng, and sci.
            # Digits is number of significant digits

        self.history = QTextBrowser()
        self.history.setFixedHeight(385)
        self.setCentralWidget(self.history)

        self.labels = list("hgfedcbazyx")
        self.register = QTableWidget(len(self.labels), 1)
        self.register.setHorizontalHeaderLabels(("Register",))
        self.register.setVerticalHeaderLabels(self.labels)
        self.register.setFixedWidth(125)
        self.register.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        self.register.setAlternatingRowColors(True)
        self.getRegister()

        dockwidget = QDockWidget("", self)
        dockwidget.setAllowedAreas(Qt.RightDockWidgetArea)
        dockwidget.setWidget(self.register)
        self.addDockWidget(Qt.RightDockWidgetArea, dockwidget)

        self.input = QLineEdit("Input Expression & Press Enter")
        self.connect(self.input, SIGNAL("returnPressed()"), self.getInput)

        btnQuit = QPushButton(QIcon("stock_cancel.png"), "Quit")
        self.connect(btnQuit, SIGNAL("clicked()"), app.quit)

        toolbar = QToolBar()
        toolbar.setAllowedAreas(Qt.BottomToolBarArea)
        toolbar.addWidget(QLabel(" INPUT:  "))
        toolbar.addWidget(self.input)
        toolbar.addWidget(btnQuit)
        self.addToolBar(Qt.BottomToolBarArea, toolbar)

    def getInput(self):
        text = unicode(self.input.text())
        self.updateUI(text)
        return

    def updateUI(self, text):
        try:
            result = eval(text)
        except NameError as error:
            var = error.message.split("'")[1].lower()
            if var in self.labels:
                index = self.labels.index(var)
                item = self.register.takeItem(index, 0)
                text = text.replace(var, item.text())
                self.register.setItem(index, 0, item)
                self.updateUI(text)
            else:
                self.history.append(
                    "<font color=red>%s is invalid!</font>" % text)
        except:
            self.history.append(
                "<font color=red>%s is invalid!</font>" % text)

        else:
                self.history.append("%s = <b>%s</b>" % (text, result))
#               TODO: put result in global clipboard so other apps can use
                self.pushRegister(result)
                self.input.setFocus(True)
                self.input.selectAll()
        return

    def getRegister(self):
        for i in range(len(self.labels)):
#            item = QTableWidgetItem("< %s >" % self.labels[i])
            item = QTableWidgetItem("--")
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.register.setItem(i, 0, item)
        return

    def pushRegister(self, result):
        for row in range(len(self.labels)):
            self.register.setItem(row, 0, self.register.takeItem(row + 1, 0))
##        result = self.toEngNotation(result)
        item = QTableWidgetItem(str(result))
        item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.register.setItem(row, 0, item)
        return

    def toEngNotation(self, number, digits=5):
        if (number > -1000. and number < 1000.):
            return number
        man, exp = ('%e' % number).split('e')
        man = float(man)
        man = round(man, digits - 1)
        exp = int(exp)
        while (exp % 3):
            exp -= 1
            man *= 10
        man = str(man)
        print(man, exp, 4 + exp//3)
        return ('%s%s' % (man, self.units[4 + exp // 3]))

    def fromEngNotation(self, number):
        pass

# end of class Form

if __name__ == '__main__':
#    if os.getenv('HOME'):
#        simcalcrc = os.path.join(os.getenv('HOME'), '.simcalcrc')
#    elif os.getenv('APPDATA'):
#        simcalcrc = os.path.join(os.getenv('APPDATA'), 'simcalcrc')
#    else:
#        simcalcrc = ''
#
#    if os.access(simcalcrc, os.F_OK|os.R_OK):
#        fp = open(simcalcrc, 'r')
#        calculator = cPickle.load(fp)
#        fp.close()
#    else:
#         calculator = SimpleCalc()

    app = QApplication(sys.argv)
    calculator = SimpleCalc()
    calculator.show()
    calculator.input.setFocus(True)
    calculator.input.selectAll()
    app.exec_()
