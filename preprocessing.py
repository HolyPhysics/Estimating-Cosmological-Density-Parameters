import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from astropy.table import Table

# /content/drive/MyDrive/Colab Notebooks/SN_dataset.dat
data_file_path: str = "SN_dataset.dat"

try:
    data_table: Table = Table.read(data_file_path, format='ascii')
    print(' Great! Astropy.table.Table succesfully read the file!')
except Exception as err_cosmological_params:
    print(f' {type(err_cosmological_params).__name__} ocuured!')


def clean_import() -> list(np.ndarray, np.ndarray, np.ndarray): # for easy import into the main_cosmological_density_estimation file

    redshift: list[float,...] = np.array( data_table['Supernova'] ) # Table read the first name of the files so z got read as "Supernova" when I printed the data_table.columns
    distance_modulus: list[float,...] = np.array( data_table["cosmology"] ) # dm got read as "cosmology"
    distance_modulus_error: list[float,...] = np.array( data_table["dataset"] ) #dmerror got read as "dataset"

    return redshift, distance_modulus, distance_modulus_error

# data_to_visualize: pd.DataFrame = pd.DataFrame({
#     "Redshift" : redshift,
#     "Distance Modulus" : distance_modulus,
#     "Distance Modulus Error" : distance_modulus_error
# })

# # print(data_to_visualize)
# sns.pairplot(data_to_visualize) # This is so amazing! Makes a pair plot of all the variables and their relationships!!!
# plt.show()


if __name__ == "__main__":
    redshift, distance_modulus, distance_modulus_error = clean_import() 

    figure, ax_main = plt.subplots(figsize=(9,8.9))
    ax_main.errorbar(redshift, distance_modulus, distance_modulus_error, fmt="ok", ecolor='black', elinewidth=1.5, capsize=1.5, markersize=2, alpha=0.5)
    ax_main.set_xlabel('Redshift(z)')
    ax_main.set_ylabel("Distance Modulus(DM)")
    ax_main.set_title(" \n Errorbar Plot of Distance Modulus against the Redshift \n")
    ax_main.set_ylim(33,50)
    ax_main.grid(True)
    figure.tight_layout()
    plt.show()