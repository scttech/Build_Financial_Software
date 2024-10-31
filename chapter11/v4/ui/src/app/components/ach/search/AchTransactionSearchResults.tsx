'use client';
import * as React from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import Link from "@mui/material/Link";
import {useRouter} from "next/navigation";
import {AchTransactionSearchResponse} from "@/app/interfaces/AchTransactionSearchResultsResponse";



const defaultTheme = createTheme();

interface AchTransactionSearchResultsProps {
    results: AchTransactionSearchResponse[];
}

export default function AchTransactionSearchResults({results}: Readonly<AchTransactionSearchResultsProps>) {

    const route = useRouter();

    const columns: GridColDef[] = [
        {field: 'filename', headerName: 'Filename', width: 150},
        {field: 'individual_name', headerName: 'Individual Name', width: 150},
        {field: 'amount', headerName: 'Amount', width: 100},
        {field: 'viewFile', headerName: '', sortable: false, width: 150, renderCell: (params) => (
            <Link onClick={() => route.push(`/fileDetails/${params.row.file_id}`)} sx={{ cursor: 'pointer' }}>Jump to file...</Link>
            )},
        {field: 'viewBatch', headerName: '', sortable: false, width: 150, renderCell: (params) => (
            <Link onClick={() => route.push(`/fileDetails/${params.row.file_id}/batchDetails/${params.row.batch_header_id}`)} sx={{ cursor: 'pointer' }}>Jump to batch...</Link>
            )}
    ];

    return (
        <ThemeProvider theme={defaultTheme}>
            <Box sx={{display: 'flex'}}>
                <CssBaseline/>
                    <Container maxWidth="lg" sx={{mt: 4, mb: 4, ml: 4}}>
                        <Paper
                            sx={{
                                p: 2,
                                display: 'flex',
                                flexDirection: 'column',
                                height: 480,
                                width: '100%'
                            }}
                        >
                            <DataGrid columns={columns} rows={results} getRowId={(row) => row.entry_id} />
                        </Paper>
                    </Container>
            </Box>
        </ThemeProvider>
    );
}