# Genetic-Algorithm-for-MWISP
Implementin a genetic algorithm for Maximum Weighted Independent Set Problem

The format of the graph files is as follows:</br>
</br>
**Number of nodes**</br>
**Number of edges**</br>
**List of node weights** (format: X W where W is the weight of node X)</br>
**List of edges** (format: X Y which indicates an edge from node X to node Y)</br>

# Report of Project
**Initial Population**</br>
We generated n-digit string which is “n=Number of Nodes”. Each digits are
randomly created in between 0 and 1.</br>
We repeated this operation “k” times which is “k=Population Size”</br>
**Repair**</br>
After getting initial population, we are checking each string for feasibility. If
string is not feasible, repair operation starts.</br>
Repair function:</br>
We have “isFeasible” function which returns feasibility status and
infeasible nodes’ list. For example;</br>
">>status, list = isFeasible (Population)"</br>
status = False</br>
list = [(0,10),(0,20),(0,35),(42,0),…]</br>
We flipped the least-costed nodes. After each flipping, we are
checking feasibility. If string is still infeasible, repairing operations
continues.</br>
**Pool Selection**</br>
Firstly, we are adding fitness numbers to each string in population via
“add_fitness” function that uses “get_fitness” function and calculating
probability for each string. Then we are sorting the strings by descending
order.</br>
Now selection operation starts, we are generating a random number. From
begging the population we are comparing the random number and strings’
probability. If it fits we are adding this string to new population. And we are
doing this steps n-times (n=population size).</br>
**Crossover**</br>
We are generating a random number for each string pair. If random number is
less than our crossover probability, we are selecting a crossover point
randomly. Then we are doing crossover operation and adding to new
population list.</br>
**Mutation**</br>
We are generating a random number for each string. If random number is less
than our crossover probability, we flipping the ten random digits of string.</br>
  
![untitled](https://user-images.githubusercontent.com/33653098/40720679-351a0290-6420-11e8-990a-cc978887d09c.png)
