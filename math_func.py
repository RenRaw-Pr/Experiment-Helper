from sympy import symbols, diff, lambdify, parse_expr
from typing import Union, List, Dict

def transform_data(FUNCTION: str,
                   INCOMING_DATA: Dict[str, List[Union[int, float]]]) -> Union[int, float]:
    
    for elem in INCOMING_DATA.keys():
        exec(f"{elem} = symbols('{elem}')")
    
    for elem in INCOMING_DATA.keys():
        DIFFERENCIAL = diff(FUNCTION, elem)
        RES = lambdify([key for key in INCOMING_DATA.keys()], DIFFERENCIAL)
        exec(f"INCOMING_DATA[elem].append(RES{tuple([INCOMING_DATA[key][0] for key in INCOMING_DATA.keys()])})")

    RES = lambdify([key for key in INCOMING_DATA.keys()], parse_expr(FUNCTION, transformations="all"))
    result = []
    exec(f"result.append(RES{tuple([INCOMING_DATA[key][0] for key in INCOMING_DATA.keys()])})")
    return result[0], INCOMING_DATA

def count_summ_error(INCOMING_DATA: Dict[str, List[Union[int, float]]]) -> Union[int, float]:
    summ_error = 0
    for key in INCOMING_DATA.keys():
        error = (INCOMING_DATA[key][1]*INCOMING_DATA[key][2])**2
        INCOMING_DATA[key].append(error)
        summ_error+=error

    for key in INCOMING_DATA.keys():
        INCOMING_DATA[key].append(str(round((INCOMING_DATA[key][3]/summ_error)*100,2))+'%')

    return summ_error**0.5, INCOMING_DATA