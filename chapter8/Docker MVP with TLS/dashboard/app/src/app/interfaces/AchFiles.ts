import Decimal from "decimal.js";

export interface AchFiles {
    id: string;
    date: string;
    filename: string;
    originator: string;
    creditTotal: Decimal;
    debitTotal: Decimal;
}