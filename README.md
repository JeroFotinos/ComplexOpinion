<h1 align="center"> Complex Opinon </h1>


![Badge Development](https://img.shields.io/badge/STATUS-DEVELOPMENT-green)
![GitHub Org's stars](https://img.shields.io/github/stars/alxrojas?style=social)

The complex_opinion package allows for comfortable exploration of opinion models in sociophysics, by wrapping networkx graphs, used as topologies, and adding to them different methods for the opinion dynamics.


## Features

- `OpinionModel`: The `OpinionModel` class wraps a networkx graph as topology, and is equipped with different methods for the opinion dynamics.


## Examples

#### Initializing an Opinion Model
First use networkx to declare a topology, then use it to instance an Opinion Model
```python
import networkx as nx
import complex_opinion as cx

# Generate Watts-Strogatz network
number_of_nodes = 500
k = 5
p = 0.01
graph = nx.watts_strogatz_graph( number_of_nodes , k , p , seed = 896803 )

# instance the OpinionModel class with graph as topology
model = cx.OpinionModel(graph)
```
#### Evolving an opinion dynamics
The `OpinionModel` class is equipped with different opinion dynamics methods.

#### Accesing networkx graph features
You can access any Networkx feature keeping in mind that the `topology` attribute of the `OpinionModel` class is a Networkx graph. 

## Dependencies
 This package needs (and therefore installs) other packages, namely:

- [numpy](https://numpy.org/): Data analysis and calculation
- [networkx](https://networkx.org/): Network Analysis in Python

## Authors

| [<sub>Jerónimo Fotinós</sub>](https://github.com/JeroFotinos) | <sub>María Cecilia Gimenez</sub> |  <sub>Mahdi</sub> |
| :---: | :---: | :---: |

## License
This project is licensed under (MIT) - Look at the LICENSE file in the [Repo](https://github.com/JeroFotinos/ComplexOpinion) for details.

## Expressions of gratitude

* Tell others about this project
* Cite our project in your paper
