import numpy as np
from load_case import LoadCase
from skin_stress import skin_stress
from Moment_of_inertia import get_ixx
from matplotlib import pyplot as plt

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

    def mos_compr_stringer(self, y: float) -> float:
        stress = skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringer, 1)
        return self.sigma_yield/stress

    def mos_compr_skin(self, y: float) -> float:
        stress = skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringer, 1)
        return self.sigma_yield/stress

    def mos_compr_front(self, y: float) -> float:
        moment = self.load.z2_moment(y)
        c = 3.49 -3.49*(1-0.372)/12 *y
        coord = c * 0.114/2
        ixx = get_ixx(y, self.t_f, self.t_r, self.t_s, self.n_stringer, self.a_stringer)
        
        stress = moment*coord/ixx

        return self.sigma_yield/stress

    def mos_compr_rear(self, y: float) -> float:
        moment = self.load.z2_moment(y)
        c = 3.49-3.49*(1-0.372)/12 *y
        coord = c * 0.063/2
        ixx = get_ixx(y, self.t_f, self.t_r, self.t_s, self.n_stringer, self.a_stringer)

        stress = moment*coord/ixx
        return self.sigma_yield/stress

    def generate_plots(self):
        y_axis = np.linspace(0,11.98,100)

        mos_compr_stringer = []
        mos_compr_skin = []
        mos_compr_front = []
        mos_compr_rear = []

        for y in y_axis:
            mos_compr_stringer.append(self.mos_compr_stringer(y))
            mos_compr_skin.append(self.mos_compr_skin(y))
            mos_compr_front.append(self.mos_compr_front(y))
            mos_compr_rear.append(self.mos_compr_rear(y))

        
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

        name = f"./Figures_mos_compr_option_{self.option}.svg"
        plt.savefig(name, format="svg")
        plt.cla()

def main():
    option_2 = design_option_compr((0.012675), 2, 10, 8e-3,5.5e-3,4e-3,2)
    option_2.generate_plots()

if __name__ == '__main__':
    main()