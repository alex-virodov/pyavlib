import numpy as np

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

# thank you https://stackoverflow.com/questions/14873203/plotting-of-1-dimensional-gaussian-distribution-function
def gaussian_normalized(x, mu, sig):
    return (1.0/(sig*np.sqrt(2*np.pi))) * gaussian(x, mu, sig)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.clf()
    x = np.linspace(-1.0, 1.0, 256)
    y = gaussian(x, mu=0.2, sig=0.1) + gaussian(x, mu=-0.2, sig=0.15)
    plt.plot(x, y)
