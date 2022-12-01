<h1 align="center"> complex_opinon </h1>


![Badge Development](https://img.shields.io/badge/STATUS-DEVELOPMENT-green)
![GitHub Org's stars](https://img.shields.io/github/stars/alxrojas?style=social)

The complex_opinion package allows for comfortable exploration of opinion models in sociophysics, by wrapping networkx graphs, used as topologies, and adding to them different methods for the opinion dynamics.


## Features

- `Opinion_Model`: The `Opinion_Model` class wraps a networkx graph as topology, and is equipped with different methods for the opinion dynamics.


## Examples

#### Initializing an Opinion Model
First use networkx to declare a topology, then use it to instance an Opinion Model
```python
import networkx as nx
import complex_opinion as cx

G = nx.watts_strogatz_graph( N , k , p , seed = 896803 )
m = cx.Opinion_Model(G)
```
#### Evolving an opinion dynamics


#### Accesing networkx graph features


## Dependencies
Things do you need to install the software:

- [numpy](https://numpy.org/): Data analysis and calculation
- [networkx](https://networkx.org/): Network Analysis in Python

## Authors

| [<sub>Jerónimo Fotinós</sub>](https://github.com/JeroFotinos) | <sub>María Cecilia Gimenez</sub> |  <sub>Mahdi</sub> |
| :---: | :---: | :---: | :---: |

## License
This project is licensed under (MIT) - Look at the LICENSE file in the [Repo](https://github.com/JeroFotinos/ComplexOpinion) for details.

## Expressions of gratitude

* Tell others about this project
* Cite our project in your paper
