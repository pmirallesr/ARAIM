from defaults import get_cfg_defaults, get_user_error, get_tropo_error
from yacs.config import CfgNode as CN
import numpy as np
from typing import List, Union

def get_integrity_service_message(n_sat: int, n_const: int) -> CN():
    integrity_message = CN()
    integrity_message.integrity_clock_ephem_error = {f"sat_{i}": 1e-10 for i in n_sat}
    integrity_message.acc_cont_clock_ephem_error = {f"sat_{i}": 1e-10 for i in n_sat}
    integrity_message.max_bias = {f"sat_{i}": 0 for i in n_sat}
    integrity_message.p_sat_fault = {f"sat_{i}": 1e-10 for i in n_sat}
    integrity_message.p_const_fault = {f"sat_{i}": 1e-10 for i in n_const}
    return integrity_message


def build_covariance_matrices(ism:CN, tropo_error: Union(List[float], float), user_error: Union(float, List[float])) -> List[np.ndarray, np.ndarray]:
    
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
    n_sat = conf.sim.n_sat
    n_const = conf.sim.n_const
    active_sats = [f"sat_{i}" for i in range(n_sat)]
    # Start calculation loop
    while True:
        # The ism provides information related to instantaneous signal integrity
        ism = get_integrity_service_message(n_sat, n_const)
        # Pseudorange covariance matrices
        user_error = get_user_error()
        tropo_error = get_tropo_error()
        pseudorange_cov_integrity, pseudorange_cov_acc_cont = build_covariance_matrices(ism, tropo_error, user_error)
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