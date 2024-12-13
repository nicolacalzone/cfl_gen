from nltk import Nonterminal
import random as rand
import logging as log
import re 
from collections import Counter



log.basicConfig(filename='logs/app.log', 
                    filemode='a',
                    level=log.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


#################################################################
# Productions
################################################################# 

class ProductionElement:
    def __init__(self, symbol, index):
        self._symbol = symbol
        self._index = index 
        self._isnonterminal = isinstance(symbol, Nonterminal)
    
    def symbol(self):
        return self._symbol
    
    def index(self):
        return self._index
    
    def isnonterminal(self):
        return self._isnonterminal
    
    def __repr__(self):
        return f"{self._symbol}, {self._index}, {self._isnonterminal}"

class SynchronousProduction:
    """
    lhs -> (source_rhs, target_rhs)
    """

    def __init__(self, lhs, source_rhs, target_rhs, indexes_source, indexes_target):
        ## Given
        self._lhs = lhs
        self._source_rhs = source_rhs               # right-hand side for the source language - FIRST LANGUAGE
        self._target_rhs = target_rhs               # right-hand side for the target language - SECOND LANGUAGE
        self._indexes_source = indexes_source
        self._indexes_target = indexes_target

        ## Derived
        self._same_order = self._indexes_source == self._indexes_target

    def list_source_elements(self):
        return [ProductionElement(elem, idx) for elem, idx in zip(self._source_rhs, self._indexes_source)]
    
    def list_target_elements(self):
        return [ProductionElement(elem, idx) for elem, idx in zip(self._target_rhs, self._indexes_target)]
        
    def lhs(self):
        """Return the left-hand side nonterminal."""
        return self._lhs
    
    def source_rhs(self):
        """Return the right-hand side for the source language."""
        return self._source_rhs
    
    def target_rhs(self):
        """Return the right-hand side for the target language."""
        return self._target_rhs
    
    def source_indexes(self):
        """Return the indexes of the source language."""
        return self._indexes_source
    
    def target_indexes(self):
        """Return the indexes of the target language."""
        return self._indexes_target
    
    def same_order(self):
        """Return True if the source and target indexes are the same."""
        return self._same_order

    def __repr__(self):
        """Return a string representation of the production."""
        return f"{self._lhs} -> {' '.join(map(str, self._source_rhs))} // {' '.join(map(str, self._target_rhs))}"

#################################################################
# Grammars
#################################################################

class TreeSynCFG:
    
    def __init__(self, start, productions):
        self._start = start
        self._productions = productions
        self._class_name = "TreeSynCFG"
        self._translated_grammar = []

    def get_productions(self):
        return self._productions
    
    def get_start(self):
        return self._start
    
    def list_productions(self):
        list_elements = []
        for prod in self._productions:
            list_elements.append((prod.list_source_elements(), prod.list_target_elements()))
        return list_elements

    @staticmethod
    def error_checker(source_rhs, target_rhs, source_indexes, target_indexes):
        """Check for errors in the productions."""

        if len(source_rhs) != len(target_rhs):
            log.error(f"Source and target right-hand sides must have the same length. Found: {len(source_rhs)} and {len(target_rhs)}")
            raise ValueError(f"Source and target right-hand sides must have the same length. Found: {len(source_rhs)} and {len(target_rhs)}")
        
        if len(source_indexes) != len(target_indexes):
            log.error(f"Source and target indexes must have the same length. Found: {len(source_indexes)} and {len(target_indexes)}")
            raise ValueError(f"Source and target indexes must have the same length. Found: {len(source_indexes)} and {len(target_indexes)}")
        
        if len(source_rhs) != len(source_indexes):
            log.error(f"Source right-hand side and indexes must have the same length. Found: {len(source_rhs)} and {len(source_indexes)}")
            raise ValueError(f"Source right-hand side and indexes must have the same length. Found: {len(source_rhs)} and {len(source_indexes)}")
        
        if len(target_rhs) != len(target_indexes):
            log.error(f"Target right-hand side and indexes must have the same length. Found: {len(target_rhs)} and {len(target_indexes)}")
            raise ValueError(f"Target right-hand side and indexes must have the same length. Found: {len(target_rhs)} and {len(target_indexes)}")
         
        # Check if # of nonterminals match
        source_counter = Counter([elem.symbol() for elem in source_rhs if isinstance(elem, Nonterminal)])
        target_counter = Counter([elem.symbol() for elem in target_rhs if isinstance(elem, Nonterminal)])
        if source_counter != target_counter:
            log.error("Nonterminal counts do not match between source and target RHS")
            raise ValueError("Nonterminal counts do not match between source and target RHS")

        # Check if indexes match for each nonterminal
        source_index_map = {f"{elem.symbol()}{idx}": idx for elem, idx in zip(source_rhs, source_indexes) if isinstance(elem, Nonterminal)}
        target_index_map = {f"{elem.symbol()}{idx}": idx for elem, idx in zip(target_rhs, target_indexes) if isinstance(elem, Nonterminal)}
        if source_index_map != target_index_map:
            log.error("Nonterminal indexes do not match between source and target RHS")
            raise ValueError("Nonterminal indexes do not match between source and target RHS")

    @classmethod
    def fromstring(cls, grammar_str: str):

        method_name = "TreeSynCFG.fromstring()"

        productions = []
        for line in grammar_str.strip().splitlines():

            if line:
                if '//' not in line or "->" not in line:
                    raise ValueError(f"Unable to parse line: {line}. Expected '//' and '->'.")

                source_rule, target_rhs = line.split('//')
                lhs, source_rhs = source_rule.split('->') 
                lhs = lhs.strip()

                source_rhs = source_rhs.strip()
                target_rhs = target_rhs.strip()

                #print(lhs, "->", source_rhs, "//", target_rhs)

                source_elements = re.findall(r'(\w+)(?:\{(\d+)?\})?', source_rhs) 
                target_elements = re.findall(r'(\w+)(?:\{(\d+)?\})?', target_rhs)

                #print(source_elements, target_elements)
                
                source_rhs_clean = []
                source_indexes = []

                i = 0
                for elem, idx in source_elements:
                    source_rhs_clean.append(Nonterminal(elem) if elem.isupper() else elem)
                    
                    if elem.isupper(): 
                        source_indexes.append(int(idx) if idx else i)
                        i += 2  
                    else:  
                        source_indexes.append(int(idx) if idx else i)
                        i += 1  

                                                                    
                target_rhs_clean = []
                target_indexes = []
                i = 0
                for elem, idx in target_elements:
                    target_rhs_clean.append(Nonterminal(elem) if elem.isupper() else elem)
                    
                    if elem.isupper(): 
                        target_indexes.append(int(idx) if idx else i)
                        i += 2  
                    else:  
                        target_indexes.append(int(idx) if idx else i)
                        i += 1  

                
                TreeSynCFG.error_checker(source_rhs_clean, target_rhs_clean, source_indexes, target_indexes)

                lhs = Nonterminal(lhs)
                prod = SynchronousProduction(lhs, source_rhs_clean, target_rhs_clean, source_indexes, target_indexes)
                productions.append(prod)

        return TreeSynCFG(Nonterminal('S'), productions)

    def _choose_production(self, symbol: str, p_factor: float, depth: int):
        """Choose a production for the given nonterminal symbol, favoring terminal productions as depth decreases."""
       
       ## Find Applicable Productions
        applicable_productions = [prod for prod in self._productions if prod.lhs() == symbol]

       # From Applicable Productions, 
       # find:
       #    - Terminal Productions 
       #    - Expandable Productions
        terminal_productions = [prod for prod in applicable_productions if len(prod.source_rhs()) == 1]
        expandable_productions = [prod for prod in applicable_productions if prod not in terminal_productions]

        # Increase the probability of choosing terminal productions as depth decreases
        if terminal_productions or (rand.random() > p_factor):   
            chosen_production = rand.choice(terminal_productions)
            log.info(f"Chosen terminal production: {chosen_production}")
            return chosen_production
        
        if expandable_productions:
            chosen_production = rand.choice(expandable_productions)
            log.info(f"Chosen expandable production: {chosen_production}")
            return chosen_production
        
        #log.debug("No applicable production found.")
        return None


    def generate_trees(self, p_factor: float, depth: int, source_symbol="S", target_symbol="S"):
        """Generate trees for both source and target synchronously."""

        if depth <= 0:
            log.info("Depth reached. Returning terminal nodes: {} and {}".format(source_symbol, target_symbol))
            return TreeNode(source_symbol), TreeNode(target_symbol)

        source_node = TreeNode(source_symbol)
        target_node = TreeNode(target_symbol)
        
        # Choose a production for the given symbol
        chosen_production = self._choose_production(source_symbol, p_factor, depth)
        if not chosen_production:
            log.info("No production available. Returning terminal nodes: {} and {}".format(source_symbol, target_symbol))
            return TreeNode(source_symbol), TreeNode(target_symbol)  # No productions available
        
        source_rhs = chosen_production.source_rhs()
        target_rhs = chosen_production.target_rhs()
        source_indexes = chosen_production.source_indexes()
        target_indexes = chosen_production.target_indexes()

        #print(f"Depth: {depth}")
        #print(f"Chosen production: {chosen_production}")
        #print(f"Source RHS: {source_rhs}, Target RHS: {target_rhs}")

        #for i, (source_sym, target_sym) in enumerate(zip(source_rhs, target_rhs)):

        for i, source_sym in enumerate(source_rhs):
            #print("i:", i, "\n\tsource_sym=", source_sym, "\tsrc_rhs[i]=", source_rhs[i], "\n\ttrg_rhs[i]", target_rhs[i])

            source_child, target_child = self.generate_trees(
                                                                p_factor, depth - 1,
                                                                source_sym, target_rhs[i],  
                                                            )

            source_node.add_child(source_child)
            target_node.add_child(target_child)

            source_node.link_to(target_node)
            target_node.link_to(source_node)

            if i < len(source_indexes) and i < len(target_indexes):
                position_source = source_indexes[i]
                position_target = target_indexes[i]

                source_child.set_index(position_source)
                target_child.set_index(position_target)

            log.debug(f"Source node at depth {depth}: {source_node}" + 
            f"\nSource child at depth {depth}: \n{source_child}")

            log.debug(f"Target node at depth {depth}: {target_node}" +
                      f"\nTarget child at depth {depth}: \n{target_child}")

        return source_node, target_node


    def generate_sentence(self, node):
        """Convert the tree into a sentence."""
        if node is None or not node.get_children():
            return node.get_value() if node else ""  # Nodo terminale: restituisce il valore

        sentence = []
        for child in node.get_children():
            child_sentence = self.generate_sentence(child)
            if not isinstance(child_sentence, Nonterminal):
                sentence.append(str(child_sentence))
        
        return " ".join(sentence)

    def produce(self, p_factor: float, depth: int):
        """Generate trees and sentences for both source and target."""
        
        source_tree, target_tree = self.generate_trees(p_factor, depth, self._start, self._start)
        target_tree_reordered = target_tree.sort_children()

        source_sentence = self.generate_sentence(source_tree)
        target_sentence = self.generate_sentence(target_tree_reordered)

        return source_tree, source_sentence, target_tree_reordered, target_sentence
    


    ######### SEPARATED METHODS #########
    """
        functions:
            - translate_grammar_for_parser(self)
            - append(set_, item)

        description:
            Two functions to translate the grammar into a grammar 
            that can be read by the parser in the main program.
    """
    @staticmethod
    def append(set_, item):
        if item[0] not in set_:
            set_[item[0]] = [(item[1], item[2])]
        else:
            set_[item[0]].append((item[1], item[2]))

    def translate_grammar_for_parser(self):
        """Generate a parser-like grammar"""
        parser_grammar = {}

        for i, prod in enumerate(self._productions):
            source_elements = prod.list_source_elements()
            target_elements = prod.list_target_elements()
            TreeSynCFG.append(parser_grammar, (prod.lhs(), source_elements, target_elements))

        return parser_grammar
        


#################################################################
#   Helper Structures
#################################################################

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
    

    def sort_children(self):
        """Sort children at each level based on the index, with integers before 't'."""
        # Sort children: first by integer indices, then by 't' if present
        self._children.sort(key=lambda x: (x._index))
        
        # Recursively sort children for each child node
        for child in self._children:
            child.sort_children()

        return self