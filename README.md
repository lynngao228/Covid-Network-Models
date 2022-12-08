# Covid-Network-Models

Simulated social distancing and Covid-19 infection spread within models of UCI’s Math Department and used enrollment data from Spring 2020 to increase simulation accuracy.
5 Network Models are discussed and simulated:
\begin{enumerate}
    \item Spatial-Random Network Model: individuals are connected to their local neighbors.
    \item Scale-Free (Barabasi-Albert) Network Model: individuals have non-local connections, and a few individuals having a disproportionately large number of connections
    \item Hybrid Network: a spatial scale-free network. The backbone consists of spatial network connections, with a set of long-range connections.
    \item Small world (Watts-Strogatz) Network Model: individuals are connected to their local neighbors but these connections are rewired at a certain probability. 
    \item Stochastic Block Model: individuals are separated into blocks. These individuals have a certain probability of being connected with those in the same block and a different probability (usually lower) of being connected to individuals in other blocks.
\end{enumerate}
