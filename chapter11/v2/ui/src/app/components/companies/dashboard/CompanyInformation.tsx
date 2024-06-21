// components/CompanyInformation.js
import React, {useLayoutEffect, useState} from 'react';
import {Container, Grid, Paper, Typography, Box} from '@mui/material';
import {TinType} from "@/app/interfaces/common/TinType";
import {Company} from "@/app/interfaces/companies/Company";
import {AddressType} from "@/app/interfaces/common/AddressType";
import {PhoneType} from "@/app/interfaces/common/PhoneType";
import {IndustryType} from "@/app/interfaces/common/IndustryType";
import ImageBase64 from "@/app/components/images/ImageBase64";
import StandardSubmitButton from "@/app/components/input/buttons/StandardButton";
import {useRouter} from "next/navigation";

interface CompanyInformationProps {
    companyId?: string;
    company?: Company;
}

export default function CompanyInformation(props: Readonly<CompanyInformationProps>) {
    const [companyEntry, setCompanyEntry] = useState<Company>({
        name: '',
        taxIdType: TinType.EIN,
        taxIdNumber: '',
        duns: 0,
        achCompanyId: 0,
        logo: '',
        website: '',
        industry: IndustryType.TECHNOLOGY,
        addresses: [{
            addressType: AddressType.STREET,
            addressLine1: '',
            city: '',
            state: '',
            zipCode: '',
            zipCode4: ''
        }],
        phones: [{phoneType: PhoneType.MAIN, phoneNumber: '', extension: '', allowSms: false}],
    });

    useLayoutEffect(() => {
        if (props.company) {
            setCompanyEntry(props.company);
        }
    }, [props]);

    const address = companyEntry.addresses[0];
    const phone = companyEntry.phones[0];
    const router = useRouter();

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
                    <Typography variant="h6">Company Information</Typography>
                </Box>
                <Grid container>
                    <Grid item xs={8}>
                        <Grid container>
                            <Grid item xs={4}>
                                <Typography variant="body1" fontWeight="bold" align="right">Company Name:</Typography>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography variant="body1">{companyEntry.name}</Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="body1" fontWeight="bold" align="right">Website:</Typography>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography variant="body1">{companyEntry.website}</Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="body1" fontWeight="bold" align="right">Industry:</Typography>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography variant="body1">{companyEntry.industry}</Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={4}>
                        <ImageBase64 base64={companyEntry.logo ?? ''} alt={companyEntry.name} width="100%" maxWidth="100px" />
                    </Grid>
                </Grid>
                <Box sx={{mt: 2, mb: 2}}>
                    <Typography variant="h6">Address Information</Typography>
                </Box>
                <Grid container>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">Address Line 1:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{address.addressLine1}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">City:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{address.city}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">State:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{address.state}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">Zip Code:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{address.zipCode}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">Zip Code+4:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{address.zipCode4}</Typography>
                    </Grid>
                </Grid>
                <Box sx={{mt: 2, mb: 2}}>
                    <Typography variant="h6">Contact Information</Typography>
                </Box>
                <Grid container>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">Phone Number:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{phone.phoneNumber}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="body1" fontWeight="bold" align="right">Extension:</Typography>
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="body1">{phone.extension}</Typography>
                    </Grid>
                </Grid>
                <StandardSubmitButton onClick={() => router.push(`/companies/${props.companyId}/details`)} variant="contained" color="primary">
                    Edit
                </StandardSubmitButton>
            </Paper>
        </Container>
    );
};
