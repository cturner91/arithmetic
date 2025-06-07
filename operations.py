# Codifying the arithmetic we're taught at primary school
# We only work with single-digit integer values but we can add / subtract / multiply / divide
# And logically work with the results.
# we work out what 123.456 + 7.89 is by converting and manipulating integers


def _validate_ints_below_10(*args) -> None:
    # The fundamental methods are only allowed to work with single-digit integers
    for i, value in enumerate(args):
        value = int(value)
        assert isinstance(value, int), f"Value #{i} ({value}) must be an integer"
        assert 0 <= value < 10, f"Value #{i} ({value}) must be less than 10"


# These are the fundamental operations we can perform

def _add_ints(v1: str | int, v2: str | int) -> int:
    int1, int2 = int(v1), int(v2)
    _validate_ints_below_10(int1, int2)
    return int1 + int2


def _subtract_ints(v1: str | int, v2: str | int) -> int:
    int1, int2 = int(v1), int(v2)
    _validate_ints_below_10(int1, int2)
    return int1 - int2


def _multiply_ints(v1: str | int, v2: str | int) -> int:
    int1, int2 = int(v1), int(v2)
    _validate_ints_below_10(int1, int2)
    return int1 * int2

# End fundamental operations


# Utility methods

def _pad_strings(v1: str, v2: str, is_decimal: bool) -> str:
    # helper function to align two strings of numbers in terms of place value
    length = max(len(v1), len(v2))
    if is_decimal:
        v1 = v1.ljust(length, '0')
        v2 = v2.ljust(length, '0')
    else:
        v1 = v1.rjust(length, '0')
        v2 = v2.rjust(length, '0')

    return v1, v2


def _format_int_and_decimal(integer: str, decimal: str) -> str:
    if decimal:
        return f"{integer}.{decimal}"
    else:
        return integer


def _align_numbers(v1: str, v2: str) -> tuple[str, str]:
    # helper function to align two strings of numbers in terms of place value
    integer1, decimal1 = _int_and_decimal(v1)
    integer2, decimal2 = _int_and_decimal(v2)

    integer1, integer2 = _pad_strings(integer1, integer2, False)
    decimal1, decimal2 = _pad_strings(decimal1, decimal2, True)

    v1 = _format_int_and_decimal(integer1, decimal1)
    v2 = _format_int_and_decimal(integer2, decimal2)
    assert len(v1) == len(v2), "Strings must be of equal length."
    return v1, v2


def _int_and_decimal(value: str) -> tuple[str, str]:
    # Helper function to split a string into integer and decimal parts
    if '.' in value:
        integer_part, decimal_part = value.split('.')
    else:
        integer_part, decimal_part = value, ''
    return integer_part, decimal_part


def _string_set(string: str, index: int, value: str | int) -> str:
    # Helper function to set a character in a string at a specific index
    assert len(str(value)) == 1, "Value must be a single character."
    return f'{string[:index]}{str(value)}{string[index + 1:]}'


def _is_zero(value: str) -> bool:
    for replace in ('.', '0', '-'):
        value = value.replace(replace, '')
    return len(value) == 0


def _equivalent_division(number1: str, number2: str) -> tuple[str]:
    # 1 / 0.23 === 100 / 23
    # but diviing by an integer is so much easier
    if '.' in number2:
        integer2, decimal2 = number2.split('.')

        if '.' in number1:
            integer1, decimal1 = number1.split('.')
            max_decimals = max(len(decimal1), len(decimal2))
            number1 = f"{integer1}{decimal1.ljust(max_decimals, '0')}"
            number2 = f"{integer2}{decimal2.ljust(max_decimals, '0')}"
        else:
            # number1 does not have a decimal => pad with zeroes
            number1 = f'{number1}{"0" * len(decimal2)}'
            number2 = number2.replace('.', '')

    return number1, number2


def _clean_number(number: str) -> str:
    if _is_zero(number):
        return '0'

    number = number.lstrip('0')
    if '.' in number:
        # only strip trailing zeroes after the decimal point
        # otherwise, the 0 is an integral part of place-value
        number = number.rstrip('0')

    if number.startswith('.'):
        number = '0' + number
    if number.endswith('.'):
        number = number[:-1]
    return number


