import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import {formatCurrency} from "@/app/utils/CurrencyUtils";

// Generate Order Data
function createData(
    id: number,
    date: string,
    name: string,
    creditAmount: number,
    debitAmount: number,
) {
    return { id, date, name, creditAmount, debitAmount };
}

const rows = [
    createData(
        0,
        '03/20/2023',
        'sample.ach',
        312.40,
        100.20
    ),
    createData(
        1,
        '03/20/2023',
        'sample1.ach',
        1866.90,
        1234.10
    ),
    createData(2,
        '03/20/2023',
        'bad.ach',
        100.81,
        500.50
    ),
    createData(
        3,
        '03/20/2023',
        'sample2.ach',
        654.39,
        400.00
    ),
    createData(
        4,
        '03/20/2023',
        'sample3.ach',
        212.79,
        140.95
    ),
];

function preventDefault(event: React.MouseEvent) {
    event.preventDefault();
}

export default function RecentAchUploads() {
    return (
        <>
            <Title>Recent ACH Uploads</Title>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Filename</TableCell>
                        <TableCell align="right">Credit Total</TableCell>
                        <TableCell align="right">Debit Total</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TableRow key={row.id}>
                            <TableCell>{row.date}</TableCell>
                            <TableCell>{row.name}</TableCell>
                            <TableCell align="right">{formatCurrency(row.creditAmount)}</TableCell>
                            <TableCell align="right">{formatCurrency(row.debitAmount)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
                See more uploads
            </Link>
        </>
    );
}