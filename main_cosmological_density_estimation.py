import numpy as np
import seaborn as sns
import emcee
import corner
import matplotlib.pyplot as plt
import pandas as pd
from astropy.table import Table
from scipy.stats import norm
from astropy.cosmology import LambdaCDM
from scipy.optimize import minimize
from preprocessing import clean_import

# Define functions to compute the log-prior, log-likelihood, and log-posterior
# Note: theta = [omega_m, Omega_L]

redshift, distance_modulus, distance_modulus_error = clean_import()


class cosmological_density_parameter_estimators(object):

  def __init__(self, initial_guess: list[float], redshift: list[float], distance_modulus: list[float], distance_modulus_error: list[float]) -> None:
    self.initial_guess = initial_guess
    self.distance_modulus = distance_modulus
    self.redshift = redshift
    self.distance_modulus_error = distance_modulus_error

    self.samples_with_chain = None # these let's me handle the storage of these values with ease and avoid several function calls to the MCMC_sampler
    self.samples_without_chain = None

  def getdmmod(self,parameters,z):
    omega_m,omega_l = parameters[0],parameters[1]
    if omega_m > 0.0 and omega_l > 0.0:
      cosmo = LambdaCDM(H0=70.,Om0=omega_m,Ode0=omega_l)
      r = cosmo.comoving_distance(z).value
      dl = r*(1.+z)
      # print(dl)
      return 5.*np.log10(dl) + 25.
    if omega_m < 0.0 or omega_l < 0.0:
      return -np.inf  # log(0)

  def log_prior(self,theta):
      # What kind of priors should we use? To make the data do the bulk of the inference, I utitlized a weakly informative prior. Spefically, I used a
      # flat prior knowing that Omega_m and Omega_l have values between 0 and 1 we shall exclude all negative values
      omega_m, omega_l = theta

      if np.any(theta <= 0):
        return -np.inf

      # prior_omega_m = np.log(omega_m)
      # prior_omega_l = np.log(omega_l)
      return 0

  def log_likelihood(self, theta):

    distance_modulus_model = self.getdmmod(theta, self.redshift) # this works
    mu, sigma = distance_modulus_model, self.distance_modulus_error

    return np.sum(norm.logpdf(self.distance_modulus,mu, sigma))

  def cosmology_maximum_likelihood_estimation(self):

    def log_likelihood_optimizer(parameters):

      return -self.log_likelihood(parameters)

    maximized_parameters = minimize(log_likelihood_optimizer, self.initial_guess, method="Nelder-Mead")

    # omega_m, omega_l = maximized_parameters.x

    # return omega_m, omega_l
    return maximized_parameters.x

  def log_posterior(self,theta):

    return self.log_prior(theta) + self.log_likelihood(theta)

  def cosmology_MCMC_sampler(self, burning_point=9, number_of_walkers= 50, number_of_steps = 1000):

    def cosmology_MCMC_log_posterior(mcmc_parameters):
      return self.log_posterior(mcmc_parameters)

    number_of_dimensons = 2

    starting_point = self.cosmology_maximum_likelihood_estimation() + 0.1*np.abs(np.random.randn(number_of_walkers, number_of_dimensons))

    sampler = emcee.EnsembleSampler(number_of_walkers, number_of_dimensons, cosmology_MCMC_log_posterior)

    sampler.run_mcmc(starting_point, number_of_steps, progress=True)

    self.samples_with_chain = sampler.get_chain()
    self.samples_without_chain = sampler.get_chain(discard=burning_point, flat=True)

    #Im guessing since our sample is quite big, and we have 50 walkers(good enough) the burn in position will occur much earlier. But, it doesn't hurt to verify this
    if len(self.samples_with_chain) <= burning_point:
      print(' \n Careful not to burn all your data away! \n')
    else:
      print(' \n Clear to proceed, Chidi! \n')

    return self.samples_with_chain, self.samples_without_chain


  def cosmology_trace_plot(self, burning_point = 9):

    chain_for_trace_plot = self.samples_with_chain[:] # alias

    figure, ax_main = plt.subplots(2,1, figsize=(9,7.9), sharex=True)

    parameter_names = ["Omega_m", "Omega_l"]

    for lines in range(2):
      ax_current = ax_main[lines] # add the labels for the axis
      ax_current.plot(chain_for_trace_plot[:,:,lines], '-k')
      ax_current.axvline(burning_point, color="red", linestyle="--", label="burning point")
      ax_current.set_ylabel(parameter_names[lines])

    ax_main[1].set_xlabel(" Iterations")
    figure.tight_layout()


  def cosmology_corner_plot(self):

    parameter_names = ["Omega_m", "Omega_l"]

    corner.corner(self.samples_without_chain, labels = parameter_names, show_titles = True)

  def cosmology_fit_plot(self):

    omega_m = self.samples_without_chain[:,0]
    omega_l = self.samples_without_chain[:,1]

    figure, ax_main = plt.subplots(figsize=(9,8.9))

    ax_main.errorbar(self.redshift, self.distance_modulus, self.distance_modulus_error, fmt="ok", ecolor='black', elinewidth=1.5, capsize=1.5,markersize=2, alpha=0.4)

    x_range = np.linspace(min(self.redshift), max(self.redshift), 200)

    # I want to draw random choices for the parameter values
    number_of_points = 100
    index_for_cosmic_parameters = np.random.choice(len(self.samples_without_chain), number_of_points, replace= False)

    for points in index_for_cosmic_parameters:

      parameters = [omega_m[points], omega_l[points]]

      DM_fit = self.getdmmod(parameters,x_range) # better fit

      # the fit below was off by a lot of miles
      # DM_fit = 43.17 - 5 * np.log(72/70) + 5* np.log(x_range) + 1.086 * (1 - q_naught) * x_range # the desired fit

      ax_main.plot(x_range, DM_fit, "r--", alpha=1)

    mean_parameters = [np.mean(omega_m), np.mean(omega_l)]
    mean_DM_fit = self.getdmmod(mean_parameters,x_range) # better fit
    # mean_DM_fit = 43.17 - 5 * np.log(72/70) + 5* np.log(x_range) + 1.086 * (1 - q_naught) * x_range # the desired fit
    ax_main.plot(x_range, mean_DM_fit, color="green", linestyle="-", alpha=1)

    ax_main.set_xlabel('Redshift(z)')
    ax_main.set_ylabel("Distance Modulus(DM)")

    ax_main.set_ylim(33, 50)
    ax_main.set_title(" \n Bayesian fitting of lines to a plot of Distance Modulus against the Redshift \n")
    ax_main.grid(True)
    figure.tight_layout()


