'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import axios from "axios";
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import {AchExceptionsResponse} from "@/app/interfaces/AchExceptionsResponse";
import {convertDateFormat} from "@/app/utils/DateUtils";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import {IconButton} from '@mui/material';
import Toolbar from "@mui/material/Toolbar"
import InfoIcon from '@mui/icons-material/Info';
import AlertMessage from "@/app/components/dialogs/AlertMessage";
import {AchExceptionDetailsResponse} from "@/app/interfaces/AchExceptionDetailsResponse";


const defaultTheme = createTheme();

export default function Exceptions() {

    const [entries, setEntries] = useState<AchExceptionsResponse[]>([]);
    const [isOpen, setIsOpen] = useState(false);
    const [unparsedRecord, setUnparsedRecord] = useState('');
    const columns: GridColDef[] = [
        {field: 'view', headerName: 'View', sortable: false, width: 10, renderCell: (params) => (
                <IconButton
                    onClick={(e) => {
                        e.preventDefault();
                        console.log(`Row data ${JSON.stringify(params.row)}`);
                        const fileId = params.row.file_id;
                        const exceptionId = params.row.id;
                        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
                        axios.get<AchExceptionDetailsResponse>(`${apiUrl}/files/${fileId}/exceptions/${exceptionId}`, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        })
                            .then(response => {
                                console.log(`Response data ${JSON.stringify(response.data)}`);
                                setUnparsedRecord(response.data.unparsed_record);
                                setIsOpen(true);
                            })
                            .catch(error => {
                                console.log(error);
                                setUnparsedRecord(error.message)
                                setIsOpen(true);
                            });

                    }}
                    color="primary"
                >
                    <InfoIcon />
                </IconButton>
            )},
        {field: 'file_name', headerName: 'Filename', width: 150},
        {field: 'created_at', headerName: 'Date', width: 150, valueGetter: (params) => convertDateFormat(params.value)},
        {field: 'record_number', headerName: 'Record Number', width: 150},
        {field: 'exception_code', headerName: 'Code', width: 10},
        {field: 'description', headerName: 'Description', width: 300},
    ]
    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchExceptionsResponse[]>(`${apiUrl}/files/exceptions`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setEntries(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    return (
        <ThemeProvider theme={defaultTheme}>
            <Box sx={{display: 'flex'}}>
                <CssBaseline/>
                <StandardNavigation/>
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
                            <DataGrid columns={columns} rows={entries}/>
                        </Paper>
                    </Container>
                </Box>
            </Box>
            <AlertMessage open={isOpen} setOpen={setIsOpen} message={unparsedRecord} title="Unparsed Record" />
        </ThemeProvider>
    );
}