'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import axios from "axios";
import {DataGrid, GridColDef} from '@mui/x-data-grid';
import Toolbar from "@mui/material/Toolbar";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import AchTransactionCodesPieChart from "@/app/components/charts/pie/AchTransactionCodesPieChart";
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Decimal from "decimal.js";


const defaultTheme = createTheme();

const columns: GridColDef[] = [
    { field: 'transaction_code', headerName: 'Transaction Code', width: 150},
    { field: 'transaction_description', headerName: 'Description', width: 150},
    { field: 'account_number_last_4', headerName: 'Account Number', width: 150},
    { field: 'individual_name', headerName: 'Name', width: 150},
    { field: 'amount', headerName: 'Amount', width: 150},
    { field: 'addenda_count', headerName: 'Addenda Count', width: 150},
]


export interface AchBatchEntriesResponse {
    id: string;
    transaction_code: number;
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
        <ThemeProvider theme={defaultTheme}>
            <Box sx={{ display: 'flex' }}>
                <CssBaseline />
                <StandardNavigation />
                <Box
                    component="main"
                    sx={{
                        backgroundColor: (theme) =>
                            theme.palette.mode === 'light'
                                ? theme.palette.grey[100]
                                : theme.palette.grey[900],
                        flexGrow: 1,
                        height: '100vh',
                        overflow: 'auto',
                    }}
                >
                    <Toolbar />
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4, ml: 4 }}>
                        <Paper
                            sx={{
                                p: 2,
                                display: 'flex',
                                flexDirection: 'column',
                                height: 480,
                                width: '100%'
                            }}
                        >
                            <AchTransactionCodesPieChart entries={entries} />
                        </Paper>
                    </Container>
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4, ml: 4 }}>
                        <Paper
                            sx={{
                                p: 2,
                                display: 'flex',
                                flexDirection: 'column',
                                height: 480,
                                width: '100%'
                            }}
                        >
                            <DataGrid columns={columns} rows={entries} />
                        </Paper>
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
}