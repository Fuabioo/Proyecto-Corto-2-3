"""
Testing module
"""
import pytest
import tec.ic.ia.pc2.g08 as g08


def get_two_carrot_input():
    """
    Obtains pre-defined testing base genetic that is assured not to fail
    """
    args = g08.get_args()
    args.genetico = True
    args.derecha = True
    args.individuos = 3
    args.generaciones = 1000
    args.vision = 4
    args.zanahorias = 2
    args.tablero_inicial = "_generated_inputs_/4x4(2).txt"
    result = g08.get_result(algorithm="Genetic", args=args)
    return result


def get_one_carrot_input():
    """
    Obtains pre-defined testing base genetic that is assured not to fail
    """
    args = g08.get_args()
    args.genetico = True
    args.derecha = True
    args.individuos = 3
    args.generaciones = 1000
    args.vision = 4
    args.zanahorias = 2
    args.tablero_inicial = "_generated_inputs_/4x4(1).txt"
    result = g08.get_result(algorithm="Genetic", args=args)
    return result


class TestCompletness(object):
    """ Test object for proof that the algorithm actually CAN finish """

    def test_completeness_one(self):
        """
        Two present carrots and bunny needs two carrots
        """
        result = get_two_carrot_input()
        print(result.run())
        assert result.args.zanahorias == 0

    def test_completeness_two(self):
        """
        One present carrots but bunny needs two
        """
        result = get_one_carrot_input()
        result.run()
        assert result.args.zanahorias > 0
