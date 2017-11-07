[![Build Status](https://travis-ci.org/mumbleskates/data-structures.svg?branch=master)](https://travis-ci.org/mumbleskates/data-structures)
[![Coverage Status](https://coveralls.io/repos/github/mumbleskates/data-structures/badge.svg?branch=master)](https://coveralls.io/github/mumbleskates/data-structures?branch=master)


# data-structures

## This project contains sample code for implementing the following structures:

### Trie
Ordered tree data structure used to store an associative array where we care about the path to the leaf, rather than
any individual content of a node. Implements insert and contains methods.

### Insertion Sort
Insertion-sort is an in-place sorting algorithm with O(n^2) average- & worst-case, O(n) best-case time complexity.

### Merge Sort
Merge-sort is a non in-place sorting algorithm with O(n log n) best- & worst-case time complexity.

### Radix Sort
Radix sort is an efficient sorting algorithm that orders numbers by taking them apart digit by digit rather than
comparing them directly. Time complexity is always a virtually constant O(n log k), where k is the length of the
largest number (in this case, in hexadecimal).

### Quick Sort
Quicksort is an in-place sorting algorithm with O(n log n) best- & average-case, O(n^2) worst-case time complexity.

### Binary Search Tree
A Python implementation of a Binary Search Tree (BST). The value of each node in the BST is greater than the values
stored in its left sub-tree, and smaller than the values in its right sub-tree. 
The BST has four traveral patterns: in-order, pre-order, post-order, and breadth-first.

### Graph

Graphs(g) are used to record relationships between things. Popular uses of 
graphs are mapping, social networks, chemical compounds and electrical 
circuits.

Supports:

g.depth_first_traversal(start): Perform a full depth-first traversal of 
the graph beginning at start. Return the full visited path when traversal 
is complete.

g.breadth_first_traversal(start): Perform a full breadth-first traversal 
of the graph, beginning at start. Return the full visited path when 
traversal is complete.

### WeightedGraph

A subclass of the above which can optionally store and provide weights for each
edge. This class also supports shortest-path traversals for graphs with and without
negative edge weights.

g.dijkstra_traversal(start, end): An algorithm for finding the shortest 
paths between nodes in a graph, which may represent, for example, road networks.

g.bellman_ford(node): An algorithm that computes shortest paths from a 
single source node to all of the other nodes in the graph. Slower than Dijkstra's 
algorithm for the same graph, but more versatile, as it is capable of handling graphs
in which some of the edge weights are negative numbers. 

This example walks a graph from a set vertex and sets each vertex
with a previous vertex and weight. It then returns a dictionary of all the 
vertices that you can then use to walk back to the provided vertex along the
smallest weighted path.

### Binary Heap

This data structure, Heap, is a specialized tree-based data structure that 
satisfies the heap property: If A is a parent node of B then the key of 
node A is ordered with respect to the key of node B with the same ordering 
applying across the heap. Fills from left to right. There are minHeap 
and maxHeap alternatives.

### Priority Queue

This data structure, a priority queue, is an abstract data type which is 
like a regular queue or stack data structure, but where additionally each 
element has a "priority" associated with it.

### Deque

This data structure, Deque (usually pronounced like "deck"), is an irregular acronym of double-ended 
queue. Double-ended queues are sequence containers with dynamic sizes that can be expanded or 
contracted on both ends (either its FRONT(head) or REAR(tail)).

### Queue

This data structure, a Queue, is an abstract data type or a linear data structure, in which the first element is 
inserted from one end called REAR(or tail), and the deletion of existing element takes place from the other end 
called as FRONT(or head).

### Doubly Linked List

This data structure is a linked data structure that consists of a set of sequentially linked records called nodes. Each 
node contains two fields, called _next and _prev, that are references to the previous(_prev) and to the next(_next) node 
in the sequence of nodes.

### Stack

This data structure that allows for a Last In First Out (LIFO) access to a collection of objects (nodes), each
containing a link to its successor and a piece of data. Access is given through the methods push(), adding an item to
the stack, or pop(), removing an item from the stack.

### Linked List

This data structure has an ordered set of data elements (nodes), each containing a link to its successor and a piece of
data.

### LRU Cache

A dict-like structure that evicts least-recently-used entries when new entries are added until some maximum total cost
is achieved. This is implemented as usual, using a hash-map concurrent to a doubly linked list that establishes recency
order.

## *Interview Challenge: Proper Parenthetics*

Takes a unicode string proper_paren(text) as input and returns one of three possible values:

> Return 1 if the string is “open” (there are open parens that are not closed)
> Return 0 if the string is “balanced” (there are an equal number of open and closed parentheses in the string)
> Return -1 if the string is “broken” (a closing parens has not been proceeded by one that opens)
