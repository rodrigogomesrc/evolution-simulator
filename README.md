# evolution-simulator

## About

A basic simulator built in python to see the impact on the "creatures" population characteristics
evolution based on changes to the environment parameters.

## Configurating parameters

To tweak the environment parameters, edit the `config.json` file.

You can display the simulation using pygame. To do so, set `display` to `true` in the `config.json` file. But that makes
it run slower.

## Running the simulation

To run the simulation, run the `evolution.py` file:

```bash
python3 evolution.py
```

## Displaying the results

To display the results, there's a file name **stats.py**.

**Command Syntax:**
    
```bash
python3 stats.py <filename> <plot_type> <labels>
```
`<filename>`: Name of the CSV file containing the simulation results.

`<plot_type>`: Type of plot to generate (all, va, or custom).

`<labels>`: Labels of metrics to be plotted (applicable for custom plot type).

By default, the simulation generates a CSV file named **stats.csv**. You can use this file to generate the plots.

**Examples:**

Plotting all metrics:

```bash
python stats.py stats.csv all
```
Plotting average velocity and age:

```bash
python stats.py stats.csv va
```

Customized plotting:
    
```bash
python stats.py stats.csv custom population food
```

This command generates a plot with metrics specified
(population and food in this case) over the recorded days.

