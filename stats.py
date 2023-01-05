import pandas as pd
import matplotlib.pyplot as plt
import sys

cols = ['day', 'velocity', 'age', 'population', 'food']

def load_dataframe(filename):
    return pd.read_csv(filename)


def plot_all_stats(filename):
    df = load_dataframe(filename)
    df.columns = cols
    plot_all_from_dataframe(df)


def plot_all_from_dataframe(df):
    plt.plot(df['day'], df['velocity'], label='Average velocity')
    plt.plot(df['day'], df['age'], label='Average age')
    plt.plot(df['day'], df['population'], label='Population')
    plt.plot(df['day'], df['food'], label='Food')
    plt.title('Metrics by day')
    plt.xlabel('Day')
    plt.ylabel('Metrics')
    plt.legend()
    plt.show()


def plot_velocity_and_age(filename):
    df = load_dataframe(filename)
    df.columns = cols
    plt.plot(df['day'], df['velocity'], label='Average velocity')
    plt.plot(df['day'], df['age'], label='Average age')
    plt.title('Average velocity and age by day')
    plt.xlabel('Day')
    plt.ylabel('Average velocities and age')
    plt.legend()
    plt.show()


def plot_customized(filename, y_labels):
    df = load_dataframe(filename)
    df.columns = cols
    for y_label in y_labels:
        plt.plot(df['day'], df[y_label], label=y_label)
    plt.title('Average velocity and age by day')
    plt.xlabel('Day')
    plt.ylabel('Metrics')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    file = sys.argv[1]
    plot_type = sys.argv[2]
    if plot_type == 'all':
        plot_all_stats(file)

    if plot_type == 'va':
        plot_velocity_and_age(file)

    if plot_type == 'custom':
        plot_customized(file, sys.argv[3:])
