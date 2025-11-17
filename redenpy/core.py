from decimal import Decimal, ROUND_HALF_UP

class RedenPy:
    
    def __init__(self, digit, rule):
        """
        A class to do redenomination of a currency.

        Parameters:
        digit (int): The number of digits that wants to be removed from the back
        rule (json): The rule for the redenomination, round up, round down, etc. Check the docs for details
        """
        self.rule = rule
        self.digit = digit

    def redenomination(self, money, fractional=False, cur_symbol='begin', output_type=str):
        """
        Convert money according to redenomination rules.

        Args:
            money (str | int | float | Decimal): The amount to convert
            fractional (bool): Whether to include fractional part
            cur_symbol (str): 'begin' or 'end', position of currency symbol
            output_type (type): Type to return: str, Decimal, float, int
        Returns:
            str | Decimal | float | int: The redenominated value in the requested type
        """
        # Convert string to Decimal if needed
        if isinstance(money, str):
            try:
                money = Decimal(money.replace(',', '').replace(' ', ''))
            except Exception:
                raise ValueError("Invalid money string")
        else:
            money = Decimal(money)

        # Apply redenomination: remove digits from back
        factor = Decimal(10) ** self.digit
        money = (money / factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Separate whole and fractional parts
        whole = int(money)
        frac = int((money - whole) * 100)

        # Currency symbol (example)
        symbol = "CUR"

        # Format output as string
        result_str = None
        match (fractional, cur_symbol, isinstance(money, Decimal)):
            case False, 'begin', True:
                result_str = f"{symbol}{whole}"
            case False, 'end', True:
                result_str = f"{whole}{symbol}"
            case True, 'begin', True:
                result_str = f"{symbol}{whole},{frac:02d}"
            case True, 'end', True:
                result_str = f"{whole},{frac:02d}{symbol}"
            case False, _, False:
                result_str = f"{whole}"
            case True, _, False:
                result_str = f"{whole},{frac:02d}"

        # Convert result to requested type
        if output_type == str:
            return result_str
        elif output_type == Decimal:
            return money
        elif output_type == float:
            return float(money)
        elif output_type == int:
            return int(money)
        else:
            raise ValueError("Unsupported output_type. Use str, Decimal, float, or int.")
