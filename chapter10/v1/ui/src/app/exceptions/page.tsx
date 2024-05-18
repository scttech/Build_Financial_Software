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
import Exceptions from "@/app/components/ach/exceptions/Exceptions";


const defaultTheme = createTheme();

export default function ExceptionsPage() {

    const [entries, setEntries] = useState<AchExceptionsResponse[]>([]);

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
                    <Exceptions exceptions={entries} />
                </Box>
            </Box>
        </ThemeProvider>
    );
}