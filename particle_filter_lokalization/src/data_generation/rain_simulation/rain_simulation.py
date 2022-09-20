import numpy as np


def apply_rain(position, rain_rate, pc_array, p_min, lidar_range):

    # get all points in range of lidar sensor
    subs = (position - pc_array[:,0:2])
    # calculate their range
    ranges = np.linalg.norm(subs, axis=1)
    in_range = ranges[ranges<lidar_range]

    # get their reflectivity
    reflectivities = pc_array[:,2][ranges < lidar_range] #+ np.random.randn(p.shape)*self.pc_array_measure_noise
    new_intensities = reflectivities/(in_range**2) * np.exp(-0.02*(rain_rate**0.6)*in_range)

    # filter out the points with intensities below p_min
    taken_ranges = in_range[new_intensities > p_min]
    taken_intensities = new_intensities[new_intensities > p_min]

    # noise the ranges
    noisy_ranges = np.random.normal(0, 0.02*taken_ranges*(1-np.exp(-rain_rate))**2)

    return noisy_ranges, taken_intensities