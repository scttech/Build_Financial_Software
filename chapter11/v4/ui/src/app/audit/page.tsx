'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import axios from "axios";
import Toolbar from "@mui/material/Toolbar"
import {AuditResponse} from "@/app/interfaces/AuditResponse";
import AuditRecords from "@/app/components/audit/AuditLogRecords";


const defaultTheme = createTheme();

export default function AuditPage() {

    const [entries, setEntries] = useState<AuditResponse[]>([]);

    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AuditResponse[]>(`${apiUrl}/audits`, {
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
                    <AuditRecords records={entries}/>
                </Box>
            </Box>
        </ThemeProvider>
    );
}