'use client';
import * as React from 'react';
import {useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import { IconButton } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import {AuditResponse} from "@/app/interfaces/AuditResponse";
import {convertDateFormat} from "@/app/utils/DateUtils";
import {stripSubnet} from "@/app/utils/StringUtils";
import AuditModal from "@/app/components/dialogs/AuditModal";
import Title from "@/app/components/Title";


const defaultTheme = createTheme();

interface AuditRecordsProps {
    records: AuditResponse[];
}

export default function AuditRecords({records}: Readonly<AuditRecordsProps>) {

    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [auditDetails, setAuditDetails] = useState<AuditResponse | null>(null);
    const columns: GridColDef[] = [
        {field: 'view', headerName: 'View', sortable: false, width: 10, renderCell: (params) => (
                <IconButton
                    onClick={(e) => {
                        e.preventDefault();
                        console.log(`Row data ${JSON.stringify(params.row)}`);
                        setAuditDetails(params.row);
                        setIsOpen(true);
                    }}
                    color="primary"
                >
                    <InfoIcon />
                </IconButton>
            )},
        {field: 'created_at', headerName: 'Date', width: 150, valueGetter: (params) => convertDateFormat(params.value)},
        {field: 'ip_address', headerName: 'IP Address', width: 150, valueGetter: (params) => stripSubnet(params.value)},
        {field: 'message', headerName: 'Audit Message', width: 300},
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
                            <Title>Audit Log</Title>
                            <DataGrid columns={columns} rows={records} getRowId={(row) => row.audit_log_id} />
                        </Paper>
                    </Container>
            </Box>
            <AuditModal open={isOpen} onClose={setIsOpen.bind({}, false)} auditData={auditDetails} />
        </ThemeProvider>
    );
}