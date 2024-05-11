import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';
import {AchFiles} from "@/app/interfaces/AchFiles";
import {formatCurrency} from "@/app/utils/CurrencyUtils";

interface TodaysAchTotalsProps {
    files: AchFiles[];
}
export default function TodaysAchTotals({files}: Readonly<TodaysAchTotalsProps>) {

    let creditTotal = 0;
    let debitTotal = 0;
    files.forEach(file => {
        creditTotal += file.creditTotal.toNumber();
        debitTotal += file.debitTotal.toNumber();
    });

    return (
        <React.Fragment>
            <Title>Todays Totals</Title>
            <Typography component="p" variant="h4">
                Credits:
            </Typography>
            <Typography component="p" variant="h6">
                {formatCurrency(creditTotal)}
            </Typography>
            <Typography component="p" variant="h4">
                Debits:
            </Typography>
            <Typography component="p" variant="h6">
                {formatCurrency(debitTotal)}
            </Typography>
        </React.Fragment>
    );
}