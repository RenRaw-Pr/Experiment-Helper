from sympy import *

# Формат хранения данных: '_название_переменной_в_уравнении_' : [_значение_переменной_ , _погрешность_]
INCOMING_DATA = {
    'x' : [10, 0.5],
    'y' : [20, 0.2]
}

# Преобразование всех заданных переменных в символы выражения (для дальнейшего использования)
for elem in INCOMING_DATA.keys():
    exec(f"{elem} = symbols('{elem}')")

FUNCTION = "y**2+x**2"

for elem in INCOMING_DATA.keys():
    DIFFERENCIAL = diff(FUNCTION, elem)
    RES = lambdify([key for key in INCOMING_DATA.keys()], DIFFERENCIAL)
    exec(f"print(RES{tuple([INCOMING_DATA[key][0] for key in INCOMING_DATA.keys()])})")
    


# latex(diff(FUNCTION, elem))