import numpy as np
import config.config as config


def apply_rain(position, rain_rate, pc_array, p_min): 
    p_min = 0.9/(np.pi * config.lidar_range**2)
    # get all points in range of lidar sensor
    subs = (position - pc_array[:,0:2])
    # calculate their range
    ranges = np.linalg.norm(subs, axis=1)
    angles = np.arctan2(subs[:,1], subs[:,0])

    ranges_in_range = ranges[ranges < config.lidar_range]
    angles_in_range = angles[ranges < config.lidar_range]
    
    reflectivities = pc_array[:,2][ranges < config.lidar_range]
    new_intensities = reflectivities/(ranges_in_range**2) * np.exp(-0.02*(rain_rate**0.6)*ranges_in_range)
    taken_ranges = ranges_in_range[new_intensities > p_min]
    taken_angles = angles_in_range[new_intensities > p_min]
    if (len(taken_ranges[taken_ranges < 0]) > 0): 
        taken_ranges[taken_ranges < 0] = 0
    taken_intensities = new_intensities[new_intensities > p_min]
    noisy_ranges = np.random.normal(0, 0.02*taken_ranges*(1-np.exp(-rain_rate))**2)
    points_after_rain = np.stack([noisy_ranges * np.cos(taken_angles), noisy_ranges * np.sin(taken_angles)], axis=1)

    return points_after_rain

'''
def apply_rain(position, rain_rate, pc_array, p_min, lidar_range):

    # get all points in range of lidar sensor
    subs = (pc_array[:,0:2] - position)
    # calculate their range
    ranges = np.linalg.norm(subs, axis=1)
    
    in_range = ranges[ranges<lidar_range]
    in_range = in_range + np.random.randn()*config.lidar_sensor_std # apply noise from sensor

    # get their reflectivity
    reflectivities = pc_array[:,2][ranges < lidar_range] #+ np.random.randn(p.shape)*self.pc_array_measure_noise
    new_intensities = reflectivities/(in_range**2) * np.exp(-0.02*(rain_rate**0.6)*in_range)

    # filter out the points with intensities below p_min
    taken_ranges = in_range[new_intensities > p_min]
    if (len(taken_ranges[taken_ranges < 0]) > 0): 
        taken_ranges[taken_ranges < 0] = 0

    taken_intensities = new_intensities[new_intensities > p_min]

    # noise the ranges according to rain
    noisy_ranges = np.random.normal(0, 0.02*taken_ranges*(1-np.exp(-rain_rate))**2)

    return noisy_ranges, taken_intensities

'''


