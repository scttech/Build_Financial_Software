import {describe, it} from "@jest/globals";
import expect from "expect";
import {formatCurrency} from "@/app/utils/CurrencyUtils";

describe('Formatting Currency', () => {
    it('Has trailing zeros', () => {
        const result = formatCurrency(1.0)

        expect(result).toBe('$1.00')
    })

    it('Default currency is USD', () => {
        const result = formatCurrency(1.0)

        expect(result).toBe('$1.00')
    })

    it('Has comma separator', () => {
        const result = formatCurrency(1000.0)

        expect(result).toBe('$1,000.00')
    })

    it('Has comma separators for large numbers', () => {
        const result = formatCurrency(1000000.0)

        expect(result).toBe('$1,000,000.00')
    })

    it('German formatting', () => {
        const result = formatCurrency(1000000.0, 'EUR', 'de-DE')

        expect(result).toBe('1.000.000,00\u00A0€')
    })
})