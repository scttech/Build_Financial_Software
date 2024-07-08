'use client';
import * as React from 'react';
import {useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import {AuditResponse} from "@/app/interfaces/AuditResponse";
import Title from "@/app/components/Title";
import {OfacResponse} from "@/app/interfaces/ofac/OfacResponse";
import Link from "@mui/material/Link";
import {CheckCircle} from "@mui/icons-material";
import Typography from "@mui/material/Typography";


const defaultTheme = createTheme();

interface OfacRecordsProps {
    records: OfacResponse[];
}

export default function OfacRecords({records}: Readonly<OfacRecordsProps>) {

    const columns: GridColDef[] = [
        {
            field: 'ach_files_id',
            headerName: '',
            width: 100,
            renderCell: (params) => (
                <Link href={`/fileDetails/${params.value}`} color="inherit">
                    View File
                </Link>
            ),
        },
        {
            field: 'ach_batch_id',
            headerName: '',
            width: 100,
            renderCell: (params) => (
                <Link href={`/fileDetails/${params.row.ach_files_id}/batchDetails/${params.value}`} color="inherit">
                    View batch
                </Link>
            ),
        },
        {field: 'sdn_name', headerName: 'Suspect Name', width: 150},
        {field: 'alias', headerName: 'Suspect Alias', width: 150},
        {field: 'individual_name', headerName: 'Customer Name', width: 150},
        {field: 'similarity_score', headerName: 'Score', width: 75, renderCell: (params) => (
                <Typography>{Math.floor(params.value)}</Typography>
            )},
        {
            field: 'daitch_mokotoff_match_name',
            headerName: 'Name Match',
            width: 100,
            renderCell: (params) => (
                <Box
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    width="100%"
                    height="100%"
                >
                    {params.value ? <CheckCircle sx={{color: "green"}}/> : null}
                </Box>),
        },
        {
            field: 'daitch_mokotoff_match_alias',
            headerName: 'Alias Match',
            width: 100,
            renderCell: (params) => (
                <Box
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    width="100%"
                    height="100%"
                >
                    {params.value ? <CheckCircle sx={{color: "green"}}/> : null}
                </Box>),
        },
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
                        <Title>OFAC Report</Title>
                        <DataGrid columns={columns} rows={records}/>
                    </Paper>
                </Container>
            </Box>
        </ThemeProvider>
    );
}