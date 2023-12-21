from sympy import symbols, diff, lambdify, parse_expr
from math import log10,floor
from typing import Union, List, Dict

def transform_data(FUNCTION: str,
                   INCOMING_DATA: Dict[str, List[Union[int, float]]]) -> Union[int, float]:
    
    for elem in INCOMING_DATA.keys():
        exec(f"{elem} = symbols('{elem}')")
    
    for elem in INCOMING_DATA.keys():
        if float(INCOMING_DATA[elem][1]['Scientific'])!=0:
            DIFFERENCIAL = diff(FUNCTION, elem)
            RES = lambdify([key for key in INCOMING_DATA.keys()], DIFFERENCIAL)
            exec(f"INCOMING_DATA[elem].append(RES{tuple([float(INCOMING_DATA[key][0]['Scientific']) for key in INCOMING_DATA.keys()])})")
        else: INCOMING_DATA[elem].append(0)
        
    RES = lambdify([key for key in INCOMING_DATA.keys()], parse_expr(FUNCTION, transformations="all"))
    result = []
    exec(f"result.append(RES{tuple([float(INCOMING_DATA[key][0]['Scientific']) for key in INCOMING_DATA.keys()])})")
    return result[0], INCOMING_DATA

def count_summ_error(INCOMING_DATA: Dict[str, List[Union[int, float]]]) -> Union[int, float]:
    summ_error = 0
    for key in INCOMING_DATA.keys():
        error = (float(INCOMING_DATA[key][1]['Scientific'])*INCOMING_DATA[key][2])**2
        INCOMING_DATA[key].append(error)
        summ_error+=error

    for key in INCOMING_DATA.keys():
        try: INCOMING_DATA[key].append(str(round((INCOMING_DATA[key][3]/summ_error)*100,2))+'%')
        except ZeroDivisionError: INCOMING_DATA[key].append("0.00%")

    return summ_error**0.5, INCOMING_DATA

def adjusted_scientific_notation(val: float, round_to: int=3) -> Dict[str, str]:
    try: order = floor(log10(abs(val)))
    except ValueError: return {"Scientific": 0.0, "Classical": 0.0}
    nearest = round_to*(order//round_to+int(order%round_to==round_to-1))
    val = str("{:.4f}".format(float(val*10**(-nearest))))
    exp = "+-"[nearest<0] + str(abs(nearest))

    if exp==('+0' or '-0'): return {"Scientific": val, "Classical": val}
    else: return {"Scientific" : val+"e"+exp, "Classical" : val+'*10^'+exp}
