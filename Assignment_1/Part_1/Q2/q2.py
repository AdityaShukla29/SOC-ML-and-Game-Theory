import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def PCA(init_array: pd.DataFrame):

    sorted_eigenvalues = None
    final_data = None
    dimensions = 2

    # TODO: transform init_array to final_data using PCA
    standardized_array = init_array-np.mean(init_array,axis=0)
    covariance_matrix = np.cov(np.transpose(standardized_array))
    eigenvalues,eigenvectors = np.linalg.eig(covariance_matrix)
    sorting_order=eigenvalues.argsort()[::-1]
    sorted_eigenvalues=eigenvalues[sorting_order]
    sorted_eigenvalues=np.round(sorted_eigenvalues,decimals=4)
    eigenvectors=eigenvectors[sorting_order]
    final_data=np.matmul(standardized_array,eigenvectors[0:,0:2])

    # END TODO

    return sorted_eigenvalues, final_data


if __name__ == '__main__':
    init_array = pd.read_csv("pca_data.csv", header = None)
    sorted_eigenvalues, final_data = PCA(init_array)
    np.savetxt("transform.csv", final_data, delimiter = ',')
    for eig in sorted_eigenvalues:
        print(eig)

    # TODO: plot and save a scatter plot of final_data to out.png
plot_data=pd.read_csv("transform.csv",header=None)
first_column = plot_data.iloc[:, 0]
second_column = plot_data.iloc[:, 1]
  
plt.scatter(first_column,second_column)
plt.xlim(-15, 15)
plt.ylim(-15, 15)
plt.savefig("out.png")
plt.show()
    # END TODO
