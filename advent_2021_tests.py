import unittest

import advent_2021 as code


class AdventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        cls.example_dive = "forward 5, down 5, forward 8, up 3, down 8, forward 2"
        cls.example_diag = ["00100", "11110", "10110", "10111", "10101", "01111",
                            "00111", "11100", "10000", "11001", "00010", "01010"]

    def test_one(self):
        self.assertEqual(7, code.sonar_sweep(self.example_input))

    def test_two(self):
        self.assertEqual(5, code.sonar_sweep_window(3, self.example_input))

    def test_three(self):
        self.assertEqual(150, code.steer(self.example_dive.split(',')))

    def test_four(self):
        self.assertEqual(900, code.steer_aim(self.example_dive.split(',')))

    def test_five(self):
        self.assertEqual(198, code.determine_power_consumption(self.example_diag))

    def test_six(self):
        self.assertEqual(230, code.get_life_support_rating(self.example_diag))


class AnswerTest(unittest.TestCase):
    def setUp(self) -> None:
        with open("advent_input.txt") as fin:
            self.inputs = fin.read().split("\n")[:-1]
    
    def test_output(self):
        self.assertEqual(123, code.get_life_support_rating(self.inputs))
