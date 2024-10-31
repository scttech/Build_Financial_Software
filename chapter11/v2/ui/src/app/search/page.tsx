'use client';
import * as React from 'react';
import {useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import axios from "axios";
import Toolbar from "@mui/material/Toolbar"
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import AchTransactionSearchResults from "@/app/components/ach/search/AchTransactionSearchResults";
import {AchTransactionSearchResponse} from "@/app/interfaces/AchTransactionSearchResultsResponse";


const defaultTheme = createTheme();

export default function SearchPage() {
    const [searchCriteria, setSearchCriteria] = useState<string>('');
    const [results, setResults] = useState<AchTransactionSearchResponse[]>([]);

    const handleChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setSearchCriteria(event.target.value);
    };

    const handleSearch = async () => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchTransactionSearchResponse[]>(`${apiUrl}/files/transactions/search?criteria=${searchCriteria}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setResults(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    };

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
                    <Toolbar/>
                    <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2}}>
                        <TextField id="searchinput" label="Search" variant="standard" onChange={handleChange} sx={{ width: '40%' }} />
                        <Button variant="outlined" id="searchbtn" color="primary" onClick={handleSearch}>
                            Search
                        </Button>
                    </Box>
                    <AchTransactionSearchResults results={results}/>
                </Box>
            </Box>
        </ThemeProvider>
    );
}