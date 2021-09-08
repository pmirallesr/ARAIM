
from yacs.config import CfgNode as CN
import numpy as np
from typing import Dict
from dataclasses import dataclass
import math


@dataclass
class IntegrityMessage:
    integrity_clock_ephem_error : np.ndarray
    acc_cont_clock_ephem_error : np.ndarray
    max_bias : np.ndarray
    p_sat_fault : np.ndarray
    p_const_fault : np.ndarray

class Simulation:
    def __init__(self, sim_conf: CN):
        assert len(sim_conf.n_sats) == sim_conf.n_const
        self.n_const = sim_conf.n_const
        self.n_sats = sim_conf.n_sats
        self.geo_matrix = sim_conf.geo_matrix
        # Table source:
        # https://web.stanford.edu/group/scpnt/gpslab/pubs/papers/Blanch_et_al_IONGNSS_2012_B5_nr7_post_submission_rev3.pdf
        self._galileo_user_errors_elevations = {5.0: 0.4529,
                        10.0: 0.3553,
                        15.0: 0.3063,
                        20.0: 0.2638,
                        25.0: 0.2593,
                        30.0: 0.2555,
                        35.0: 0.2504,
                        40.0: 0.2438,
                        45.0: 0.2396,
                        50.0: 0.2359,
                        55.0: 0.2339,
                        60.0: 0.2302,
                        65.0: 0.2295,
                        70.0: 0.2278,
                        75.0: 0.2297,
                        80.0: 0.2310,
                        85.0: 0.2274,
                        90.0: 0.2277,}
    
    def get_integrity_service_message(self) -> IntegrityMessage:

        return IntegrityMessage(integrity_clock_ephem_error = 0.5*np.ones(shape=(self.n_const, self.n_sats)),
                                acc_cont_clock_ephem_error = 0.75*np.ones(shape=(self.n_const, self.n_sats)),
                                max_bias = 0.5*np.ones(shape=(self.n_const, self.n_sats)),
                                p_sat_fault = 1e-4*np.ones(shape=(self.n_const, self.n_sats)),
                                p_const_fault = 1e-4*np.ones(shape=(self.n_const)))

    def get_user_error(self,elevation: float) -> float:
        """
        Gets galileo user terminal error standard deviation given the elevation angle of a GNSS signal.
        TODO: Implement GPS user terminal error
        Args:
            elevation (float): Elevation of the satellite sending the pseudorange signal for which the troposheric error must be obtained

        Returns:
            float: User terminal error
        """  
        assert 0.0 < elevation < 90.0
        if elevation in self._galileo_user_errors_elevations:
            return self._galileo_user_errors_elevations[elevation]
        else:
            key_min = elevation - elevation%5.0
            key_max = key_min + 5.0
            user_min = self._galileo_user_errors_elevations[key_min]
            user_max = self._galileo_user_errors_elevations[key_max]
            user_error = user_min + elevation/(key_max-key_min)*(user_max - user_min)
        return user_error

    def get_tropo_error(self, elevation: float) -> float:
        """
        Gets tropospheric error standard deviation given the elevation angle of a GNSS signal. Formula source:
        https://web.stanford.edu/group/scpnt/gpslab/pubs/papers/Blanch_et_al_IONGNSS_2012_B5_nr7_post_submission_rev3.pdf
        Args:
            elevation (float): Elevation of the satellite sending the pseudorange signal for which the troposheric error must be obtained

        Returns:
            float: Troposheric error
        """    
        assert 0.0 < elevation < 90.0
        return 0.12*1.0017/(0.002001 + math.sin(math.pi*elevation/180)**2)

    def get_geometry_matrix(self) -> np.ndarray:
        return self.geo_matrix
        