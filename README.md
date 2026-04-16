# evolution-simulator

## About

A basic simulator built in Python to see the impact of environmental parameters on creature population characteristics and evolution. Watch creatures evolve based on natural selection, energy consumption, reproduction, and mutation mechanics.

## Features

- **Real-time visualization** with pygame (optional, slows execution)
- **Creature genetics**: velocity, age, energy consumption, reproduction
- **Sexual reproduction** mode (optional, with male/female distinction)
- **Natural selection** based on energy and survival
- **Mutation system** affecting creature traits
- **Population dynamics** with birth, death, starvation, and aging
- **Food spawning and consumption** system
- **Statistics export** to CSV for analysis
- **Configurable ecosystem** parameters
- **Performance optimizations** including cache and JIT support

## Quick Start

### Configuration

All environment parameters are customizable via `config.json`. Key features:

- **Display simulation**: Set `displaySimulation` to `true` to watch with pygame (recommended: `false` for speed)
- **Sexual reproduction**: Set `considerTwoSexes` to `true/false` to enable/disable gender system
- **Population restart**: Set `restartWithLastPopulation` to auto-restart with last surviving creature's traits when extinct
- **Execution limit**: Set `limitExecutionInDays` + `daysLimit` to cap simulation duration

## Configuration Parameters

All parameters are in `config.json`. Below is the complete reference:

### World & Display
| Parameter | Default | Description |
|-----------|---------|-------------|
| `screenWidth` | 1000 | Simulation viewport width in pixels |
| `screenHeight` | 600 | Simulation viewport height in pixels |
| `displaySimulation` | false | Show pygame visualization (slower if true) |
| `cicleSize` | 100 | World height (creatures move between 0-cicleSize) |

### Creatures Configuration
| Parameter | Default | Description |
|-----------|---------|-------------|
| `initialCreatures` | 100 | Number of creatures at start |
| `minCreatureStartVelocity` | 2 | Minimum initial creature speed |
| `maxCreatureStartVelocity` | 20 | Maximum initial creature speed |
| `maxCreatureAge` | 10000 | Maximum age before death (cycles) |
| `maxCreatureEnergy` | 100000 | Maximum energy a creature can have |
| `velocityBaseCost` | 5 | Base energy cost per cycle |
| `velocityCostRate` | 0.20 | Additional cost multiplier per velocity point |
| `mutationRange` | 0.4 | Mutation severity (0.4 = ±40% change) |

### Reproduction
| Parameter | Default | Description |
|-----------|---------|-------------|
| `considerTwoSexes` | true | Enable sexual reproduction (male/female) |
| `reproductionAgeStart` | 2000 | Minimum age to reproduce (cycles) |
| `reproductionAgeEnd` | 8000 | Maximum age to reproduce (cycles) |
| `reproductionEnergyMinimum` | 30000 | Minimum energy required to reproduce |
| `reproductionEnergyCost` | 15000 | Energy consumed when reproducing |

### Food System
| Parameter | Default | Description |
|-----------|---------|-------------|
| `initialFood` | 100 | Number of food items at start |
| `maxFood` | 1000 | Maximum food in world at once |
| `foodEnergy` | 500 | Energy gained when eating food |
| `foodDuration` | 10 | Cycles until food spoils (removed) |
| `ciclesToSpawnFood` | 1 | Spawn attempt frequency (every N cycles) |
| `foodForSpawn` | 1 | How many food items spawn per cycle |

### Population Control
| Parameter | Default | Description |
|-----------|---------|-------------|
| `limitPopulation` | false | Enforce population cap |
| `populationLimit` | 1000 | Maximum creatures allowed (if limitPopulation=true) |
| `restartWithLastPopulation` | true | When extinct, restart with last creature's traits |

### Execution
| Parameter | Default | Description |
|-----------|---------|-------------|
| `limitExecutionInDays` | true | Cap execution time by days (vs cycles) |
| `daysLimit` | 600 | Execution limit (days if limitExecutionInDays=true) |

### Output
| Parameter | Default | Description |
|-----------|---------|-------------|
| `printStats` | false | Print population stats to console each cycle |
| `saveStatsToFile` | true | Save stats CSV file for analysis |

## Setting up the environment

First-time setup only. You only need to do this once:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

After the initial setup, you just need to activate the virtual environment:

```bash
source venv/bin/activate
```

## Running the simulation

To run the simulation, run the `evolution.py` file:

```bash
python3 evolution.py
```

You can also run about 6 times faster using the **pypy3** interpreter:

```bash
pypy3 evolution.py
```
Note: 

The simulation may be a little bit different using pypy3. For some reason using pypy the population will go extinct prematurely way easier.
For now, it doesn't work trying to display the simulation using pypy3. Because I couldn't manage to install pygame on pypy3.

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

## Understanding Simulation Mechanics

### Creature Lifecycle
- **Birth**: Usually from two parents (if `considerTwoSexes=true`). Parents must be in reproduction age range and have sufficient energy.
- **Movement**: Each cycle, creatures move in 8 directions. Movement costs energy based on their velocity.
- **Aging**: Age increases each cycle. Creatures die when reaching `maxCreatureAge`.
- **Starvation**: Creatures die when energy drops to zero.
- **Energy consumption**: Every cycle, creatures lose energy = `velocityBaseCost + (velocity * velocityCostRate)`

### Evolution & Mutation  
- Creature traits (velocity, sex) inherited from parents with mutations applied
- Mutation severity controlled by `mutationRange` (0.4 = ±40% variation)
- Natural selection: Only well-fed, fitting creatures survive to reproduce

### Food System
- Food spawns randomly at rate `foodForSpawn` per `ciclesToSpawnFood` cycles
- Each food lasts `foodDuration` cycles then spoils
- World maintains up to `maxFood` food items
- Eating food: creature gains `foodEnergy` instantly

### Population Control
- If `limitPopulation=true`, world caps at `populationLimit` creatures
- If `restartWithLastPopulation=true` and all creatures die, simulation restarts with traits of last survivor
- This allows quasi-continuous evolution even after extinction

## Performance Tips

- **Speed up**: Set `displaySimulation=false` (pygame visualization is expensive)
- **Use PyPy3**: About 5-10x faster than Python3 for long runs
- **Print/Save cautiously**: `printStats=true` and `saveStatsToFile=true` slow execution (disk I/O)
- **Parameter tuning**: High `initialFood` + low creature velocity = stable, slow evolution
- **Extinction avoidance**: Start with adequate `initialFood` and `foodEnergy` relative to reproduction costs

## Troubleshooting

### Creatures go extinct immediately
- Increase `initialFood` or `foodEnergy`
- Decrease `velocityBaseCost` or `velocityCostRate`  
- Increase `reproductionEnergyMinimum` or decrease `reproductionEnergyCost`
- Ensure reproduction age range is reasonable (`reproductionAgeStart < reproductionAgeEnd`)

### Simulation runs too slowly
- Ensure `displaySimulation=false`
- Use PyPy3 instead of Python3

### Population explodes
- Decrease `initialFood` or `foodEnergy`
- Increase `reproductionEnergyCost`
- Enable `limitPopulation=true` with reasonable `populationLimit`
- Increase `velocityBaseCost` (makes survival harder)
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

