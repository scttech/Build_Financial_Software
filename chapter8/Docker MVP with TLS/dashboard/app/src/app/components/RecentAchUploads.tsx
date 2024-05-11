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
import {AchFiles} from "@/app/interfaces/AchFiles";
import {AchFilesResponse} from "@/app/interfaces/AchFilesResponse";


function preventDefault(event: React.MouseEvent) {
    event.preventDefault();
}

interface RecentAchUploadsProps {
    files: AchFiles[];
}

export default function RecentAchUploads({files}: Readonly<RecentAchUploadsProps>) {

    const route = useRouter();

    return (
        <>
            <Title>Recent ACH Uploads</Title>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Filename</TableCell>
                        <TableCell>Originator</TableCell>
                        <TableCell align="right">Credit Total</TableCell>
                        <TableCell align="right">Debit Total</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {files.map((file) => (
                        <TableRow key={file.id}>
                            <TableCell>{convertDateFormat(file.date)}</TableCell>
                            <TableCell>
                                <Link onClick={() => route.push(`/fileDetails/${file.id}`)} sx={{ cursor: 'pointer' }}>{file.filename}</Link>
                            </TableCell>
                            <TableCell>{file.originator}</TableCell>
                            <TableCell align="right">{formatCurrency(file.creditTotal)}</TableCell>
                            <TableCell align="right">{formatCurrency(file.debitTotal)}</TableCell>
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