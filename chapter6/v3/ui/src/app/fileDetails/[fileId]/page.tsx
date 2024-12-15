'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import AchBatchesScatterPlot from "@/app/components/charts/scatter/AchBatchesScatterPlot";
import axios from "axios";
import Paper from "@mui/material/Paper";
import {Accordion, AccordionDetails, AccordionSummary, Divider} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Decimal from "decimal.js";
import {useRouter} from "next/navigation";
import { formatCurrency } from '@/app/utils/CurrencyUtils';

export interface AchBatchInfo {
    id: string;
    companyId: string;
    companyName: string;
    batchNumber: number;
    debitTotal: Decimal;
    creditTotal: Decimal;
    recordCount: number;
}

export interface AchBatchInfo {
    companyName: string;
    companyBatches: AchBatchDetails[];
}

export interface AchBatchDetails {
    batchId: string;
    companyName: string;
    recordCount: number;
    totalDebitAmount: number;
    totalCreditAmount: number;
}

interface AchBatchInfoResponse {
    batches: AchBatchInfo[];
}

const defaultTheme = createTheme();

export default function FileDetails({params}: any) {

    const fileId: string | string[] = params.fileId;
    const [batches, setBatches] = useState<AchBatchInfo[]>([]);
    const route = useRouter();


    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<AchBatchInfoResponse>(`${apiUrl}/files/${fileId}/batches`)
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setBatches(response.data.batches);
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
                                <AccordionDetails>
                                {item.companyBatches.map((companyBatch, index) => (
                                    <>
                                        <Typography>
                                            Batch ID: {companyBatch.batchId}<br />
                                            Record Count: {companyBatch.recordCount}<br />
                                            Total Debit Amount: {formatCurrency(companyBatch.totalDebitAmount)}<br />
                                            Total Credit Amount: {formatCurrency(companyBatch.totalCreditAmount)}
                                        </Typography>
                                        <Link>View Batch</Link>
                                        <Divider />
                                    </>
                                )
                                )}
                                </AccordionDetails>
                            </Accordion>

                        ))}
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
}