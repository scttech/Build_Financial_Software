'use client';
import * as React from 'react';
import {DragEvent, useCallback, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import {CloudUpload} from "@mui/icons-material";
import StandardNavigation from "@/app/components/navigation/StandardNavigation";


// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function Uploads() {
    const [dragOver, setDragOver] = useState(false);
    const [fileInfo, setFileInfo] = useState<File>();

    const handleDragOver = useCallback((event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setDragOver(true);
    }, []);

    const handleDragLeave = useCallback(() => {
        setDragOver(false);
    }, []);

    const handleDrop = useCallback((event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setDragOver(false);

        const files = event.dataTransfer.files;
        // Handle file upload here
        if ( files.length > 0 && files[0].name !== '' ) {
            console.log(files);
            setFileInfo(files[0]);
        }

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
                    <Box display="flex" justifyContent="center" alignItems="center" height="30vh" sx={{ mt: 10, mx: 4}}>
                        <Paper
                            variant="outlined"
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={handleDrop}
                            sx={{
                                width: '100%',
                                height: '100%',
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                backgroundColor: dragOver ? 'lightblue' : 'white',
                                textAlign: 'center',
                                cursor: 'pointer',
                                borderWidth: 1,
                                borderColor: dragOver ? 'black' : 'lightblue',
                                borderStyle: dragOver ? 'dashed' : 'solid'
                            }}
                        >
                                <Typography variant="h6">{fileInfo?.name ? fileInfo.name : 'Drag and drop files here'}</Typography>
                        </Paper>
                    </Box>
                    <Box display="flex" justifyContent="center" mt={2}>
                        <Button
                            startIcon={<CloudUpload />}>
                            Upload
                        </Button>
                    </Box>
                </Box>
            </Box>
        </ThemeProvider>
    );
}