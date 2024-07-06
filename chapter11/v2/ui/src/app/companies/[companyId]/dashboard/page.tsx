'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import CompanyInformation from "@/app/components/companies/dashboard/CompanyInformation";
import {Company} from "@/app/interfaces/companies/Company";
import {CompanyDetailResponse} from "@/app/interfaces/companies/CompanyDetailResponse";
import {IndustryType} from "@/app/interfaces/common/IndustryType";
import axios from "axios";
import RecentCompanyBatches from "@/app/components/companies/dashboard/RecentCompanyBatches";

function Copyright(props: any) {
    return (
        <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/" sx={{ cursor: 'pointer' }}>
                Full Stack FinTech
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function CompanyDashboard({params}: any) {

    const companyId: string = params.companyId;
    const [company, setCompany] = useState<Company | undefined>(undefined);

    function convertToCompany(detailResponse: CompanyDetailResponse): Company {
    return {
      name: detailResponse.name,
        taxIdType: detailResponse.tax_id_type,
        taxIdNumber: detailResponse.tax_id_number,
        duns: detailResponse.duns,
        logo: detailResponse.logo,
        achCompanyId: detailResponse.ach_company_id,
        website: detailResponse.website,
        industry: detailResponse.industry as IndustryType,
        addresses: detailResponse.addresses.map(address => ({
            addressType: address.address_type,
            addressLine1: address.address_line_1,
            addressLine2: address.address_line_2 || '',
            addressLine3: address.address_line_3 || '',
            addressLine4: address.address_line_4 || '',
            city: address.city,
            state: address.state,
            zipCode: address.zip_code,
            zipCode4: address.zip_code_4 || ''
        })),
        phones: detailResponse.phones.map(phone => ({
            phoneType: phone.phone_type,
            phoneNumber: phone.phone_number,
            extension: phone.extension || '',
            allowSms: phone.allow_sms,
        })),
    };
}

    useEffect(() => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
        axios.get<CompanyDetailResponse>(`${apiUrl}/companies/${companyId}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                console.log(`Response data ${JSON.stringify(response.data)}`);
                setCompany(convertToCompany(response.data));
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
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                        <Grid container spacing={3}>
                            <Grid item xs={12} md={8} lg={9}>
                                <CompanyInformation companyId={companyId} company={company} />
                            </Grid>
                            <Grid item xs={12} md={8} lg={9}>
                                <RecentCompanyBatches companyId={companyId} />
                            </Grid>
                        </Grid>
                        <Copyright sx={{ pt: 4 }} />
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
}