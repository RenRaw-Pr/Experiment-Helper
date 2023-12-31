from sympy import symbols, diff, lambdify, parse_expr
from math import log10,floor
from typing import Union, List, Dict

def transform_data(FUNCTION: str,
                   INCOMING_DATA: Dict[str, List[Union[int, float]]]) -> Union[int, float]:
    
    for elem in INCOMING_DATA.keys():
        exec(f"{elem} = symbols('{elem}')")
    
    for elem in INCOMING_DATA.keys():
        DIFFERENCIAL = diff(FUNCTION, elem)
        RES = lambdify([key for key in INCOMING_DATA.keys()], DIFFERENCIAL)
        exec(f"INCOMING_DATA[elem].append(RES{tuple([float(INCOMING_DATA[key][0]['Scientific']) for key in INCOMING_DATA.keys()])})")

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
        INCOMING_DATA[key].append(str(round((INCOMING_DATA[key][3]/summ_error)*100,2))+'%')

    return summ_error**0.5, INCOMING_DATA

def round_by_error(value: Union[int, float],
                   error: Union[int, float]) -> Union[int, float]:
    first_meaning=0
    value = float(value)
    error = float(error)
    for i, elem in enumerate(str(error)):
        if elem!='0' and elem!='.':
            if elem=='1' or elem=='2':
                first_meaning=i+2
                break
            else: 
                first_meaning=i+1
                break
    if error-int(error)!=0 and int(error)==0:
        first_meaning-=2
    if int(error)!=0:
        first_meaning-=len(str(int(error)))
    return round(value, first_meaning), round(error, first_meaning)

def round_by_meaning(value: Union[int, float]) -> Union[int, float]:
    value = float(value)
    first_meaning=0
    for i, elem in enumerate(str(value)):
        if elem!='0' and elem!='.':
            if elem=='1' or elem=='2':
                first_meaning=i+2
                break
            else: 
                first_meaning=i+1
                break
    if value-int(value)!=0 and int(value)==0:
        first_meaning-=2
    if int(value)!=0:
        first_meaning-=len(str(int(value)))
    return round(value, first_meaning)

def adjusted_scientific_notation(val: float, round_to: int=3) -> Dict[str, str]:
    try: order = floor(log10(abs(val)))
    except ValueError: return {"Scientific": 0.0, "Classical": 0.0}
    nearest = round_to*(order//round_to+int(order%round_to==round_to-1))
    val = str(float("{:.4f}".format(val*10**(-nearest))))
    exp = "+-"[nearest<0] + str(abs(nearest))

    if exp==('+0' or '-0'): return {"Scientific": val, "Classical": val}
    else: return {"Scientific" : val+"e"+exp, "Classical" : val+'*10^'+exp}
