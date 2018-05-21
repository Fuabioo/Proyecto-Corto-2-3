"""
Main execution module
"""

from argparse import ArgumentParser

from genetic import Genetic
from a_star import AStar


def get_args():
    """
    Processes the arguments, returning them
    """
    parser = ArgumentParser(
        description="Proyecto Corto 2 y 3 - Buscador de Zanahorias")

    parser.add_argument(
        '--tablero-inicial',
        type=str,
        required=False,  # True,
        help="Archivo de entrada")

    parser.add_argument('--a-estrella', action='store_true')
    parser.add_argument('--vision', default='2', type=int)
    parser.add_argument('--zanahorias', default='10', type=int)

    parser.add_argument('--genetico', action='store_true')
    parser.add_argument('--derecha', action='store_true')
    parser.add_argument('--izquierda', action='store_true')
    parser.add_argument('--abajo', action='store_true')
    parser.add_argument('--arriba', action='store_true')
    parser.add_argument('--individuos', default='3', type=int)
    parser.add_argument('--generaciones', default='1000', type=int)

    parser.add_argument('--taza-mutacion', default='0.5', type=float)
    parser.add_argument('--politica', default='gen', type=str)

    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--show-graphic', action='store_true')
    parser.add_argument(
        '--guardar-archivos',
        action='store_true',
        default=True)

    args = parser.parse_args()
    return args


def get_result(algorithm="AStar", args=None):
    """ Factory method: gets the algorithm class """
    algorithms = dict(AStar=AStar, Genetic=Genetic)
    return algorithms[algorithm](args=args)


def main():
    """ Main execution """
    args = get_args()
    # testing args astar
    args.a_estrella = True
    args.vision = 10
    args.zanahorias = 10
    args.tablero_inicial = "25x25(18).txt"
    # args.tablero_inicial = "4x4(2).txt"

    # testing args genetis
    # args.genetico = True
    # args.derecha = True
    # args.individuos = 20
    # args.generaciones = 10
    # args.vision = 4
    # args.zanahorias = 2
    # args.tablero_inicial = "4x4(2).txt"
    # args.show_graphic = True

    result = get_result(algorithm="AStar", args=args)
    # result = get_result(algorithm="Genetic", args=args)
    # print(result)
    result.run()
    return result


if __name__ == '__main__':
    main()
