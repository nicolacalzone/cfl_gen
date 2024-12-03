class TreeNode:
    def __init__(self, value, index=None):
        self._value = value      # Symbol of the node (e.g., 'A', 'B', 'a')
        self._index = index      # Index of the node for the generation of the sentence
        self._children = []      # List of children of the node
        self._linked_node = None # Reference to a node in another tree
    
    def add_child(self, child):
        self._children.append(child)

    def set_children(self, children):
        self._children = children

    def get_children(self):
        return self._children
    
    def get_value(self):
        return self._value
    
    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index
    
    def link_to(self, other_node):
        """Link this node to a node in another tree."""
        if isinstance(other_node, TreeNode):
            self._linked_node = other_node
        else:
            raise ValueError("other_node must be an instance of TreeNode")

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self._value) + " (Index: {})\n".format(self._index)
        for child in self._children:
            ret += child.__repr__(level + 1)
        #if self._linked_node:
        #    ret += "\t" * level + "Linked to: " + repr(self._linked_node._value) + "\n"
        return ret
    

    def reorder_tree(self, root):
        if not root:
            return None


        ## Change the indexes of the children
        levels = []
        for i, child in enumerate(root.get_children()):
            level = 1
            print(child.get_value(), child.get_index())
            if child.get_children():
                level += 1
                levels.append(level)
                print(f"levels of child_{i}: ", level)

        print(levels)
        child_array = []
        for i, child in enumerate(root.get_children()):
            if child.get_children():
                child.set_index(levels[i])
                child_array.append(child)
            else:
                print(f"child_{i} has no children")
                child_array.append(child)
                print(child_array)

    def sort__children(self):
        """Sort children at each level based on the index, with integers before 't'."""
        # Sort children: first by integer indices, then by 't' if present
        self._children.sort(key=lambda x: (x._index != 't', x._index))
        
        # Recursively sort children for each child node
        for child in self._children:
            child.sort_children()

        return self 

    def sort_children(self):
        """Sort children with integer indices, leaving 't'-indexed nodes in their original order."""
        # Separate children into two lists based on the index type
        int_index_children = [child for child in self._children if isinstance(child._index, int)]
        t_index_children = [child for child in self._children if child._index == 't']
        
        # Sort only the integer-indexed children
        int_index_children.sort(key=lambda x: x._index)
        
        # Combine sorted integer nodes with 't' nodes in their original order
        self._children = int_index_children + t_index_children
        
        # Recursively sort children for each child node
        for child in self._children:
            child.sort_children()

        return self



from nltk.grammar import Nonterminal

tree = TreeNode('S')
tree.add_child(TreeNode(Nonterminal('A'), 2))
tree.add_child(TreeNode(Nonterminal('B'), 1))

tree.get_children()[0].add_child(TreeNode(Nonterminal('A'), 1))
tree.get_children()[0].add_child(TreeNode(Nonterminal('a'), 't'))
tree.get_children()[0].get_children()[0].add_child(TreeNode(Nonterminal('a'), 't'))

tree.get_children()[1].add_child(TreeNode(Nonterminal('b'), 't'))
tree.get_children()[1].add_child(TreeNode(Nonterminal('B'), 1))
tree.get_children()[1].get_children()[1].add_child(TreeNode(Nonterminal('b'), 't'))

print(tree)

reordered_tree = tree.sort_children()

print(reordered_tree)