def _lte(number1: str, number2: str) -> bool:
    # use string comparison for number1 <= number2
    number1 = _clean_number(number1)
    number2 = _clean_number(number2)

    if number1 == number2:
        return True
    
    if number1.startswith('-') and number2.startswith('-'):
        # both numbers are negative, so we can compare them as if they were positive
        return not _lte(number1[1:], number2[1:])
    elif number1.startswith('-') and not number2.startswith('-'):
        return True
    elif not number1.startswith('-') and number2.startswith('-'):
        return False

    if len(number1) < len(number2):
        return True
    elif len(number1) > len(number2):
        return False
    else:
        # same length - compare each char
        for char1, char2 in zip(number1, number2):
            if char1 < char2:
                return True
            elif char1 > char2:
                return False
            else:
                # maybe unnecessary to have this block, but it makes the logic clear
                continue
    
    # if we get here, something has gone wrong
    raise ValueError(f"Cannot compare {number1} and {number2} for less than or equal to (<=)")


# Begin public methods

def add(
    number1: str, 
    number2: str, 
) -> str:
    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):
        # add the absolute values and negate the result
        return f'-{add(number1[1:], number2[1:])}'
    
    elif number1.startswith('-'):  # -4 + 2 => 2 - 4
        return subtract(number2, number1[1:])

    elif number2.startswith('-'):  # -4 + 2 => 2 - 4
        return subtract(number1, number2[1:])

    # neither input is negative

    v1, v2 = _align_numbers(number1, number2)

    # This just applies add_int inside a loop and carries the 1 if necessary
    carry = 0
    output = ''
    for i in range(len(v1) - 1, -1, -1):
        if v1[i] == '.':
            output = '.' + output
            continue

        int1 = int(v1[i])
        int2 = int(v2[i])
        result = _add_ints(int1, int2)
        if carry:  # can only ever be 1 or 0?
            result += carry

        if result >= 10:
            carry = 1
            result -= 10
        else:
            carry = 0
        
        # pre-pend, not append, to the output
        output = str(result) + output
        
    if carry:
        return f'1{output}'
    return output


def subtract(
    number1: str, 
    number2: str, 
) -> str:
    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):            
        result = subtract(number1[1:], number2[1:])
        if result.startswith('-'):
            # if we subtract a bigger negative from a smaller negative, we get a positive result
            return result[1:]
        return f'-{result}'

    elif number1.startswith('-'):  # -4 - 2 => -(4 + 2)
        return f'-{add(number1[1:], number2)}'
    elif number2.startswith('-'): # 4 - -2 => 4 + 2
        return add(number1, number2[1:])

    # neither input is negative

    v1, v2 = _align_numbers(number1, number2)

    # both numbers are aligned - easy to see which is bigger. String sorting even makes this possible
    negative = None
    for int1, int2 in zip(v1, v2):
        if int1 == int2:
            continue
        elif int1 > int2:
            negative = False
        else:
            negative = True
        break
    
    # numbers are identical
    if negative is None:
        return '0'
    elif negative:
        # swap the numbers so we can do the subtraction
        v1, v2 = v2, v1

    output = ''
    for i in range(len(v1)-1, -1, -1):
        if v1[i] == '.':
            output = '.' + output
            continue

        int1 = int(v1[i])
        int2 = int(v2[i])
        result = _subtract_ints(int1, int2)
        if result < 0:
            # we need to borrow from higher value places
            # we know a higher value place exists because the values aren't equal 
            # and we know v1 > v2
            for j in range(i-1, -1, -1):
                if v1[j] == '.':
                    continue
                elif v1[j] == '0':
                    v1 = _string_set(v1, j, 9)
                else:
                    v1 = _string_set(v1, j, int(v1[j]) - 1)
                    result += 10  # 3 - 6 = -3, but 13 - 6 = 7 => result += 10
                    break
        
        # pre-pend, not append, to the output
        output = str(result) + output
        
    # strip any leading / trailing zeros?
    output = _clean_number(output)
    if negative:
        output = '-' + output
    return output


