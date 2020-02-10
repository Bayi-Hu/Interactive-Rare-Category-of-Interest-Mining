## Interactive-Rare-Category-of-Interest-Mining

Code and datasets released for the paper ["Interactive-Rare-Category-of-Interest-Mining"](https://)

 ```
├── Code
│     ├── IRim_RCD.py
│     ├── IRim_RCE.py
│     ├── Offline_abstraction.py
│     └── Configuration.py
├── Dataset
│     ├── Abalone
│     ├── Bird*
│     ├── Shuttle
│     ├── Kddcup
│     └── Game*
├── Interval_abstraction
│     ├── Abalone
│     ├── Bird
│     ├── Shuttle
│     ├── Kddcup
│     └── Game
├── README
 ```

### **Code**

`IRim_RCD.py` is the IRim algorithm for rare category detection.

`IRim_RCE.py` is the IRim algorithm for rate category exploration.

`Offline_abstraction` is the code for offline abstraction construction process.

`Configuration.py` is the parameter configuration used in the experiment.

### **Dataset**

Abalone, Shuttle and Kddcup are commonly used for rare category mining in academia. **Bird** and **Game** are two new datasets proposed by us and will be released soon.
 
### **Interval Abstraction**

Following the settings of the paper, 

### Usage

To run the code, you may first run ` Offinle_abstraction.py`  for abstraction construction, then run `IRim_RCD.py` to interactively detect few samples for rare-category-of-interest, and eventually run `IRim_RCE.py` to explore as much as possible samples from rare-category-of-interest.      

### Citation
please use the following bibtex entry:

