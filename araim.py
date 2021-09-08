from sim import Simulation
from defaults import get_cfg_defaults
from yacs.config import CfgNode as CN
import numpy as np
from typing import List, Union



def build_covariance_matrices(ism:CN, tropo_error: Union(float, np.ndarray), user_error: Union(float, np.ndarray)) -> List[np.ndarray, np.ndarray]:
    
    n_sat = len(ism.integrity_clock_ephem_error)
    pseudorange_cov_integrity = np.zeros((n_sat,n_sat))
    pseudorange_cov_acc_cont = np.zeros((n_sat,n_sat))
    for i in range(n_sat):
        sat_tropo_error = tropo_error if type(tropo_error) == float else tropo_error[i]
        sat_user_error = user_error if type(user_error) == float else user_error[i]
        pseudorange_cov_integrity[i, i] = ism.integrity_clock_ephem_error**2 + sat_tropo_error**2 + sat_user_error**2
        pseudorange_cov_acc_cont[i, i] = ism.acc_cont_clock_ephem_error**2 + sat_tropo_error**2 + sat_user_error**2
    
    return [pseudorange_cov_integrity, pseudorange_cov_acc_cont]





def main():
    """
    Simulates an araim algorithm. Working prototype
    """

    conf = get_cfg_defaults()
    sim = Simulation(conf.sim)
    n_sat = sim.n_sats
    n_const = sim.n_const
    active_sats = np.ones(shape=(sim.n_const, sim.n_sat))
    # Start calculation loop
    while True:
        # The ism provides information related to instantaneous signal integrity
        ism = sim.get_integrity_service_message(n_sat, n_const)
        # Pseudorange covariance matrices

        pseudorange_cov_integrity, pseudorange_cov_acc_cont = build_covariance_matrices(ism, sim.get_tropo_error(), sim.get_user_error())
        # All in view position solution
        
        # Determination of faults that need to be monitored
            # Satellite
            # Constellation
            # Sat-constellation combined
        # Fault tolerant positions and associated st. devs and biases
        # Solution separation threshold and chi-squared test
        # Protection levels
        # Accuracy, fault free position error bound, Effective Monitor Threshold
        # Fault exclusion
            # Determining candidates
            # Testing candidates
                # Regular test
                # Wrong exclusion
            # New protection level
            # New accuracy after exclusion
            # Integrity of exclusion algorithm
        # Monitoring previously excluded satellites



if __name__ = "__main__":
    main()