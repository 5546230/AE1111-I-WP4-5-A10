import numpy as np
from load_case import LoadCase
from skin_stress import skin_stress
from Moment_of_inertia import get_ixx, get_J
from matplotlib import pyplot as plt
from spar_shear import shear_tor, shear_max

class design_option_compr:
    def __init__(
        self,
        a_stringer: float,
        n_stringer: int,
        a_t: float,
        t_f: float,
        t_r: float,
        t_s: float,
        option_nr: int
    ):
        self.sigma_yield = 275e6
        self.a_stringer = a_stringer
        self.n_stringer = n_stringer
        self.a_t = a_t
        self.t_f = t_f
        self.t_r = t_r
        self.t_s = t_s
        self.option_nr = option_nr

        self.a = np.sqrt(a_stringer*a_t/2)

        self.load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
        
        pass

    def compr_stringer(self, y: float) -> float:
        stress = skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringer, 1)
        return stress

    def compr_skin(self, y: float) -> float:
        stress = skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringer, 1)
        return stress

    def compr_front(self, y: float) -> float:
        moment = self.load.z2_moment(y)
        c = 3.49 -3.49*(1-0.372)/12 *y
        coord = c * 0.114/2
        ixx = get_ixx(y, self.t_f, self.t_r, self.t_s, self.n_stringer, self.a_stringer)
        
        stress = moment*coord/ixx

        return stress

    def compr_rear(self, y: float) -> float:
        moment = self.load.z2_moment(y)
        c = 3.49-3.49*(1-0.372)/12 *y
        coord = c * 0.063/2
        ixx = get_ixx(y, self.t_f, self.t_r, self.t_s, self.n_stringer, self.a_stringer)

        stress = moment*coord/ixx
        return stress

    def shear_stringer(self, y: float) -> float:
        torque_box = self.load.torque(y)
        j= get_J(y, self.t_f, self.t_r, self.t_s)

        stress = torque_box*self.a*self.a_t/j

        return stress
    
    def shear_skin(self, y: float) -> float:
        c = 3.49-3.49*(1-0.372)/12 *y
        A_enclosed= 0.5*(0.114*c + 0.063*c)*0.55*c
        torque = self.load.torque(y)
        stress = torque / (2*A_enclosed*self.t_s)
        return stress

    def shear_front(self, y: float) -> float:
        stress = shear_max(y, self.t_f, self.t_r, self.load)/1.45+shear_tor(y, self.t_f, self.load)
        return stress

    def shear_rear(self, y: float) -> float:
        stress = shear_max(y, self.t_f, self.t_r, self.load)/1.45+shear_tor(y, self.t_r, self.load)
        return stress
    
    def mos_stringer(self, y: float) -> float:
        stress_tensor = np.zeros((2,2))
        stress_tensor[0,1] = self.shear_stringer(y)
        stress_tensor[1,0] = self.shear_stringer(y)
        stress_tensor[1,1] = self.compr_stringer(y)

        a, b = np.linalg.eigvals(stress_tensor)
        tau_max = abs(a-b)/2
        mos = self.sigma_yield/2/tau_max

        return mos
    
    def mos_skin(self, y: float) -> float:
        stress_tensor = np.zeros((2,2))
        stress_tensor[0,1] = self.shear_skin(y)
        stress_tensor[1,0] = self.shear_skin(y)
        stress_tensor[1,1] = self.compr_skin(y)
        
        a, b = np.linalg.eigvals(stress_tensor)
        tau_max = abs(a-b)/2
        mos = self.sigma_yield/2/tau_max
        
        return mos
    
    def mos_front(self, y: float) -> float:
        stress_tensor = np.zeros((2,2))
        stress_tensor[0,1] = self.shear_front(y)
        stress_tensor[1,0] = self.shear_front(y)
        stress_tensor[1,1] = self.compr_front(y)
        
        a, b = np.linalg.eigvals(stress_tensor)
        tau_max = abs(a-b)/2
        mos = self.sigma_yield/2/tau_max
        
        return mos
    
    def mos_rear(self, y: float) -> float:
        stress_tensor = np.zeros((2,2))
        stress_tensor[0,1] = self.shear_rear(y)
        stress_tensor[1,0] = self.shear_rear(y)
        stress_tensor[1,1] = self.compr_rear(y)
        
        a, b = np.linalg.eigvals(stress_tensor)
        tau_max = abs(a-b)/2
        mos = self.sigma_yield/2/tau_max
        
        return mos
    
    def generate_plots(self):
        y_axis = np.linspace(0,11.98,100)

        mos_compr_stringer = []
        mos_compr_skin = []
        mos_compr_front = []
        mos_compr_rear = []

        for y in y_axis:
            mos_compr_stringer.append(self.mos_stringer(y))
            mos_compr_skin.append(self.mos_skin(y))
            mos_compr_front.append(self.mos_front(y))
            mos_compr_rear.append(self.mos_rear(y))
        print(np.min(mos_compr_rear), np.min(mos_compr_front), np.min(mos_compr_skin),np.min(mos_compr_stringer))
        
        fig, ax = plt.subplots(4, sharex= True)
        fig.set_figheight(8)
        fig.set_figwidth(8)

        ax[0].plot(y_axis, mos_compr_stringer)
        ax[1].plot(y_axis, mos_compr_skin)
        ax[2].plot(y_axis, mos_compr_front)
        ax[3].plot(y_axis, mos_compr_rear)

        ax[0].set_title('Stringer ')
        ax[1].set_title('Skin')
        ax[2].set_title('Front Spar')
        ax[3].set_title('Rear Spar')

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)
        ax[3].grid(True)

        ax[0].set_ylabel('Margin of Safety [-]')
        ax[1].set_ylabel('Margin of Safety [-]')
        ax[2].set_ylabel('Margin of Safety [-]')
        ax[3].set_ylabel('Margin of Safety [-]')

        ax[0].set_yscale('log')
        ax[1].set_yscale('log')
        ax[2].set_yscale('log')
        ax[3].set_yscale('log')
        
        ax[0].set_ylim(1)
        ax[1].set_ylim(1)
        ax[2].set_ylim(1)
        ax[3].set_ylim(1)

        ax[3].set_xlabel('Spanwise location [m]')
        ax[3].set_xlim(0,12)

        plt.show()
        # name = f"./Figures_mos_compr_option_{self.option_nr}.svg"
        # plt.savefig(name, format="svg")
        # plt.cla()

def main():
    option_2 = design_option_compr((0.012675), 2, 10, 8e-3,5.5e-3,4e-3,2)
    option_2.generate_plots()

if __name__ == '__main__':
    main()