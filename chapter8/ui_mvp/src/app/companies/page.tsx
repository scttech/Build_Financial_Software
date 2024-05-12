'use client';
import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TopMenuBar from "@/app/components/navigation/TopMenuBar";
import SideBarNav from "@/app/components/navigation/SideBarNav";
import {useState} from "react";
import Container from '@mui/material/Container';

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function Companies() {
    const [open, setOpen] = useState(true);
    const toggleDrawer = () => {
        setOpen(!open);
    };

    return (
        <ThemeProvider theme={defaultTheme}>
            <Box sx={{ display: 'flex' }}>
                <CssBaseline />
                <TopMenuBar toggleDrawer={toggleDrawer} drawerOpen={open} />
                <SideBarNav toggleDrawer={toggleDrawer} drawerOpen={open} />
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
                    <Container maxWidth="lg" sx={{ mt: 9, mb: 4 }}>
                        <Typography>Companies</Typography>
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
}