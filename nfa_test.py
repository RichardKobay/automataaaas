import unittest
from nfa import NFA  # Assume the class is saved in a file named `nfa.py`

class TestNFA(unittest.TestCase):
    def setUp(self):
        """Set up a sample NFA for testing."""
        self.nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            start_state="q0",
            accept_states={"q2"}
        )
        self.nfa.add_transition("q0", "a", {"q0", "q1"})
        self.nfa.add_transition("q1", "b", {"q2"})
        self.nfa.add_transition("q0", None, {"q2"})  # Epsilon transition

    def test_add_state(self):
        """Test adding a state."""
        self.nfa.add_state("q3")
        self.assertIn("q3", self.nfa.states)

    def test_set_start_state(self):
        """Test setting the start state."""
        self.nfa.set_start_state("q1")
        self.assertEqual(self.nfa.start_state, "q1")
        with self.assertRaises(ValueError):
            self.nfa.set_start_state("q3")  # State not in NFA

    def test_add_accept_state(self):
        """Test adding an accept state."""
        self.nfa.add_accept_state("q1")
        self.assertIn("q1", self.nfa.accept_states)
        with self.assertRaises(ValueError):
            self.nfa.add_accept_state("q3")  # State not in NFA

    def test_add_transition(self):
        """Test adding transitions."""
        self.nfa.add_transition("q0", "b", {"q1"})
        self.assertIn("q1", self.nfa.transitions[("q0", "b")])
        with self.assertRaises(ValueError):
            self.nfa.add_transition("q3", "a", {"q1"})  # Invalid current state
        with self.assertRaises(ValueError):
            self.nfa.add_transition("q0", "c", {"q1"})  # Invalid symbol
        with self.assertRaises(ValueError):
            self.nfa.add_transition("q0", "a", {"q3"})  # Invalid next state

    def test_epsilon_closure(self):
        """Test epsilon closure computation."""
        closure = self.nfa.epsilon_closure({"q0"})
        self.assertEqual(closure, {"q0", "q2"})  # q0 has epsilon transition to q2

    def test_valid_string_simple(self):
        """Test a valid string with straightforward transitions."""
        self.assertTrue(self.nfa.validate_string("ab"))

    def test_valid_string_epsilon(self):
        """Test a valid string due to epsilon transitions."""
        self.assertTrue(self.nfa.validate_string(""))

    def test_invalid_string_short(self):
        """Test an invalid string that's too short."""
        self.assertTrue(self.nfa.validate_string("a"))

    def test_invalid_string_long(self):
        """Test an invalid string with extra symbols."""
        self.assertFalse(self.nfa.validate_string("abc"))

    def test_no_epsilon_transitions(self):
        """Test validation when the NFA has no epsilon transitions."""
        nfa_no_epsilon = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            start_state="q0",
            accept_states={"q2"}
        )
        nfa_no_epsilon.add_transition("q0", "a", {"q1"})
        nfa_no_epsilon.add_transition("q1", "b", {"q2"})
        self.assertTrue(nfa_no_epsilon.validate_string("ab"))
        self.assertFalse(nfa_no_epsilon.validate_string("a"))
        self.assertFalse(nfa_no_epsilon.validate_string(""))

    def test_multiple_paths(self):
        """Test validation with multiple non-deterministic paths."""
        nfa_multi_path = NFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b"},
            start_state="q0",
            accept_states={"q3"}
        )
        nfa_multi_path.add_transition("q0", "a", {"q1", "q2"})
        nfa_multi_path.add_transition("q1", "b", {"q3"})
        nfa_multi_path.add_transition("q2", "b", {"q3"})
        self.assertTrue(nfa_multi_path.validate_string("ab"))
        self.assertFalse(nfa_multi_path.validate_string("aa"))

    def test_cyclic_transitions(self):
        """Test validation with cyclic transitions."""
        nfa_cyclic = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            start_state="q0",
            accept_states={"q2"}
        )
        nfa_cyclic.add_transition("q0", "a", {"q1"})
        nfa_cyclic.add_transition("q1", "a", {"q0"})  # Cycle
        nfa_cyclic.add_transition("q1", "b", {"q2"})
        nfa_cyclic.print_transitions()
        self.assertTrue(nfa_cyclic.validate_string("abab"))
        self.assertFalse(nfa_cyclic.validate_string("aaa"))

    def test_unreachable_states(self):
        """Test validation when accept states are unreachable."""
        nfa_unreachable = NFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a"},
            start_state="q0",
            accept_states={"q3"}
        )
        nfa_unreachable.add_transition("q0", "a", {"q1"})
        nfa_unreachable.add_transition("q1", "a", {"q2"})  # q3 is unreachable
        self.assertFalse(nfa_unreachable.validate_string("aa"))