def multiply(
    number1: str, 
    number2: str, 
) -> str:
    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):            
        return multiply(number1[1:], number2[1:])
    elif number1.startswith('-'):
        return f'-{multiply(number1[1:], number2)}'
    elif number2.startswith('-'):
        return f'-{multiply(number1, number2[1:])}'

    # neither input is negative

    # save ourselves some CPU cycles
    if _is_zero(number1) or _is_zero(number2):
        return '0'

    v1, v2 = _align_numbers(number1, number2)

    # count all decimal places, then perform total integer multiplication, and re-add the 
    # decimal place later
    decimal_places = 0
    if '.' in v1:
        i, d = v1.split('.')
        decimal_places += len(d)
        v1 = v1.replace('.', '')
    if '.' in v2:
        i, d = v2.split('.')
        decimal_places += len(d)
        v2 = v2.replace('.', '')

    numbers = []  # as we multiply, we end up with a bunch of numbers to be added together
    # start at right-most value of v2, multiply by each digit of v1
    padding = 0
    for i in range(len(v2)-1, -1, -1):
        int2 = int(v2[i])

        # when multiplying, need to pad the right-hand side with zeros 
        # i.e. we are multiplying by 30, not 3 -> pad the right
        output = '0' * padding
        carry = 0
        for j in range(len(v1)-1, -1, -1):
            int1 = int(v1[j])
            result = _multiply_ints(int1, int2)
            result = add(str(result), str(carry))

            if len(result) > 1:
                # can only be max 2-digits. Even if we are multiplying 9999 * 9999, then max of
                # and operation will be 81 + 8 => 89 i.e. still 2 digits
                carry = int(result[0])
                result = result[1]
            else:
                carry = 0
        
            # pre-pend, not append, to the output
            output = str(result) + output
        
        # inner loop has finished - add to numbers and perform next loop
        if carry:
            output = str(carry) + output
        
        numbers.append(output)
        padding += 1

    # All numbers have now been created -> sum them all up
    total = '0'
    for number in numbers:
        total = add(total, number)

    # re-add the decimal place
    if decimal_places > 0:
        integer = total[:-decimal_places]
        decimal = total[-decimal_places:]
        total = f'{integer}.{decimal}'

    total = _clean_number(total)
    return total
    

def divide(
    number1: str, 
    number2: str, 
    max_decimals: int = 10,
) -> str:
    if _is_zero(number2):
        raise ZeroDivisionError()

    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):            
        return divide(number1[1:], number2[1:])
    elif number1.startswith('-'):
        return f'-{divide(number1[1:], number2)}'
    elif number2.startswith('-'):
        return f'-{divide(number1, number2[1:])}'

    # neither input is negative

    # save ourselves some CPU cycles
    if _is_zero(number1):
        return '0'
    
    v1, v2 = _equivalent_division(number1, number2)
    if '.' not in v1:
        v1 = f'{v1}.0'  # ensure we always have a decimal so no special case handling

    # I always used to do multiplication 1-9 of the divisor, and then just look up the biggest 
    # one that fits...
    lookup = {i: multiply(v2, str(i)) for i in range(0, 10)}

    output = ''
    value = ''
    decimal = False
    n_decimals = 0
    i = 0
    while True:
        # Can't think of the requisite logic for a single conditional
        # we msut run until at least len(v1), and if we have a remainder at that point, we keep 
        # going until we exceed max_decimals
        if i >= len(v1) and n_decimals >= max_decimals:
            break

        if i < len(v1):
            if v1[i] == '.':
                output += '.'
                decimal = True
                i += 1
                continue

            value = f'{value}{v1[i]}'
        else:
            value = f'{value}0'

        # lookup goes down to 0 - so something will always fit
        for j in range(9, -1, -1):
            multiple = lookup[j]
            if _lte(multiple, value):
                output += str(j)
                value = subtract(value, multiple)
                if decimal:
                    n_decimals += 1
                break

        # we have finished iterating over the number and we have no remainder -> finshed!
        if i >= len(v1) and value == '0':
            break
        
        i += 1

    output = _clean_number(output)
    return output
