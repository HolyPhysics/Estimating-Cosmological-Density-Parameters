# Estimating Cosmological Density Parameters
In this project, I run an MCMC analysis on the supernova redshift-DM dataset to determine the cosmological parameters  Ω𝑚  and  ΩΛ

Supernovae occur when massive stars explode at the end of their lives. A very particular type of supernova, known as a Type Ia, occurs when a white dwarf star in a binary pair with a red dwarf star steals mass from the red dwarf until it is too massive to support itself against gravity. When this happens, the white dwarf collapses, starting a runaway nuclear reaction and a bright explosion. Because the white dwarf collapse always occurs at the same critical mass (known as the Chandrasekhar Mass, 1.44  𝑀⊙ ), the resulting explosion always has the same luminosity. As a result, supernovae are known as Standard Candles. Comparing this luminosity to the observed brightness of the star allows one to estimate the distance to the supernova. We can also idependently measure the redshift to the galaxy that hosts the supernova explosion by observing the redward shift of spectral lines in the galaxy's spectrum.

It turns out that the relationship between redshift and the distance to galaxies depends on the curvature of space-time. Massive objects like the Sun or the Earth cause local space-time to warp around them, but the same thing happens to the overall curvature of space-time due to the mass and energy density of the entire Universe (energy bends space-time just like matter does). This curvature will change the relationship between redshift and distance. Since we can measure both redshift and distance independently for supernovae, they allow us to constrain the density of the Universe.

There are two primary contributors to the density of the Universe today: matter and dark energy. The first slows the expansion of the Universe, while the latter accelerates it. Both bend space-time and affect its curvature. The density of the Universe is usually expressed in terms of the dimensionless Density Parameter,  Ω . The density parameter is the ratio of the average density of matter and energy in the Universe to the critical density,  𝜌critical , the density at which the Universe would have a flat space-time (no curvature). Add too much matter, and the Universe becomes "closed", with positive curvature. Spheres like the Earth have positive curvature (except in 3D instead of 4D). Add too much dark energy and the Universe becomes "open", with negative curvature. Strike the right balance and space-time will be flat.

The density of matter and dark energy relative to the critical density is given by the unitless parameters:

Ω𝑚=𝜌𝑚/𝜌critical 

ΩΛ=𝜌Λ/𝜌critical

The sum of which is the total density relative to the critical density,  Ω=Ω𝑚+ΩΛ . Here  Λ  is the cosmological constant, which Einstein introduced when he formulated General Relativity. Today,  Λ  is given a different interpretation, related to an energy density of the vacuum, which is what we think powers dark energy. The values of the cosmological parameters are known quite accurately today, with values of  Ω𝑚=0.3  and  ΩΛ=0.7 , partly due to studies of distant supernova using datasets similar to the one you'll be working with today.


---

## Methods and Data

### Data Sources
- Data file is included in the file SN_dataset.dat

### Features 
- Redshift-DM plot
- Parameters burn-in chain plots
- corner plots
- final fit

### Parameters and Constants
- z -- Redshift
- d_l -- distance
- H_0 -- Hubble Constant
- DM -- Distance Modulus

### Relationship Between Parameters 

The relationship between the redshift,  𝑧 , and distance,  𝑑𝐿 , to a galaxy depends on the density parameters approximately as

𝑑𝐿∼𝑐𝐻0𝑧 (1+1+𝑞02 𝑧) 

where  𝐻0  is the Hubble Constant ( 𝐻0=72  km/s/Mpc) and  𝑞0  contains the dependancy on the density parameters

𝑞0=12 Ω𝑚−ΩΛ 

Unfortunately, we don't actually measure  𝑑𝐿  when we observe supernovae. Instead, we measure their apparent magnitude,  𝑚  (related to apparent brightness), and compare it to their known absolute magnitudes,  𝑀  (related to their luminosities). The difference between these quantities is known as the distance modulus

𝐷𝑀=𝑚−𝑀=5log𝑑𝐿1 Mpc+25 

Folding everything together gives us the following approximate relationship between distance modulus, redshift, and the cosmological density parameters:

𝐷𝑀∼43.17−5log(𝐻070 km/s/Mpc)+5log(𝑧)+1.086 (1−𝑞0) 𝑧 

This relationship is only an approximation. In the cell below, I've provided the function getdmmod that calculates the distance modulus exactly when given a redshift and density parameters.



---

## Installation

### Requirements

- Python 3.x
- numpy
- matplotlib
- astropy
- astroML
- scikit-learn

### Installation Command

```bash
pip install numpy matplotlib astropy astroML scikit-learn
```

---

## Example Plots
