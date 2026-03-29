import matplotlib.pyplot as plt

def plot_signal(real, pred, anomalies):
    plt.figure()
    plt.plot(real, label="Real")
    plt.plot(pred, label="Pred")
    plt.scatter(range(len(real)), anomalies, color='red', s=2)
    plt.legend()
    plt.show()
