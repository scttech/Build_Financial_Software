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
import {useRouter} from "next/navigation";
import Decimal from "decimal.js";


function preventDefault(event: React.MouseEvent) {
    event.preventDefault();
}

interface AchFiles {
    id: number;
    date: string;
    filename: string;
    creditTotal: Decimal;
    debitTotal: Decimal;
}

interface AchFilesResponse {
    id: number;
    date: string;
    filename: string;
    credit_total: number;
    debit_total: number;
}

export default function RecentAchUploads() {

    const [rows, setRows] = useState<AchFiles[]>([]);
    const route = useRouter();

    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchFilesResponse[]>(`${apiUrl}/files`)
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                const transformedData: AchFiles[] = response.data.map((row: AchFilesResponse) => ({
                  id: row.id,
                    date: row.date,
                    filename: row.filename,
                    creditTotal: new Decimal(row.credit_total),
                    debitTotal: new Decimal(row.debit_total)
                }));
                setRows(transformedData);
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
                            <TableCell>
                                <Link onClick={() => route.push(`/fileDetails/${row.id}`)}>{row.filename}</Link>
                            </TableCell>
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