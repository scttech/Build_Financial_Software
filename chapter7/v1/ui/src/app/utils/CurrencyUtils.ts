import Decimal from "decimal.js";

export function formatCurrency(value: number | Decimal, currency: string = "USD", locale: string = 'en-US'): string {

    const decimalValue = typeof value === 'number' ? value : value.toNumber();

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(decimalValue);
}