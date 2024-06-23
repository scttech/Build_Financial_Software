import Decimal from "decimal.js";

function convertToNumber(value: any): number {
    if (typeof value === 'number') {
        return value;
    }

    if (typeof value === 'string') {
        return parseFloat(value);
    }

    return value.toNumber();
}
export function formatCurrency(value: number | Decimal, currency: string = "USD", locale: string = 'en-US'): string {

    const decimalValue = convertToNumber(value);

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(decimalValue);
}