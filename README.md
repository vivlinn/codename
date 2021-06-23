# Smart Grid
*Created by CodeName*

Green energy is the energy of the future, and self-producing is today's fashion. Nowadays, many houses have solar panels, windmills or other installations to produce their own energy. Fortunately, these installations often produce more energy than is necessary for their own consumption. The oversupply could be sold back to the supplier, but the infrastructure (the grid) is often not designed for this. Batteries must be installed to manage peaks in consumption and production.

To solve this problem, we will look at three residential areas, each containing 150 houses and 5 batteries. The houses are build with solar panels with a maximum output, while the batteries have a maximum capacity. The challenge is to connect houses with batteries using cables while keeping the costs as low as possible. 


### Part 1   
The first part consists of the following requirements:
- Batteries cannot be connected to each to each other.
- A house cannot be connected to multiple batteries.
- Each house is connected to a battery through their own unique cable.
-  Multiple cables are allowed to run over the same gridsegments. However, each house will still have their own unique cable, and this will not reduce costs.


1. For the first district, connect all houses to a battery. The maximum capacity of the houses cannot exceed the capacity of the batteries.
2. Calculate the total costs of cables and batteries for each district. Try to find the best possible configuration of cables. 

### Part 2
Houses can now share the same cable leading to a battery.

1. For each district, connect all houses to a battery. The maximum capacity of the houses cannot exceed the capacity of the batteries.
2. Optimalise the SmartGrid for all three districts.



## Get Started

### Requirements
This code is written entirely in Python 3.8.5. The following packages and files are needed to run the project succesfully.

```bash
python -m pip install -U pip
```

```bash
python -m pip install -U matplotlib
```
Use the following instructions to create the empty files.

```bash
touch output/output.json
```
```bash
touch output/longrun_hill.json
```
```bash
touch output/final_hill.json
```

### Run Project
To run this project, choose a district. See the following example to run the project for district 1. The number changes depending on chosen district.
```bash
python3 main.py 1
```
This will provide a command line interface where instructions will be available.

### Structure  
The following list describes the main folders and files for this project, and where to find them:
- **/code**: contains all code of this project.
    - **/code/algorithms**: contains the code for the algorithms.
    - **/code/classes**: contains the code for the classes
    - **/code/visualisation**: contains the code for visualising the results.
- **/data**: contains all data files needed to run this project.
- **/doc**: contains the images needed to create some of the visualisations
- **/output**: contains results after running this project.

## Algorithms

### Random Algorithm
This algorithm will randomly assign houses to battery, while checking if the battery has enough capacity left. If succeeded, a path of cables will be randomly created between houses and batteries. The paths will never return the way it came from.

**Problems**  
This algorithm is very inefficient, both for pairing and creating paths. It's also not possible to find a valid solution for all three districts. When running this algorithm, a smaller test district will be used.

### Greedy Algorithm
This algorithm will assign houses to the nearest battery and paths will be created in the right direction. When assiging the houses, the houses are sorted by max output. Then, if capacity of the batteries are exceeded, five houses will be reassigned and its path recreated.

**Problems**  
Using this algorithms allows only one way of assiging houses. As a result, this algorithm only results in a valid solution for district 1.

### Hill Climber
This algorithm creates a random start state using the Random and Greedy algorithms. First it will assign randomly the houses to the batteries, and secondly will create the paths in the right direction.

Subsequently, a number of N iterations are run where in each iteration a mutation is performed. During this mutation, a house from each battery is randomly removed and reassigned. The paths will also be recreated. Then, total costs for both states will be compared. The next iteration starts with the best state.

### Simulated Annealing

**Main**

**Code**
*Object Classes*
- Grid
- Battery
- House
- Route

*Algorithms*
- Random
- Greedy
- Hill Climber
- Simulated Annealing

*Visualisation*
- visualise (grid / annealing)

**Data**
- battery specifics
- house specifics

**Doc**
- battery image
- house image

## Authors
- Vincent Engelhard
- Lotte Kaatee
- Pamela Sneekes