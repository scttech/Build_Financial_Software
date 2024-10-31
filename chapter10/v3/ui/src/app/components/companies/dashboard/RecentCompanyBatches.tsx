import React, {useEffect, useState} from 'react';
import {Box, Container, Paper} from '@mui/material';
import {useRouter} from "next/navigation";
import axios from "axios";
import {AchBatchSearchResponse} from "@/app/interfaces/AchBatchSearchResponse";
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import Link from "@mui/material/Link";
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Title from "@/app/components/Title";

interface RecentCompanyBatchesProps {
    companyId?: string;
}

export default function RecentCompanyBatches({companyId}: Readonly<RecentCompanyBatchesProps>) {

    const router = useRouter();
    const [results, setResults] = useState<AchBatchSearchResponse[]>([]);

    useEffect(() => {

        if (!companyId) {
            return;
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchBatchSearchResponse[]>(`${apiUrl}/files/batches/search?criteria=${companyId}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setResults(response.data);
            })
            .catch(error => {
                console.log(error);
            });

    }, [companyId]);

    const columns: GridColDef[] = [
       {field: 'file_id', headerName: 'File', sortable: false, width: 50, renderCell: (params) => (
            <Link onClick={() => router.push(`/fileDetails/${params.row.file_id}`)} sx={{ cursor: 'pointer' }}>View</Link>
            )},
        {field: 'batch_header_id', headerName: 'Batch', sortable: false, width: 50, renderCell: (params) => (
            <Link onClick={() => router.push(`/fileDetails/${params.row.file_id}/batchDetails/${params.row.batch_header_id}`)} sx={{ cursor: 'pointer' }}>View</Link>
            )},
        {field: 'filename', headerName: 'Filename', width: 200},
        {field: 'company_name', headerName: 'Company Name', width: 200},
        {field: 'total_credit_entry_dollar_amount', headerName: 'Total Credit', width: 125, renderCell: (params) => (
            formatCurrency(Number(params.row.total_credit_entry_dollar_amount))
            )},
        {field: 'total_debit_entry_dollar_amount', headerName: 'Total Debit', width: 125, renderCell: (params) => (
            formatCurrency(Number(params.row.total_debit_entry_dollar_amount))
            )},
    ];

    return (
        <Container>
            <Paper
                sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                    width: '100%',
                    maxWidth: '1000px'
                }}
            >
                <Box sx={{mb: 2}}>
                    <Title>Recent Company Batches</Title>
                    <DataGrid rows={results} columns={columns} getRowId={(row: any) => row.batch_header_id}/>
                </Box>
            </Paper>
        </Container>
    );
};
