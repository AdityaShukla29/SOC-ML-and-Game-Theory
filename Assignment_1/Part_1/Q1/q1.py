import json
import numpy as np
import matplotlib.pyplot as plt

def inv_transform(distribution: str, num_samples: int, **kwargs) -> list:
    """ populate the 'samples' list from the desired distribution """

    samples = []

    # TODO: first generate random numbers from the uniform distribution
    random_numbers=np.round(np.random.rand(num_samples),decimals=4)
    if distribution == "exponential":
        random_numbers=np.delete(random_numbers,np.where(random_numbers==0))
        samples_in_np_format = (-np.log(random_numbers)/kwargs["lambda"])
        samples = samples_in_np_format.tolist()
    elif distribution == "cauchy":
        samples_in_np_format = kwargs["peak_x"]+kwargs["gamma"]*np.tan(np.pi*(random_numbers-0.5))
        samples = samples_in_np_format.tolist()


    # END TODO
            
    return samples


if __name__ == "__main__":
    np.random.seed(42)

    for distribution in ["cauchy", "exponential"]:
        file_name = "q1_" + distribution + ".json"
        args = json.load(open(file_name, "r"))
        samples = inv_transform(**args)
        
        with open("q1_output_" + distribution + ".json", "w") as file:
            json.dump(samples, file)

        # TODO: plot and save the histogram to "q1_" + distribution + ".png"
        histo="q1"+ distribution+".png"
        


        if distribution == "exponential":
            plt.hist(samples,100)
            plt.xticks([0,0.5,1,1.5,2,2.5,3,3.5,4])

        elif distribution == "cauchy":
              plt.hist(samples, 100)
        plt.savefig(histo)
        plt.clf()
        # END TODO
