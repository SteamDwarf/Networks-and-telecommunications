from tkinter import *
from tkinter import ttk
from GUI import GUI
from SectorCalculator import SectorCalculator

gui = GUI()
sc = SectorCalculator()

channel_in_power: float = -5#-8#-4#
channel_out_power: float = -5#-10#-6#
transmitter_gain: float = 22#15#11#
receiver_gain: float = 8#9#5#
amplifier_gain: float = 18#25#21#
channel_length: float = 400#200#120#
damping_per_km: float = 3.4#2#1.2#
interference_level = -23
interference_immunity = 1

transmitter_out_power = sc.get_out_power(channel_in_power, transmitter_gain)
reciever_in_power = sc.get_in_power(channel_out_power, receiver_gain)
min_power = sc.get_min_power(interference_immunity, interference_level)
[amplifiers_points, powers, sectors] = sc.make_sectors(transmitter_out_power, reciever_in_power, amplifier_gain, damping_per_km, channel_length)

amplifiers_points.insert(0, 0)
amplifiers_points.append(channel_length + 0.01)
powers.insert(0, channel_in_power)
powers.append(channel_out_power)

result_columns_id = ['amplifier', 'in_power', 'out_power', 'power_gain','sector_length', 'damping']
result_columns_size = [200, 200, 200, 200, 200, 200]
result_columns_headers = ["Усилитель", 
                            "Мощность на входе усилителя",
                            "Мощность на выходе усилителя",
                            'Коэффициент усиления',
                            "Длина учатска",
                            "Затухание"
                        ]
result_data = [
    ['Передатчик', 
        channel_in_power, 
        transmitter_out_power, 
        transmitter_gain, 
        '0',
        '0'
    ],
    ['1', 
        sectors[0].out_power, 
        sectors[1].in_power, 
        amplifier_gain, 
        sectors[0].length,
        sectors[0].damping
    ],
    ['2', 
        sectors[1].out_power, 
        sectors[2].in_power, 
        amplifier_gain, 
        sectors[1].length,
        sectors[1].damping
    ],
    [len(sectors) - 1, 
        sectors[-2].out_power, 
        sectors[-1].in_power, 
        amplifier_gain, 
        sectors[-2].length,
        sectors[-2].damping
    ],
    ['Приемник', 
        sectors[-1].out_power, 
        channel_out_power, 
        receiver_gain, 
        sectors[-1].length,
        sectors[-1].damping
    ],
]                    

conditions_columns_id = ["channel_in_power",
                            "transmitter_gain",
                            "channel_length",
                            "damping_coefficient",
                            "amplifier_gain",
                            "reciever_gain",
                            "interference_level",
                            "interference_immunity",
                            "channel_out_power",
                            "min_power",
                        ]
conditions_columns_size = [80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
conditions_columns_headers = ["Pвх", "Sпер", "L", "a", "S", "Sпр", "Pпом", "А", "Pвых", "Pmin"]
conditions_data = [[channel_in_power, 
                    transmitter_gain, 
                    channel_length, 
                    damping_per_km, 
                    amplifier_gain, 
                    receiver_gain,
                    interference_level,
                    interference_immunity,
                    channel_out_power,
                    min_power,
                ]]      


gui.create_table(conditions_columns_id, conditions_columns_size, conditions_columns_headers, conditions_data, 1)
gui.create_table(result_columns_id, result_columns_size, result_columns_headers, result_data, 5)
gui.create_btn('Показать график', lambda: gui.show_graph(amplifiers_points, powers, channel_length, min_power))
gui.show_gui()



