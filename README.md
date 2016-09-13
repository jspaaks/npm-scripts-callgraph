# npm-scripts-callgraph

Python script to generate a [dot format](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) callgraph from a package.json's "script" key.


```
# say you have an npm package called helloworld
# (will write an output file in the current directory)
python callgraph.py ~/helloworld/package.json
```

You can then visualize the dot file using tools like [GraphViz](http://www.graphviz.org/). On Linux (Ubuntu/Debian), install GraphViz as follows:

```
sudo apt-get install graphviz
```

then

```
# write output in SVG format, see dot -? for your options
dot -Tsvg helloworld.dot -o callgraph-of-helloworld.svg
```
