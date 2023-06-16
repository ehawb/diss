Full disclaimer: This will be the hardest part of my code for me to try and explain since I don't have nearly as much experience with GAP as Python. I did learn a decent amount for this part of the project, but it felt more like me being in "survival" mode in GAP rather than "creative" mode... If you try to work through any of this stuff and you feel confused/stuck, please reach out to me and I will do my best to help. My email address is on my GitHub profile. This code is ultimately here because I'd like to help people learn how to do this stuff, so I will be glad to answer questions and possibly improve my code/explanation here in the process.

# Working with graphs in GAP
GAP (Groups, Algorithms, and Programming) is software I used to work with groups. Here is a link to the GAP website: https://www.gap-system.org/

I usually work with GAP by writing code in a .txt file in a basic text editor. My usual choices are either the regular Notepad app on Windows, or Notepad++ (https://notepad-plus-plus.org/downloads/). I started out working with GAP just through the GAP console, but I abandoned this approach fairly quickly because it was really frustrating whenever I made mistakes. That being said, folks who prefer that method could just manually enter the commands from the .txt files if they truly want to work within the GAP console for some reason. On the other hand, sometimes my instructions here say to open GAP and enter some commands; you could write those commands in a .txt file that you then read in from GAP.
## `nx_to_GAP.py` module
As the name implies, the `nx_to_GAP.py` module here is a way to convert NetworkX graph objects into graphs that GAP can work with. To use the module, define the following:
- `graph` should be a NetworkX graph. You can use a graph6 code or one of the built-in NetworkX graphs.
- `save_dir` is the directory where the GAP script will be saved.
    - I recommend making this directory as short/quick to type as possible, because you'll be typing it in the GAP console. 
- `graph_name` is a string that corresponds to a name for your graph. This is how the file will be saved in the aforementioned directory.
Once you run the module, a GAP script will be written and saved, and an address for the file will be printed. Here is an example of what the GAP script for the cycle graph $C_5$ looks like:

```
LoadPackage("grape"); 
 A := [[0,1,0,0,1], 
[1,0,1,0,0], 
[0,1,0,1,0], 
[0,0,1,0,1], 
[1,0,0,1,0]]; 
 graph :=  Graph( Group(()), [1..5], OnPoints, function(x,y) return A[x][y]=1; end, true );
    G := AutGroupGraph(graph);
```
Basically, it writes an adjacency matrix for the graph in the correct GAP syntax, defines a graph in GAP, and defines G as the automorphism group of the graph. These will be used later.
It also loads the `grape` package for GAP in the beginning just to make sure it's ready to go. Read more about GRAPE here: https://www.gap-system.org/Packages/grape.html

## Using the output from `nx_to_GAP.py` to get the automorphism group of the graph
Once you have the script from the NetworkX graph, open GAP. Type the following command:

`Read("C:/path_to_previous_file");`

where "C:/path_to_previous_file" is wherever your GAP script was saved by the `nx_to_GAP` module.
GAP will read the group $G$ in from the script, and now you can identify it by using the following command:

`IdGroup(G)`

The output will be something like $[n, q]$, where $n$ is the order of the group, and $q$ is the position of $G$ in GAP's list of groups of order $n$. I usually use this website to learn more about the group: https://people.maths.bris.ac.uk/~matyd/GroupNames/about.html

At that website, you can type $n, q$ in the upper left search bar to pull up the group.

## Is my graph potentially a Cayley graph?
Now that you've explored your graph and its automorphism group, suppose you're wondering if the graph is a Cayley graph. Let $\Gamma$ be the graph, and let $G$ be the automorphism group of the graph, i.e. $G = \text{Aut}(\Gamma)$. To determine whether $\Gamma$ is a Cayley graph, the first question is whether $G$ has a subgroup of order $\lvert \Gamma \rvert$.

Use GAP to read the `subgroups_given_order.txt` file from the `cayley_utils` folder in this repo. You could also copy and paste the file somewhere that it's easier to access. It has a function called `subgroups_order_k` that takes a group $G$ and an integer $k$ as input, then returns all subgroups of order $k$ in $G$. So in the above context, after running 

`Read("subgroups_given_order.txt")` 

(for wherever you have the script saved), you should enter the following command:

`subgroups_order_k(G, k)`, 

where $k = \lvert \Gamma \rvert$.

If it returns a list of groups, your graph is *potentially* a Cayley graph. If it returns an empty list, your graph is definitely not a Cayley graph.

# Fully worked example: $C_5$ is a Cayley graph
This section shows how to verify that a given graph is indeed a Cayley graph by using $C_5$ as a (hopefully) straightforward example. If you're working through this and face any difficulties, please let me know, because I would be glad to try and improve it.

1. Open the `nx_to_GAP.py` module.
-   Define `graph = nx.cycle_graph(5)`
-   Define your `save_dir` and `graph_name`. Of course, 'C5' is a good graph name!

2. Open GAP, and read the file generated in Step 1.

    *Hint: use the command `Read("my_file.txt");`*

3. Read the `subgroups_given_order.txt` file from the previous section. Since $C_5$ is a graph of order 5, run the following command after reading that file in:

    `subgroups_order_k(G, 5);`
    
    It should return exactly one such subgroup. We will now work with this subgroup $H$ directly to see if $C_5$ can be represented as a Cayley graph for $H$ and some subset $S$ of $H$.
    
4. Define the subgroup as $H$ by using the following command:

   `H := subgroups_order_k(G, 5)[1];`
   
5. What group is this? Identify it using a command.

   *Hint: use the command `IdGroup(H);`*
   
   It's the group $[5, 1]$ in GAP.

6. Make a copy of this group by using the following command (or something similar):

   `H_prime := SmallGroup(5, 1);`
   
7. Now, we want to see what this group "looks like" within the automorphism group of the graph. 
 - There is a file called `isomorphic_subgroup_image.txt` in the `cayley_utils` folder of this code. Read it in.
 - Run the command `isomorphic_subgroup_image(H, H_prime);`
 - The output should look like this:
```
 <identity> of ... --> ()
f1 --> (1,2,3,4,5)
f1^2 --> (1,3,5,2,4)
f1^3 --> (1,4,2,5,3)
f1^4 --> (1,5,4,3,2)
```

The group $SmallGroup(5, 1)$ is the cyclic group of order 5. The output above is telling us that if $f_1$ is the generator of $G$ (using GAP's notation here), that corresponds to the graph automorphism $(1\,2\,3\,4\,5)$. Similarly, $f_1^3$ corresponds to the graph automorphism $(1\,4\,2\,5\,3)$. The identity element of $G$ corresponds to the identity permutation of the automorphism group of the graph. This will help us select our set $S$ soon.

We need to run a quick check that this subgroup coincides with a simply transitive action on the vertex set (Sabidussi's theorem; see the dissertation). That is, for any two vertices $u$ and $v$ in the vertex set of our graph, we must verify that there is exactly one permutation in this subgroup above that sends $u$ to $v$.

This is a small enough example that it can be verified by hand. I actually did this for all of the Cayley graphs in my dissertation. I'm not sure how to automate this in GAP just yet, but that's a future project if anyone wants to help! :)

8. This is the fun part! Choose an arbitrary vertex of the graph to be labeled as the identity element. For the sake of this example, I'll choose 1 because it's easy.
9. We need a quick reminder of the edges of the graph we put into GAP. Enter the following command:

   `graph;`
   
   The `adjacencies` part of the output gives the neighbors of each vertex in order. Since we get
   
   `adjacencies := [ [ 2, 5 ], [ 1, 3 ], [ 2, 4 ], [ 3, 5 ], [ 1, 4 ] ], ...`
   
   This means 
   -1 is adjacent to 2 and 5; 
   -2 is adjacent to 1 and 3; 
   -3 is adjacent to 2 and 4; 
   -4 is adjacent to 3 and 5; and 
   -5 is adjacent to 1 and 4.
10. Consider the vertex selected in Step 8. Since I chose 1, I'll use that here. What are 1's neighbors in the graph? Based on the previous step, the neighbors of 1 are 2 and 5.
11. Which permutations in the subgroup send 1 to its neighbors? Look back at Step 7.
    The permutation that sends 1 to 2 is $(1\,2\,3\,4\,5)$. This permutation corresponds to $f_1$.
    The permutation that sends 1 to 5 is $(1\,5\,4\,3\,2)$. This permutation corresponds to $f_1^4$.
12. The elements we selected in Step 11 form our set $S$. To recap, let $(\mathbb{Z}_5, +)$ be the cyclic group of order 5. This group is generated by the element 1, so 1 corresponds to $f_1$. Hence 4 corresponds to $f_4$. Based on our above calculations, the graph $C_5$ is a Cayley graph
```math
\Gamma((\mathbb{Z}_5, +), \{1,4\}).
```
