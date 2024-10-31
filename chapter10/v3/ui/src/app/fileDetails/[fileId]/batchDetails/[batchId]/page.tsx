'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import axios from "axios";
import {DataGrid, GridColDef} from '@mui/x-data-grid';
import Paper from "@mui/material/Paper";
import AchTransactionCodesPieChart from "@/app/components/charts/pie/AchTransactionCodesPieChart";
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Decimal from "decimal.js";
import AchBatchStatistics from "@/app/components/ach/batches/AchBatchStatistics";
import Title from "@/app/components/Title";
import Grid from '@mui/material/Unstable_Grid2';


const defaultTheme = createTheme();

const columns: GridColDef[] = [
    { field: 'transaction_code', headerName: 'Transaction Code', width: 150},
    { field: 'transaction_description', headerName: 'Description', width: 150},
    { field: 'application', headerName: 'Application', width: 150},
    { field: 'account_number_last_4', headerName: 'Account Number', width: 150},
    { field: 'individual_name', headerName: 'Name', width: 150},
    { field: 'amount', headerName: 'Amount', width: 150},
    { field: 'addenda_count', headerName: 'Addenda Count', width: 150},
]


export interface AchBatchEntriesResponse {
    id: string;
    transaction_code: number;
    application: string;
    transaction_description: string;
    amount: string;
    individual_name: string;
    account_number_last_4: string;
    addenda_count: number;
}


export default function BatchEntries({params}: any) {

    const fileId: string | string[] = params.fileId;
    const batchId: string | string[] = params.batchId;
    const [entries, setEntries] = useState<AchBatchEntriesResponse[]>([]);

    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchBatchEntriesResponse[]>(`${apiUrl}/files/${fileId}/batches/${batchId}/entries`)
            .then(response => {
                console.log(`Response data for entries: ${JSON.stringify(response.data)}`);
                const reformattedEntries = response.data.map(entry => ({
                    ...entry,
                    amount: formatCurrency(new Decimal(entry.amount))
                }));
                console.log(`Reformatted entries: ${JSON.stringify(reformattedEntries)}`);
                setEntries(reformattedEntries);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <StandardNavigation />
            <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }} sx={{mt: 8, pl: 1, pr: 1}}>
                <Grid xs={12} sm={6} key={1} >
                        <AchTransactionCodesPieChart entries={entries} />
                </Grid>
                <Grid xs={12} sm={6} key={2} >
                        <AchBatchStatistics entries={entries}/>
                </Grid>
                <Grid xs={12} key={3} >
                    <Paper sx={{
                        minWidth: 1075,
                        maxWidth: 1075,
                    }}>
                        <Title>Batch Entries</Title>
                        <DataGrid columns={columns} rows={entries} />
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );

}