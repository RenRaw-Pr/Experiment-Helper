import re

def validate_command(value: str) -> bool:
    if value=='Value' or value=='Error': return True
    if value.count(',')+value.count('.')<=1:
        value = value.replace(' ', '').replace(',', '.')
        if value in ['', ' ', '.', ',', '-', '+']: return True
        if re.compile("[-+]?(?:\d*(?:\.\d*)?|\.\d*)(?:[eE](?:[-+]?(?:\d+)?)?)?").fullmatch(value): return True
        if re.compile("[-+]?(?:\d*(?:\.\d*)?|\.\d*)(?:\*(?:1(?:0(?:[\^](?:[-+]?(?:\d+)?)?)?)?)?)?").fullmatch(value): return True
        if re.compile("[-+]?(?:\d*(?:\.\d*)?|\.\d*)(?:\*(?:1(?:0(?:\*(?:\*(?:[-+]?(?:\d+)?)?)?)?)?)?)?").fullmatch(value): return True  
    return False

def convert_from_entry(value: str) -> float:
    value = value.replace(' ', '').replace('E', 'e')
    if re.compile("[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?").fullmatch(value):
        return float(value)
    if re.compile("[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:\*10\^[-+]?\d+)?").fullmatch(value):
        return float(value.split('*')[0])*10**int(value.split('^')[-1])
    if re.compile("[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:\*10\*{2}[-+]?\d+)?").fullmatch(value):
        return float(value.split('*')[0])*10**int(value.split('**')[-1])
    else: return 0