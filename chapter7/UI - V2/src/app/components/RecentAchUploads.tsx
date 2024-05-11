import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import {useEffect, useState} from "react";
import axios from 'axios';
import {convertDateFormat} from "@/app/utils/DateUtils";


function preventDefault(event: React.MouseEvent) {
    event.preventDefault();
}

interface AchUpload {
    id: number;
    date: string;
    filename: string;
    creditTotal: number;
    debitTotal: number;
}

export default function RecentAchUploads() {

    const [rows, setRows] = useState<AchUpload[]>([]);

    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get(`${apiUrl}/files`)
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setRows(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

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
                            <TableCell>{convertDateFormat(row.date)}</TableCell>
                            <TableCell>{row.filename}</TableCell>
                            <TableCell align="right">{formatCurrency(row.creditTotal)}</TableCell>
                            <TableCell align="right">{formatCurrency(row.debitTotal)}</TableCell>
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