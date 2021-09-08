from yacs.config import CfgNode as CN
import math
import numpy as np
"""
Values from "Advanced RAIM User Algorithm Description: Integrity Support Message Processing, 
Fault Detection, Exclusion, and Protection Level Calculation"
https://web.stanford.edu/group/scpnt/gpslab/pubs/papers/Blanch_et_al_IONGNSS_2012_B5_nr7_post_submission_rev3.pdf
"""

_C = CN()

_C.sim = CN()
_C.sim.n_sat = [5, 5]
_C.sim.n_const = 2
_C.sim.geo_matrix = np.array([[ 0.0225,  0.9951, -0.0966, 1, 0],
                              [ 0.6750, -0.6900, -0.2612, 1, 0],
                              [ 0.0723, -0.6601, -0.7477, 1, 0],
                              [-0.9398,  0.2553, -0.2269, 1, 0],
                              [-0.5907, -0.7539, -0.2877, 1, 0],
                              [-0.3236, -0.0354, -0.9455, 0, 1],
                              [-0.6748,  0.4356, -0.5957, 0, 1],
                              [ 0.0938, -0.7004, -0.7075, 0, 1],
                              [ 0.5571,  0.3088, -0.7709, 0, 1],
                              [ 0.6622,  0.6958, -0.2780, 0, 1],])
_C.sim.

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




def get_cfg_defaults() -> CN:
  """Get a yacs CfgNode object with default values for my_project."""
  # Return a clone so that the defaults will not be altered
  # This is for the "local variable" use pattern
  return _C.clone()