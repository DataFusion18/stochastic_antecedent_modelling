#!/usr/bin/env python

"""
Attempt to port Ogle's ANPP OpenBUGS example from Appendix 2. See Box 2 in the
main text.

Reference
---------
* Ogle et al. (2015) Quantifying ecological memory in plant and ecosystem
  processes. Ecology Letters, 18: 221–235
"""

import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

__author__  = "Martin De Kauwe"
__version__ = "1.0 (23.12.2017)"
__email__   = "mdekauwe@gmail.com"

N = 52
# Number of past years, including the current year for which the antecedent conditions are computed
Nlag = 5
Nyrs = 91
Nblocks = 38

# the time block that each month is assigned to such that for 60 different
# months, we are only estimating 38 unique monthly weights
block = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,\
                  18, 19, 20, 21, 22, 23, 24, 25, 25, 26, 26, 27, 27, 28, 28,\
                  29, 29, 30, 30, 31, 31, 31, 32, 32, 32, 33, 33, 33, 34, 34,\
                  34, 35, 35, 35, 36, 36, 36, 37, 37, 37, 38,\
                  38, 38]).reshape(5,12)


df2 = pd.read_csv("data/dataset2.csv", na_values="NA", skiprows=1, sep=" ")
df3 = pd.read_csv("data/dataset3.csv", na_values="NA", skiprows=1, sep=" ")

with pm.Model() as model:

    # Assign priors to the ANPP regression parameters (covariate effects)
    a0 = pm.Normal('a0', mu=0, sd=0.0000001)
    a1 = pm.Normal('a1', mu=0, sd=0.0000001)
    a2 = pm.Normal('a2', mu=0, sd=0.0000001)
    a3 = pm.Normal('a3', mu=0, sd=0.0000001)
    a4 = pm.Normal('a4', mu=0, sd=0.0000001)
    a5 = pm.Normal('a5', mu=0, sd=0.0000001)


    # Prior for residual (observation) standard deviation, and compute
    # associated precision
    sig = pm.Uniform('sig', 0, 100)
    tau = pow(sig, -2)

    # Priors for parameters in the Event missing data model:
    mu_ev0 = pm.Uniform('mu_ev0', 0, 500)
    mu_ev1 = pm.Uniform('mu_ev1', 0, 500)
    mu_ev2 = pm.Uniform('mu_ev2', 0, 500)
    mu_ev3 = pm.Uniform('mu_ev3', 0, 500)

    sig_ev0 = pm.Uniform('sig_ev0', 0, 500)
    sig_ev1 = pm.Uniform('sig_ev1', 0, 500)
    sig_ev2 = pm.Uniform('sig_ev2', 0, 500)
    sig_ev3 = pm.Uniform('sig_ev3', 0, 500)

    tau_ev0 = pow(sig_ev0, -2)
    tau_ev1 = pow(sig_ev1, -2)
    tau_ev2 = pow(sig_ev2, -2)
    tau_ev3 = pow(sig_ev3, -2)
