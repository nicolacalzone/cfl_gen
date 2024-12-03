#################################################################
#              OUTDATED ---- NOT USED AND NOT UPDATED !!!!!
#################################################################

from nltk import Nonterminal
import random as rand
import logging as log
from datetime import datetime
import re 
from collections import Counter


log.basicConfig(filename='logs/app.log', 
                    filemode='a',
                    level=log.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

#################################################################
# Productions
#################################################################

class ProducedSentence:
    def __init__(self, symbols, indexes):
        self._symbols = symbols
        self._indexes = indexes

    def indexes(self):
        """Return the indexes."""
        return self._indexes
    
    def symbols(self):
        """Return the symbols."""
        return self._symbols
    
    ## ['a', 'b', 'c']
    def add_symbols(self, symbols):
        """Add symbols to the sentence."""
        self._symbols.extend(symbols)
    
    ## [1, 2, 3]
    def add_indexes(self, index):
        """Add indexes to the sentence."""
        self._indexes.extend(index)

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
        self._same_order = indexes_source == indexes_target
        self._nonterminals = [elem for elem in source_rhs if isinstance(elem, Nonterminal)]

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
        """Return True if the indexes are in the same order."""
        return self._same_order
    
    def nonterminals(self):
        """Return the nonterminals in the production."""
        return self._nonterminals

    def __repr__(self):
        """Return a string representation of the production."""
        return f"{self._lhs} -> {' '.join(map(str, self._source_rhs))} // {' '.join(map(str, self._target_rhs))}"

#################################################################
# Grammars
#################################################################

class SynchronousCFG:
    def __init__(self, start, productions, produced_sentence=None):
        self._start = start
        self._productions = productions
        self._produced_sentence = produced_sentence if produced_sentence is not None else []

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

    @staticmethod
    def fromstring(grammar_str):
        method_name="fromstring"
        lines = grammar_str.strip().splitlines()
        productions = []
        
        for line in lines:
            line = line.strip()
            if line:
                if '//' not in line:
                    log.error(f"Unable to parse line: {line}. Expected '//' to separate two rules.")
                    raise ValueError(f"Unable to parse line: {line}. Expected '//' to separate two rules.")
                
                source_rule, target_rhs = line.split('//')
                source_lhs, source_rhs = source_rule.split('->') 
                source_lhs = source_lhs.strip()

                source_rhs = source_rhs.strip()#.split() 
                target_rhs = target_rhs.strip()#.split()

                # S -> ['A', 'B'] // ['B', 'A']
       
                log.debug(f"1 {source_lhs} -> {source_rhs} // {target_rhs}")

                source_elements = re.findall(r'(\w+)(?:\{(\d+)?\})?', source_rhs) 
                target_elements = re.findall(r'(\w+)(?:\{(\d+)?\})?', target_rhs)
                
                #log.info(f"1 Source elements: {source_elements}") # Source elements: [('A', '1'), ('B', '2')]
                                                                  # Source elements: [('a', ''), ('A', '1')]

                #log.info(f"1 Target elements: {target_elements}") # Target elements: [('A', '1'), ('B', '2')]
                                                                  # Target elements: [('a', ''), ('A', '1')]

                source_rhs_clean = []
                source_indexes = []
                for elem, idx in source_elements:
                    source_rhs_clean.append(Nonterminal(elem) if elem.isupper() else elem)
                    source_indexes.append(int(idx) if idx else elem)
                                                                    
                target_rhs_clean = []
                target_indexes = []
                for elem, idx in target_elements:
                    target_rhs_clean.append(Nonterminal(elem) if elem.isupper() else elem)
                    target_indexes.append(int(idx) if idx else elem)
                
                log.info(f"1 Source indexes: {source_indexes}") # Source indexes: ['a', 1]  <-  a A 
                                                                # Source indexes: [1, 2]    <-  A B 
                log.info(f"1 Target indexes: {target_indexes}") # Target indexes: ['a', 1]  <-  a A
                                                                # Target indexes: [1, 2]    <-  A B

                log.info(f"1 Source RHS: {source_rhs_clean}") # Source RHS: [a, A]  <-  a A
                                                                # Source RHS: [A, B]  <-  A B   
                log.info(f"1 Target RHS: {target_rhs_clean}") # Target RHS: [a, A]  <-  a A
                                                                # Target RHS: [A, B]  <-  A B               

                # Check errors
                SynchronousCFG.error_checker(source_rhs_clean, target_rhs_clean, source_indexes, target_indexes)

                # Convert to Nonterminal 
                lhs = Nonterminal(source_lhs)

                # Create a synchronous production
                prod = SynchronousProduction(lhs, source_rhs_clean, target_rhs_clean, source_indexes, target_indexes)
                productions.append(prod)

        return SynchronousCFG(Nonterminal('S'), productions)

    def produce(self):
        """Print all synchronous productions."""
        for production in self._productions:
            log.info(production)
    
    def generate(self, source_symbol=None, target_symbol=None, depth=50):
        """Recursively generate sentences for both languages synchronously."""

        if source_symbol is None:
            source_symbol = self._start
        if target_symbol is None:
            target_symbol = self._start 

        source_sentence = []
        target_sentence = []
        self._generate_sentences(source_symbol, source_sentence, target_sentence, depth)



        return ' '.join(source_sentence), ' '.join(target_sentence)

    
    def _generate_sentences(self, source_symbol, source_sentence, target_sentence, depth):
        """Generate sentences for both languages synchronously."""
        
        if depth <= 0:
            return

        chosen_production = self._choose_production(source_symbol) 

        if chosen_production:
            source_sentence, target_sentence = self._expand_production(chosen_production, source_sentence, target_sentence, depth)   

            return ''.join(source_sentence), ''.join(target_sentence)

    def _choose_production(self, symbol):
        """Choose a production for the given nonterminal symbol."""

        # Applicable productions: [A -> a A // c A, A -> a // c]
        # Terminal productions: [A -> a // c]
        # Expandable productions: [A -> a A // c A]
        applicable_productions = [prod for prod in self._productions if prod.lhs() == symbol] 
        terminal_production = [prod for prod in applicable_productions if len(prod.source_rhs()) == 1]
        expandible_production = [prod for prod in applicable_productions if prod not in terminal_production]


        if expandible_production and rand.random() > 0.3:
            chosen_production = rand.choice(expandible_production)
            log.info(f"2 Chosen expandable production: {chosen_production}")
            return chosen_production
        
        elif terminal_production:
            chosen_production = rand.choice(terminal_production)
            log.info(f"2 Chosen terminal production: {chosen_production}")
            return chosen_production
        
        else:
            log.debug("No applicable production found.")
            return None

    def _expand_production(self, chosen_production, source_sentence, target_sentence, depth):
        """Expand the production based on source and target indexes, handling mixed types."""
    
        #     EXAMPLE
        # A -> a A // c A
        # 1st cycle
        #   source_sym = a , target_sym = c
        #   so here I get inside of the ELSE and I append source_sentence(a) and target_sentence(c)
        # 2nd cycle
        #   source_sym = A , target_sym = A
        #   so here I get inside of the IF and I call the function recursively

        #   WHAT IF i get into:
        #   source_sym = A , target_sym = c ??? 

        result = None
        produced_sentence = ProducedSentence(['eps', 'eps'], [0, 0])
        
        for source_sym, target_sym in zip(chosen_production.source_rhs(), chosen_production.target_rhs()):

            position_source = chosen_production.source_rhs().index(source_sym)
            position_target = chosen_production.target_rhs().index(target_sym)
            
            print(f"*** chosen_production: {chosen_production}")
            print(f"\tsource_sym: {source_sym}, target_sym: {target_sym}")

            if isinstance(source_sym, Nonterminal) and isinstance(target_sym, Nonterminal):
                result = self._generate_sentences(source_sym, source_sentence, target_sentence, depth - 1)
                print("\t", result)
            else:
                produced_sentence.add_symbols([source_sym, target_sym])
                produced_sentence.add_indexes([chosen_production.source_indexes(),
                                             chosen_production.target_indexes()])

                print("\tprod", chosen_production)
                print("\tsource_sym", source_sym)
                print("\ttarget_sym", target_sym)
                print("\tsource index", chosen_production.source_indexes()[position_source])
                print("\ttarget index", chosen_production.target_indexes()[position_target])


                #source_sentence.append(str(source_sym))
                #target_sentence.append(str(target_sym))


                ## QUESTO CODICE VIENE SALTATO
                if False == True:
                    if isinstance(source_sym, Nonterminal) and isinstance(target_sym, str):     ## [1, 'a'] -> ['a', 1]
                        pass
                    #elif isinstance(source_sym, str) and isinstance(target_sym, Nonterminal):   ## ['a', 1] -> [1, 'a']
                    #    pass
                    else:                                                                       ## ['a', 'b'] -> ['a', 'b'] 
                                                                                                ## ['a', 'b'] -> ['b', 'a']
                        print("\tprod", chosen_production)
                        #print("\tsource_sym", source_sym) 
                        #print("\ttarget_sym", target_sym)
                        #print("\tsource index", chosen_production.source_indexes())
                        #print("\ttarget index", chosen_production.target_indexes())
                        source_sentence.append(str(source_sym))
                        target_sentence.append(str(target_sym))

        return source_sentence, target_sentence
