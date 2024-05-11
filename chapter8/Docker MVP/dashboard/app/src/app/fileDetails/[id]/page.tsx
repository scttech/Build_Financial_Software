'use client';
import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import AchBatchesScatterPlot from "@/app/components/charts/AchBatchesScatterPlot";
import {useEffect, useState} from "react";
import axios from "axios";
import Paper from "@mui/material/Paper";
import {Accordion, AccordionDetails, AccordionSummary, Divider} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Decimal from "decimal.js";

export interface AchBatchInfo {
    id: string;
    batchNumber: number;
    debitTotal: Decimal;
    creditTotal: Decimal;
    recordCount: number;
}

export interface AchCompanyBatchInfo {
    companyName: string;
    companyBatches: AchBatchInfo[];
}
export interface AchBatchInfoResponse {
    id: string;
    company_name: string;
    batch_number: number;
    debit_total: string;
    credit_total: string;
    entry_addenda_count: number;
}

const defaultTheme = createTheme();

function createAchCompanyBatchInfoRecords(response: AchBatchInfoResponse[]): AchCompanyBatchInfo[] {
    const condensedRecords: Record<string, AchCompanyBatchInfo> = {};

    response.forEach((record: AchBatchInfoResponse) => {
        if (!condensedRecords[record.company_name]) {
            condensedRecords[record.company_name] = {
                companyName: record.company_name,
                companyBatches: []
            };
        }

        condensedRecords[record.company_name].companyBatches.push({
            id: record.id,
            batchNumber: record.batch_number,
            debitTotal: new Decimal(record.debit_total),
            creditTotal: new Decimal(record.credit_total),
            recordCount: record.entry_addenda_count,
        });
    });

    return Object.values(condensedRecords);

}

export default function FileDetails({params}: any) {

    const id: string | string[] = params.id;
    const [batches, setBatches] = useState<AchCompanyBatchInfo[]>([]);

    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchBatchInfoResponse[]>(`${apiUrl}/files/${id}/batches`)
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setBatches(createAchCompanyBatchInfoRecords(response.data));
            })
            .catch(error => {
                console.log(error);
            });
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
                    <Toolbar />
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4, ml: 4 }}>
                            <Paper
                                sx={{
                                    p: 2,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    height: 480,
                                    width: '100%'
                                }}
                            >
                                <AchBatchesScatterPlot batches={batches} />
                            </Paper>
                     </Container>
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4, ml: 4 }}>
                    {batches.map((item, index) => (
                            <Accordion key={item.companyName}>
                                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                    <Typography>{item.companyName}</Typography>
                                </AccordionSummary>
                                {item.companyBatches.map((item, index) => (
                                <AccordionDetails key={item.id}>
                                        <Typography>
                                            Batch ID: {item.id}<br />
                                            Record Count: {item.recordCount}<br />
                                            Total Debit Amount: {formatCurrency(item.debitTotal)}<br />
                                            Total Credit Amount: {formatCurrency(item.creditTotal)}
                                        </Typography>
                                        <Link>View Batch</Link>
                                        <Divider />
                                </AccordionDetails>
                                ))}
                            </Accordion>
                        ))}
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
}