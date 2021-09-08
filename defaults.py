from yacs.config import CfgNode as CN
import math

"""
Values from "Advanced RAIM User Algorithm Description: Integrity Support Message Processing, 
Fault Detection, Exclusion, and Protection Level Calculation"
https://web.stanford.edu/group/scpnt/gpslab/pubs/papers/Blanch_et_al_IONGNSS_2012_B5_nr7_post_submission_rev3.pdf
"""

_C = CN()

_C.sim = CN()
_C.sim.n_sat = 24 #TODO: Support for multiple constellations
_C.sim.n_const = 1

_C.integrity = CN() # Integrity budgets
_C.total_budget = 1e-7 # total integrity budget
_C.vertical_budget = 9.8e-8 # integrity budget for the vertical component
_C.horizontal_budget = 2e-9 # integrity budget for the horizontal component

_C.fault_prob = CN() # Failure probabilities
_C.fault_prob.sat = 4e-8 # Individual satellite failure probability
_C.fault_prob.constellation = {"GPS": 4e-8, # Constellation-wide failure probability
                        "Galileo": 4e-8}

_C.continuity = CN()
_C.continuity.false_alert = 4e-6 # Continuity budget allocated to disruptions due to false alert. 
_C.continuity.vertical = 3.9e-6 # Continuity budget allocated to the vertical mode
_C.continuity.horizontal = 9e-8 # Continuity budget allocated to the horizontal mode
_C.continuity.chi_squared = 9e-8 # Continuity budget allocated to the chi-square test

_C.tolerance = 5e-2 # Tolerance for the computation of the Protection Level 
_C.acc_nb_st_devs = 1.96 # number of standard deviations used for the accuracy formula 
_C.fault_free_nb_st_devs = 5.33 # umber of standard deviations used for the 10-7 fault free vertical position error
_C.effective_maneuver_threshold_prob = 1e-5 # Probability used for the calculation of the Effective Monitor Threshold 
_C.periods = CN() 
_C.periods.consistency_check_period = 300 # Time constant between consistency checks for excluded satellites
_C.periods.recovery_period = 600 # Minimum time period a previously excluded satellite remains out of the all-in-view position solution

# Table source:
# https://web.stanford.edu/group/scpnt/gpslab/pubs/papers/Blanch_et_al_IONGNSS_2012_B5_nr7_post_submission_rev3.pdf
_errors_elevations = {5.0: 0.4529,
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

def get_user_error(elevation:float) -> float:
    """
    Gets galileo user terminal error standard deviation given the elevation angle of a GNSS signal.
    TODO: Implement GPS user terminal error
    Args:
        elevation (float): Elevation of the satellite sending the pseudorange signal for which the troposheric error must be obtained

    Returns:
        float: User terminal error
    """  
    assert 0.0 < elevation < 90.0
    if elevation in _errors_elevations:
        return _errors_elevations[elevation]
    else:
        key_min = elevation - elevation%5.0
        key_max = key_min + 5.0
        user_min = _errors_elevations[key_min]
        user_max = _errors_elevations[key_max]
        user_error = user_min + elevation/(key_max-key_min)*(user_max - user_min)
    return user_error
        
def get_tropo_error(elevation:float) -> float:
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

def get_cfg_defaults() -> CN:
  """Get a yacs CfgNode object with default values for my_project."""
  # Return a clone so that the defaults will not be altered
  # This is for the "local variable" use pattern
  return _C.clone()