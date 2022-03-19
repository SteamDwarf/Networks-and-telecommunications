from Sector import Sector

class SectorCalculator:
    def get_sector_in_power(self, prev_sector_out, gain):
        return prev_sector_out + gain

    def get_sector_out_power(self, in_power, damping):
        return in_power - damping

    def get_sector_damping(self, length, damping_coeff):
        return length * damping_coeff

    def get_in_power(self, prev_power: float, damping: float) -> float:
        return prev_power - damping

    def get_out_power(self, in_power: float, gain: float) -> float:
        return in_power + gain

    def get_sector_length(self, damping: float, damping_per_km: float) -> float:
        return damping / damping_per_km

    def get_min_power(self, interference_immunity, interference_level):
        return interference_immunity + interference_level

    def get_first_sector(self, transmitter_out_power: float, reciever_in_power: float, damping_coef: float):
        damping  = abs(transmitter_out_power - reciever_in_power)
        length = self.get_sector_length(damping, damping_coef)
        out_power = transmitter_out_power - damping

        return Sector(transmitter_out_power, length, damping, out_power)

    def create_sector(self, in_power, length, damping_per_km):
        damping = self.get_sector_damping(length, damping_per_km)
        out_power = self.get_sector_out_power(in_power, damping)
                
        return Sector(in_power, length, damping, out_power)

    def make_sectors(self, transmitter_out_power, reciever_in_power, amplifier_gain, damping_coef, channel_length):
        powers = []
        amplifiers_points = []
        sectors = []
        
        first_sector = self.get_first_sector(transmitter_out_power, reciever_in_power, damping_coef)
        sectors.append(first_sector)
        amplifiers_points = [0.1, first_sector.length]
        powers = [first_sector.in_power, first_sector.out_power]

        cur_length = first_sector._length
        count = 2

        while cur_length < channel_length:
            in_power = self.get_sector_in_power(sectors[-1]._out_power, amplifier_gain)
            length = self.get_sector_length(amplifier_gain, damping_coef)

            if cur_length + length * 2 > channel_length:
                rest_length = channel_length - cur_length
                last_sector = self.create_sector(in_power, rest_length, damping_coef)
                prelast_sector = self.create_sector(in_power, length, damping_coef)
                last_in_power2 = self.get_sector_in_power(prelast_sector.out_power, amplifier_gain)
                last_sector2 = self.create_sector(last_in_power2, rest_length - length, damping_coef)

                power_difference = abs(reciever_in_power - last_sector.out_power)
                power_difference2 = abs(reciever_in_power - last_sector2.out_power)

                if power_difference > power_difference2:
                    sectors.extend([prelast_sector, last_sector2])
                    amplifiers_points.extend([cur_length, 
                                                prelast_sector.length + cur_length, 
                                                prelast_sector.length + cur_length + 0.01, 
                                                channel_length
                                            ])
                    cur_length += rest_length
                    powers.extend([in_power, prelast_sector.out_power, last_sector2.in_power, last_sector2.out_power])

                else:
                    sectors.append(last_sector)
                    amplifiers_points.extend([cur_length, cur_length + length])
                    cur_length += length
                    powers.extend([in_power, last_sector.out_power])                

            else:
                sector = self.create_sector(in_power, length, damping_coef)
                sectors.append(sector)

                amplifiers_points.extend([cur_length, cur_length + length])
                cur_length += sector.length
                powers.extend([sector.in_power, sector.out_power])
                
                count += 2
        return [amplifiers_points, powers, sectors]