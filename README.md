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



## Installments

```bash
python -m pip install -U pip
```

```bash
python -m pip install -U matplotlib
```

### Get Started
To run this project, choose a district. See the following example to run the project for district 1. The number changes depending on chosen district.
```bash
python3 main.py 1
```
This will provide a command line interface where options will be available.

### Structure  
The following list describes the main folders and files for this project, and where to find them:
- **/code**: contains all code of this project.
    - **/code/algorithms**: contains the code for the algorithms.
    - **/code/classes**: contains the code for the classes
    - **/code/visualisation**: contains the code for visualising the results.
- **/data**: contains all data files needed to run this project.
- **/output**: contains results after running this project.



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