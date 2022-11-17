from ISA import ISA_rho
from interpolation import get_alpha, get_Lspan, get_dispan
from Weight_diagram import get_Weight
import numpy as np
import scipy as sp
from Torque_diagram import torque_diagram
from Shear_diagram import shear_diagram

class LoadCase:


    def __init__(self, n: float, W: float, v: float, h: float) -> None:
        self.n = n
        self.w = W
        self.l = 1.1*W*n
        self.h = h
        self.v = v
        self.s = 57.418137

        #define flow conditions
        self.rho = ISA_rho(self.h)
        self.cld = self.l/(0.5*self.rho*self.v**2*self.s)
        self.alpha = get_alpha(self.cld)
    
    def shear_diagram(self)->None:
        shear_diagram(self.alpha, self.v, self.rho)

    def torque_diagram(self)-> None:
        torque_diagram(self.alpha, self.v, self.rho)

load1 = LoadCase(1, 162550, 200, 12500)
load1.torque_diagram()