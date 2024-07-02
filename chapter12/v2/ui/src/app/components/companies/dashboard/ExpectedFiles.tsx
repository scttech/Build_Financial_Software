import React, {useEffect, useState} from 'react';
import {Container, Paper, Box} from '@mui/material';
import axios from "axios";
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import Title from "@/app/components/Title";
import {CompanyExpectedFilesResponse} from "@/app/interfaces/companies/CompanyExpectedFilesResponse";
import {RadioButtonUnchecked, TaskAlt} from "@mui/icons-material";

interface ExpectedFilesProps {
    companyId?: string;
}

export default function ExpectedFiles({companyId}: Readonly<ExpectedFilesProps>) {

    const [results, setResults] = useState<CompanyExpectedFilesResponse[]>([]);

    useEffect(() => {

        if (!companyId) {
            return;
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<CompanyExpectedFilesResponse[]>(`${apiUrl}/companies/${companyId}/expected_files`, {
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

    }, [companyId]);

    const columns: GridColDef[] = [
        {field: 'file_loaded', headerName: 'Loaded', width: 75, renderCell: (params) => (
                params.value ? <TaskAlt sx={{color: "green"}} /> : <RadioButtonUnchecked />
            )},
        {field: 'file_name', headerName: 'File Name', width: 200},
        {field: 'schedule', headerName: 'Schedule', width: 75},
        {
            field: 'last_file_date', headerName: 'Last File Date', width: 100,
            renderCell: (params) => (
                params.value ? new Date(params.value as string).toLocaleDateString() : ''
            ),
        },
       {
            field: 'next_file_date', headerName: 'Next Expected Date', width: 150,
            renderCell: (params) => (
                params.value ? new Date(params.value as string).toLocaleDateString() : ''
            ),
        },
    ];

    return (
        <Container>
            <Paper
                sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                    width: '100%',
                    maxWidth: '650px'
                }}
            >
                <Box sx={{mb: 2}}>
                    <Title>Expected Files</Title>
                    <DataGrid rows={results} columns={columns} getRowId={(row: any) => row.company_expected_file_id}/>
                </Box>
            </Paper>
        </Container>
    );
};
