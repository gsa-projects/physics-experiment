# %%
from dataclasses import dataclass
from enum import Enum
from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
class Material(Enum):
    CORK = 0,
    FELT = 1,
    PLASTIC = 2

@dataclass
class Tray:
    mass: float
    material: Material

@dataclass
class MassBar:
    mass: float

class Experiment:
    def __init__(self, tray: Tray, data_path: str, mass_bars: tuple[MassBar, ...], run_no: tuple[int, ...]):
        self.tray = tray
        self.data_path = data_path
        self.mass_bars = mass_bars

        self.runs = {}
        df = pd.read_csv(data_path)
        column_names = {
            'Time (s)': 't',
            'Force (N)': 'F',
            'Position (m)': 'x',
            'Velocity (m/s)': 'v',
            'Acceleration (m/s²)': 'a'
        }

        for column in df.columns:
            name, no = column.split('Run #')
            no = int(no)

            if no not in run_no:
                continue

            if no not in self.runs:
                self.runs[no] = pd.DataFrame()

            self.runs[no][column_names[name]] = df[column].to_numpy()

    def __len__(self):
        return len(self.runs)

    def __call__(self, *args, **kwargs) -> None:
        fig, axis = plt.subplots(1, len(self), figsize=(6 * len(self), 6))

        # F-t 그래프
        for i, no in enumerate(self.runs.keys()):
            run = self.runs[no]
            max_f_time = run.t.iloc[run.F.idxmax()]

            axis[i].plot(run.t, run.F)
            axis[i].axvspan(max_f_time - 1, max_f_time + 1, color='yellow', alpha=0.3)
            axis[i].set_xlabel('Time (s)')
            axis[i].set_ylabel('Force (N)')
            axis[i].set_title(f'Run #{no}')
            axis[i].grid()


# %%
cork = Tray(94 / 1000, Material.CORK)
felt1 = Tray(84.4 / 1000, Material.FELT)
felt2 = Tray(84.6 / 1000, Material.FELT)
plastic = Tray(97.6 / 1000, Material.PLASTIC)

mass1 = MassBar(253 / 1000)
mass2 = MassBar(248.2 / 1000)
mass3 = MassBar(253 / 1000)
mass4 = MassBar(247.3 / 1000)

#%%
input_dir = path.join('..', '원본 데이터')

cork_slow = [
    Experiment(cork, path.join(input_dir, '느리게.csv'), (mass1, ), (1, 2, 3, 12)),
    Experiment(cork, path.join(input_dir, '느리게.csv'), (mass1, mass2), (4, 5, 6, 7)),
    Experiment(cork, path.join(input_dir, '느리게.csv'), (mass1, mass2, mass3), (8, 9, 10, 11)),
    Experiment(cork, path.join(input_dir, '느리게.csv'), (mass1, mass2, mass3, mass4), (13, 14, 15))
]

cork_fast = [
    Experiment(cork, path.join(input_dir, '빠르게.csv'), (mass1, ), (11, 12, 13)),
    Experiment(cork, path.join(input_dir, '빠르게.csv'), (mass1, mass2), (8, 9, 10)),
    Experiment(cork, path.join(input_dir, '빠르게.csv'), (mass1, mass2, mass3), (4, 5, 6, 7)),
    Experiment(cork, path.join(input_dir, '빠르게.csv'), (mass1, mass2, mass3, mass4), (1, 2, 3))
]

felt_slow = Experiment(felt1, path.join(input_dir, 'felt slow&fast.csv'), (mass1, mass2, mass3, mass4), (1, 2, 3))
felt_fast = Experiment(felt2, path.join(input_dir, 'felt slow&fast.csv'), (mass1, mass2, mass3, mass4), (4, 5, 6))

plastic_slow = Experiment(plastic, path.join(input_dir, 'plastic slow&fast.csv'), (mass1, mass2, mass3, mass4), (1, 2, 3))
plastic_fast = Experiment(plastic, path.join(input_dir, 'plastic slow&fast.csv'), (mass1, mass2, mass3, mass4), (4, 5, 6))

#%%
