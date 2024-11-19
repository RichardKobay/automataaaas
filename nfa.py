from graphviz import Digraph

class NFA:
    def __init__(self, states=None, alphabet=None, start_state=None, accept_states=None):
        """
        Initialize an NFA object.

        :param states: Set of states (Q).
        :param alphabet: Set of input symbols (Σ).
        :param start_state: Initial state.
        :param accept_states: Set of accepting states.
        """
        self.states = states if states else set()
        self.alphabet = alphabet if alphabet else set()
        self.start_state = start_state
        self.accept_states = accept_states if accept_states else set()
        self.transitions = {}  # {(state, symbol): {next_states}}

    def add_state(self, state):
        """Add a state to the NFA."""
        self.states.add(state)

    def set_start_state(self, state):
        """Set the start state."""
        if state in self.states:
            self.start_state = state
        else:
            raise ValueError("State must be added before setting as start state.")

    def add_accept_state(self, state):
        """Add a state to the set of accept states."""
        if state in self.states:
            self.accept_states.add(state)
        else:
            raise ValueError("State must be added before marking as an accept state.")

    def add_transition(self, current_state, symbol, next_states):
        if current_state not in self.states:
            raise ValueError(f"State {current_state} not found in states.")
        if not all(state in self.states for state in next_states):
            raise ValueError("All next states must be added to the NFA first.")
        if symbol and symbol not in self.alphabet:
            raise ValueError("Symbol must be in the alphabet or None for epsilon.")

        key = (current_state, symbol)
        if key not in self.transitions:
            self.transitions[key] = set()
        self.transitions[key].update(next_states)
        print(f"Added transition: {key} -> {self.transitions[key]}")  # Debug

    def print_transitions(self):
        print("Transitions:")
        for key, value in self.transitions.items():
            print(f"{key} -> {value}")

    def epsilon_closure(self, states):
        """
        Compute the epsilon closure of a set of states.

        :param states: Set of states to compute epsilon closure for.
        :return: The epsilon closure as a set of states.
        """
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            epsilon_moves = self.transitions.get((state, None), set())
            for next_state in epsilon_moves:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def validate_string(self, input_string):
        """Validate if the input string is accepted by the NFA."""
        current_states = self.epsilon_closure({self.start_state})  # Start with epsilon closure
        print(f"Initial states: {current_states}")  # Debug
        for symbol in input_string:
            print(f"Processing symbol: {symbol}")
            next_states = set()
            for state in current_states:
                # Collect all states reachable by the current symbol
                next_states.update(self.transitions.get((state, symbol), set()))
            print(f"Next states before epsilon closure: {next_states}")
            # Update current states with epsilon closure of next states
            current_states = self.epsilon_closure(next_states)
            print(f"Current states after epsilon closure: {current_states}")
            if not current_states:
                # Early exit if no states are reachable
                print("No states reachable. String rejected.")
                return False

        # Check if any current state is an accepting state
        result = any(state in self.accept_states for state in current_states)
        print(f"String accepted? {result}")  # Debug
        return result

    def plot(self, output_file="nfa", file_format="png"):
        """
        Plot the NFA using Graphviz.

        :param output_file: Name of the output file (default is 'nfa').
        :param file_format: Format of the output file (default is 'png').
        """
        dot = Digraph(format=file_format)

        # Add states
        for state in self.states:
            if state in self.accept_states:
                dot.node(state, shape="doublecircle")  # Accept states
            else:
                dot.node(state, shape="circle")

        # Add start state marker
        if self.start_state:
            dot.node("start", shape="point")  # Invisible start node
            dot.edge("start", self.start_state)

        # Add transitions
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                label = "ε" if symbol is None else symbol
                dot.edge(state, next_state, label=label)

        # Render the graph
        dot.render(output_file, cleanup=True)
        print(f"NFA plotted to {output_file}.{file_format}")
