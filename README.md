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
│     ├── Bird*
│     ├── Shuttle
│     ├── Kddcup
│     └── Game*
├── README
 ```

### **Code**

`IRim_RCD.py` is the IRim algorithm for rare category detection.

`IRim_RCE.py` is the IRim algorithm for rate category exploration.
 
`Offline_abstraction` is the code for offline abstraction process.

`Configuration.py` is the parameter configuration used in the experiment.

### **Dataset**

Abalone, Shuttle and Kddcup are commonly used for rare category mining in academia. 

**Bird**\* and **Game**\* are two new datasets proposed by us.
 
For downloading **Bird**, please refer to https://drive.google.com/file/d/1Fol8y2OHads3juIQEQGv8CubhMzXn8Wr/view?usp=sharing.

For downloading **Game**, please refer to https://drive.google.com/file/d/1c6TggTzzenKRV6TwrRn2gKmmlwLLTEPB/view?usp=sharing.
 
### **Interval Abstraction**

Following the settings of the paper, interval abstraction will be built during the offline abstraction procedure. It mainly includes five files: `Abs_idx, Abs_idx_lst, Abs_scr, AbsIdx2Idx, Dist.npy, Idx2AbsIdx and NNindex.npy`.

### Usage

To run the code, you could first run ` Offinle_abstraction.py`  for abstraction construction, and then run `IRim_RCD.py` to interactively detect few samples for rare-category-of-interest, and eventually run `IRim_RCE.py` to explore as much as possible samples from rare-category-of-interest.      

### Citation
please use the following bibtex entry:



