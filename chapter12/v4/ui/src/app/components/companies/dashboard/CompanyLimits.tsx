import * as React from 'react';
import {useEffect, useState} from 'react';
import Typography from '@mui/material/Typography';
import {formatCurrency} from "@/app/utils/CurrencyUtils";
import axios from "axios";
import Title from "@/app/components/Title";
import {CompanyLimitsResponse} from "@/app/interfaces/companies/CompanyLimitsResponse";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";

interface CompanyLimitsProps {
    companyId?: string;
}

export default function CompanyLimits({companyId}: Readonly<CompanyLimitsProps>) {

    const [response, setResponse] =
        useState<CompanyLimitsResponse>({
            company_limit_id: '',
            daily_debit_limit: 0,
            daily_credit_limit: 0,
            current_debit_total: 0,
            current_credit_total: 0,
            daily_debit_exceeded: false,
            daily_credit_exceeded: false
        } as CompanyLimitsResponse);

    useEffect(() => {

        if (!companyId) {
            return;
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<CompanyLimitsResponse>(`${apiUrl}/companies/${companyId}/limits`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setResponse(response.data);
            })
            .catch(error => {
                console.log(error);
            });

    }, [companyId]);

    return (
        <Container>
            <Paper
                sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                    width: '100%',
                    maxWidth: '500px'
                }}
            >
                <Box sx={{mb: 2}}>
                    <Title>Company Limits</Title>
                    <Typography component="p" variant="h4">
                        Company Credits:
                    </Typography>
                    <Typography component="p" variant="h6">
                        <Typography component="span" variant="h6" style={{color: response.daily_credit_exceeded ? 'red' : 'green'}}>
                            {formatCurrency(response.current_credit_total)}
                        </Typography>
                        {" of "}
                        {formatCurrency(response.daily_credit_limit)}
                    </Typography>
                    <Typography component="p" variant="h4">
                        Company Debits:
                    </Typography>
                    <Typography component="p" variant="h6">
                        <Typography component="span" variant="h6" style={{color: response.daily_debit_exceeded ? 'red' : 'green'}}>
                            {formatCurrency(response.current_debit_total)}
                        </Typography>
                        {" of "}
                        {formatCurrency(response.daily_debit_limit)}
                    </Typography>
                </Box>
            </Paper>
        </Container>
    );
}