if __name__ == "__main__":

    # Using emcee, create and initialize a sampler with 50 walkers and draw 1000 samples from the posterior.
    # Remember to think about what starting guesses you should use!
    cosmology_instance = cosmological_density_parameter_estimators([1,1], redshift,distance_modulus, distance_modulus_error)
    omega_m, omega_l = cosmology_instance.cosmology_maximum_likelihood_estimation()
    print(f' Omega_m is: {omega_m:.4} and Omega_l is: {omega_l:.4}')


    # Kindly run the MCMC sampler to store the samples before proceeding. Thank you.
    # I tested this code with number_of_steps = 100 and it rans very slowly.
    # My submission has this set to number_of_steps = 1000 as required but this will run very much slower.
    # I have added a progress bar to help ascertain whether it runs or not
    cosmology_instance.cosmology_MCMC_sampler()

    # Plot the two chains to determine when they stabilize
    cosmology_instance.cosmology_trace_plot()
    plt.show()

    # extract the samples (removing the burn-in)
    # # already doe in the cosmology_MCMC_sampler() method above


    # Use corner.py to visualize the two-dimensional posterior
    cosmology_instance.cosmology_corner_plot()
    plt.show()


    # Next plot ~100 of the samples as models over the data to get an idea of the fit
    # this might take a little while since the plot methid calls the getdmmod() function which I believe we agreed is slow

    cosmology_instance.cosmology_fit_plot()
    plt.show()


    # Report your best-fit values and their 68% confidence
    # Hint: If you use the show_titles=True option when you call corner in the cell above, it will print the best-fit result and the 68% confidence error bars right on the plot. It's a pretty handy feature.