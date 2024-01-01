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
    plt.grid()
    plt.show()


def plot_customized(filename, y_labels):
    df = load_dataframe(filename)
    df.columns = cols
    for y_label in y_labels:
        if y_label not in cols:
            raise KeyError
    for y_label in y_labels:
        plt.plot(df['day'], df[y_label], label=y_label)
    plt.title('Average velocity and age by day')
    plt.xlabel('Day')
    plt.ylabel('Metrics')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    file = sys.argv[1]
    plot_type = sys.argv[2]
    try:
        if plot_type == 'all':
            plot_all_stats(file)

        elif plot_type == 'va':
            plot_velocity_and_age(file)

        elif plot_type == 'custom':
            plot_customized(file, sys.argv[3:])

        else:
            print("Invalid plot type!")
            print('Usage: python stats.py <filename> <plot_type> <y_labels>')
            print('Example: python stats.py stats.csv custom population food')
            print('Example: python stats.py stats.csv va')
            print('Example: python stats.py stats.csv all')

    except FileNotFoundError as e:
        print("File not found!")

    except KeyError as e:
        print("Invalid label. Metric specified was not found!")

    except Exception as e:
        print("Something went wrong. Check your arguments!")
        print('Usage: python stats.py <filename> <plot_type> <y_labels>')
        print('Example: python stats.py stats.csv custom population food')
        print('Example: python stats.py stats.csv va')
        print('Example: python stats.py stats.csv all')
