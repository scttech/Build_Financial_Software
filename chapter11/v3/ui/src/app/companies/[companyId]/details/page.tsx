'use client';
import * as React from 'react';
import {useEffect, useState} from 'react';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import StandardNavigation from "@/app/components/navigation/StandardNavigation";
import axios from "axios";
import Toolbar from "@mui/material/Toolbar"
import CompanyDetailsForm from "@/app/components/companies/CompanyDetailsForm";
import {CompanyDetailResponse} from "@/app/interfaces/companies/CompanyDetailResponse";
import {Company} from "@/app/interfaces/companies/Company";
import {IndustryType} from "@/app/interfaces/common/IndustryType";


const defaultTheme = createTheme();


export default function CompanyDetailsPage({params}: any) {

    const companyId: string | string[] = params.companyId;
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
                    <Toolbar />
                    <CompanyDetailsForm company={company}></CompanyDetailsForm>
                </Box>
            </Box>
        </ThemeProvider>
    );
}