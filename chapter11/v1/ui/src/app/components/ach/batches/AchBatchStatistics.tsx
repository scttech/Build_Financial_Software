import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import {AchBatchEntriesResponse} from "@/app/fileDetails/[fileId]/batchDetails/[batchId]/page";
import Decimal from "decimal.js";
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Paper from "@mui/material/Paper";
import Title from "@/app/components/Title";

interface AchBatchStatisticsProps {
    entries: AchBatchEntriesResponse[];
}

interface BatchStatistics {
    count: number;
    amount: Decimal;
}

interface BatchTotals {
    debit: Decimal;
    credit: Decimal;
    other: Decimal;
}

export function computeBatchTotals(entries: AchBatchEntriesResponse[]): BatchTotals {
    const totals: BatchTotals = {
        debit: new Decimal(0),
        credit: new Decimal(0),
        other: new Decimal(0)
    };
    entries.forEach(entry => {
        const cleanAmount = entry.amount.replace(/[$,]/g, '');
        const amount = new Decimal(cleanAmount);
        if (entry.transaction_code === 27) {
            totals.debit = totals.debit.plus(amount);
        } else if (entry.transaction_code === 22) {
            totals.credit = totals.credit.plus(amount);
        } else {
            totals.other = totals.other.plus(amount);
        }
    });
    return totals;

}

function computeBatchStatistics(entries: AchBatchEntriesResponse[]): Map<string, BatchStatistics> {
    const countMap = new Map<string, BatchStatistics>();
    entries.forEach(entry => {
        const cleanAmount = entry.amount.replace(/[$,]/g, '');
        const stats = countMap.get(entry.transaction_description) || { count: 0, amount: new Decimal(0) };
        stats.count += 1;
        stats.amount = stats.amount.plus(cleanAmount);
        countMap.set(entry.transaction_description, stats);
    });
    return countMap;
}

function createListItems(entries: Map<string, BatchStatistics>): React.ReactNode[] {
    const listItems: React.ReactNode[] = [];
    entries.forEach((entry: BatchStatistics, key: string) => {
        const listItem = (<ListItem key={key}>
            <ListItemText primary={key} secondary={`Count: ${entry.count} Amount: ${formatCurrency(entry.amount)}`} />
        </ListItem>);
        listItems.push(listItem);
    });
    return listItems;
}
export default function AchBatchStatistics({entries}: Readonly<AchBatchStatisticsProps>) {

    const computedBatchStatistics = computeBatchStatistics(entries);
    const computedBatchTotals = computeBatchTotals(entries);
    const listItems = createListItems(computedBatchStatistics);

    return (
        <Paper>
                <Title>Batch Statistics</Title>
                <List dense={true}>
                    <ListItem key="creditTotal">
                        <ListItemText primary="Credit Total" secondary={`${formatCurrency(computedBatchTotals.credit)}`} />
                    </ListItem>
                    <ListItem key="debitsTotal">
                        <ListItemText primary="Debit Total" secondary={`${formatCurrency(computedBatchTotals.debit)}`} />
                    </ListItem>
                    <ListItem key="otherTotal">
                        <ListItemText primary="Other Total" secondary={`${formatCurrency(computedBatchTotals.other)}`} />
                    </ListItem>
                    {listItems}
                </List>
            </Paper>
    );
}