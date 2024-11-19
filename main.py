from nfa import NFA

nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            start_state="q0",
            accept_states={"q2"}
        )

nfa.add_transition("q0", "a", {"q0", "q1"})
nfa.add_transition("q1", "b", {"q2"})
nfa.add_transition("q0", None, {"q2"})  # Epsilon transition

nfa.plot()
