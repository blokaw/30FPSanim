#
# (!) AI SLOP (!)                                           #
# VIBE CODED IT BECAUSE WHY                                 #
# WOULD I WASTE ALL MY OF TIME                              #
# DEBUGGING SOME PARSER THAT                                #
# CAN BE DONE IN FEW MINUTES                                #
# ========================================================  #
# SHORT DOC                                                 #
# parseKeyframes(text: str) -> JSON: kf string to JSON     #
# buildKeyframes(data: JSON) -> str: kf JSON to string  #
# ========================================================  #
#                                                           #

__all__ = ["parseKeyframes", "buildKeyframes"]

import re
from collections import OrderedDict


def parseKeyframes(text):
    """
    Парсит кейфреймы из текста и возвращает структуру данных.
    """
    result = OrderedDict()
    
    # Удаляем комментарии
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    
    # Находим все блоки @keyframes с правильным подсчетом скобок
    pattern = r'@keyframes\s+(\w[\w-]*)\s*'
    
    pos = 0
    while pos < len(text):
        match = re.search(pattern, text[pos:])
        if not match:
            break
            
        anim_name = match.group(1)
        start_pos = pos + match.end()
        
        # Ищем открывающую скобку
        brace_start = text.find('{', start_pos)
        if brace_start == -1:
            break
            
        # Считаем вложенные скобки
        brace_count = 1
        i = brace_start + 1
        while i < len(text) and brace_count > 0:
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
            i += 1
        
        if brace_count != 0:
            break
            
        anim_body = text[brace_start + 1:i - 1]
        pos = i
        
        if anim_name not in result:
            result[anim_name] = OrderedDict()
        
        # Парсим процентные блоки внутри тела анимации
        parse_animation_body(anim_body, result[anim_name])
    
    return result


def parse_animation_body(body, anim_dict):
    """
    Парсит тело анимации, извлекая процентные блоки.
    """
    # Ищем блоки с процентами
    percent_pattern = r'(\d+(?:\.\d+)?%)\s*'
    
    pos = 0
    while pos < len(body):
        match = re.search(percent_pattern, body[pos:])
        if not match:
            break
            
        percent_str = match.group(1)
        percent_value = float(percent_str.rstrip('%'))
        start_pos = pos + match.end()
        
        # Ищем открывающую скобку
        brace_start = body.find('{', start_pos)
        if brace_start == -1:
            break
            
        # Считаем вложенные скобки для этого блока
        brace_count = 1
        i = brace_start + 1
        while i < len(body) and brace_count > 0:
            if body[i] == '{':
                brace_count += 1
            elif body[i] == '}':
                brace_count -= 1
            i += 1
        
        if brace_count != 0:
            break
            
        properties_block = body[brace_start + 1:i - 1]
        pos = i
        
        if percent_value not in anim_dict:
            anim_dict[percent_value] = OrderedDict()
        
        # Парсим свойства
        parse_properties(properties_block, anim_dict[percent_value])


def parse_properties(block, props_dict):
    """
    Парсит свойства из блока.
    """
    # Удаляем пустые строки и разбиваем на строки
    lines = [line.strip() for line in block.split('\n') if line.strip()]
    
    for line in lines:
        # Ищем свойство: значение;
        prop_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.+);?\s*$', line)
        if prop_match:
            prop_name = prop_match.group(1)
            prop_value = prop_match.group(2).rstrip(';').strip()
            
            numbers, mask = extract_numbers_and_mask(prop_value)
            props_dict[prop_name] = {
                "value": numbers,
                "mask": mask
            }


def extract_numbers_and_mask(value_str):
    """
    Извлекает все числа из строки значения и создает маску.
    """
    numbers = []
    
    def replace_number(match):
        num_str = match.group(0)
        num = float(num_str) if '.' in num_str else int(num_str)
        numbers.append(num)
        return '%s'
    
    number_pattern = r'-?\d+\.?\d*'
    mask = re.sub(number_pattern, replace_number, value_str)
    mask = ' '.join(mask.split())
    
    return [float(n) for n in numbers], mask


def buildKeyframes(data):
    """
    Генерирует текст кейфреймов из структуры данных.
    """
    result = []
    
    for anim_name, percentages in data.items():
        result.append(f'@keyframes {anim_name}')
        result.append('{')
        
        for percent, properties in percentages.items():
            if percent == int(percent):
                percent_str = f'{int(percent)}%'
            else:
                percent_str = f'{percent}%'
            
            result.append(f'    {percent_str}')
            result.append('    {')
            
            for prop_name, prop_data in properties.items():
                value = apply_mask(prop_data['value'], prop_data['mask'])
                result.append(f'        {prop_name}: {value};')
            
            result.append('    }')
        
        result.append('}')
    
    return '\n'.join(result)


def apply_mask(values, mask):
    """
    Применяет маску к значениям.
    """
    str_values = []
    for v in values:
        if isinstance(v, float) and v == int(v):
            str_values.append(str(int(v)))
        else:
            str_values.append(str(v))
    
    result = mask
    for value in str_values:
        result = result.replace('%s', value, 1)
    
    return result


# Тестируем
if __name__ == "__main__":
    input_text = '''@keyframes anim
{
    0%
    {
        opacity: 0.0;
        position: 0px 58px 0px;
    }
    8%
    {
        opacity: 1.0;
        position: 0px 58px 0px;
    }
    90%
    {
        opacity: 1.0;
        position: 0px 58px 0px;
        transform: scale3d(1, 1, 1);
    }
    100%
    {
        opacity: 0.0;
        position: 0px 16px 0px;
        transform: scale3d(2, 2, 1);
    }
}'''
    
    import json
    
    parsed = parseKeyframes(input_text)
    print("Результат парсинга:")
    print(json.dumps(parsed, indent=4, ensure_ascii=False))
    
    print("\nОбратная генерация:")
    generated = buildKeyframes(parsed)
    print(generated)