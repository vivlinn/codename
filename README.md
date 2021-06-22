# Smart Grid
*Created by CodeName*

Green energy is the energy of the future, and self-producing is today's fashion. Nowadays, many houses have solar panels, windmills or other installations to produce their own energy. Fortunately, these installations often produce more energy than is necessary for their own consumption. The oversupply could be sold back to the supplier, but the infrastructure (the grid) is often not designed for this. Batteries must be installed to manage peaks in consumption and production.

To solve this problem, we will look at three residential areas, each containing 150 houses and 5 batteries. The houses are build with solar panels with a maximum output, while the batteries have a maximum capacity. The challenge is to connect houses with batteries using cables while keeping the costs as low as possible. 



**Part 1** 

For the first variant, the following requirements are set in place:
- Batteries cannot be connected to each to each other.
- A house cannot be connected to multiple batteries.
- Each house is connected to a battery through their own cable.
-  Multiple cables are allowed to run over the same gridsegments. However, each house will still have their own unique cable, and this will not reduce costs.



## installments
```bash
python -m pip install -U pip
```

```bash
python -m pip install -U matplotlib
```







# Files

The project consists of :

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