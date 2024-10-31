'use client';
import * as React from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import {CompaniesListingResponse} from "@/app/interfaces/companies/CompaniesListingResponse";
import ImageBase64 from "@/app/components/images/ImageBase64";
import {useRouter} from "next/navigation";

const defaultTheme = createTheme();

interface CompaniesListingProps {
    companies: CompaniesListingResponse[];
}

export default function CompaniesListing({companies}: Readonly<CompaniesListingProps>) {

    const route = useRouter();
    const columns: GridColDef[] = [
        {field: 'view', headerName: '', sortable: false, width: 100, renderCell: (params) => (
            <ImageBase64 base64={params.row.logo} alt={params.row.name} width="100%" maxWidth="200px" />
            )},
        {field: 'name', headerName: 'Name', width: 300 },
        {field: 'industry', headerName: 'Industry', width: 150 },
    ];

    const handleRowClick = (params: { id: any; }) => {
        const companyId = params.id;
        console.log(`Row clicked ${companyId}`);
        route.push(`/companies/${companyId}/dashboard`);
    };

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
                                height: '100%',
                                width: '100%'
                            }}
                        >
                            <DataGrid
                                rowHeight={100}
                                columns={columns}
                                rows={companies}
                                getRowId={(row) => row.company_id}
                                onRowClick={handleRowClick}
                            />
                        </Paper>
                    </Container>
            </Box>
        </ThemeProvider>
    );
}