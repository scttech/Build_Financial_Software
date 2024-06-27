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
import { IconButton } from '@mui/material';
import Toolbar from "@mui/material/Toolbar"
import InfoIcon from '@mui/icons-material/Info';
import AlertMessage from "@/app/components/dialogs/AlertMessage";
import {AchExceptionDetailsResponse} from "@/app/interfaces/AchExceptionDetailsResponse";
import {AchFiles} from "@/app/interfaces/AchFiles";
import Title from "@/app/components/Title";
import ExceptionsModal from "@/app/components/dialogs/ExceptionsModal";


const defaultTheme = createTheme();

interface ExceptionsProps {
    exceptions: AchExceptionsResponse[];
}

export default function Exceptions({exceptions}: Readonly<ExceptionsProps>) {

    const [isOpen, setIsOpen] = useState(false);
    const [exceptionData, setExceptionData] = useState<AchExceptionDetailsResponse | null>(null);
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
                                setExceptionData(response.data);
                                setIsOpen(true);
                            })
                            .catch(error => {
                                console.log(error);
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
        {field: 'description', headerName: 'Description', width: 300},
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
                            <Title>Exceptions</Title>
                            <DataGrid columns={columns} rows={exceptions} />
                        </Paper>
                    </Container>
            </Box>
            <ExceptionsModal open={isOpen} onClose={() => setIsOpen(false)} exceptionData={exceptionData} />
        </ThemeProvider>
    );
}