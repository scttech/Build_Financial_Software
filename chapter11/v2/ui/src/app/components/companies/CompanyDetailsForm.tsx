// components/CompanyForm.js
import React, {useLayoutEffect, useState} from 'react';
import {TextField, MenuItem, Grid, Typography, Paper, Container} from '@mui/material';
import {TinType} from "@/app/interfaces/common/TinType";
import {Company} from "@/app/interfaces/companies/Company";
import {AddressType} from "@/app/interfaces/common/AddressType";
import {PhoneType} from "@/app/interfaces/common/PhoneType";
import {IndustryType} from "@/app/interfaces/common/IndustryType";
import StandardSubmitButton from "@/app/components/input/buttons/StandardButton";

interface CompanyDetailsFormProps {
    company?: Company;
}

export default function CompanyDetailsForm(props: Readonly<CompanyDetailsFormProps>) {
    const [companyEntry, setCompanyEntry] = useState<Company>({
        name: '',
        taxIdType: TinType.EIN,
        taxIdNumber: '',
        duns: 0,
        logo: null,
        website: '',
        industry: undefined,
        addresses: [{addressType: AddressType.STREET, addressLine1: '', city: '', state: '', zipCode: ''}],
        phones: [{phoneType: PhoneType.MAIN, phoneNumber: '', extension: '', allowSms: false}],
    });

    useLayoutEffect(() => {
        if (props.company) {
            setCompanyEntry(props.company);
        }
    }, [props]);

    const handleChange = (e: { target: { name: any; value: any; }; }) => {
        const {name, value} = e.target;
        setCompanyEntry((prev) => ({...prev, [name]: value}));
    };

    const handleAddressChange = (index: number, e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const {name, value} = e.target;
        const addresses = [...companyEntry.addresses];
        addresses[index] = {...addresses[index], [name]: value};
        setCompanyEntry((prev) => ({...prev, addresses}));
    };

    const handlePhoneChange = (index: number, e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const {name, value} = e.target;
        const phones = [...companyEntry.phones];
        phones[index] = {...phones[index], [name]: value};
        setCompanyEntry((prev) => ({...prev, phones}));
    };

    const handleSubmit = (e: { preventDefault: () => void; }) => {
        e.preventDefault();
        // Perform form submission logic here (e.g., send data to API)
        console.log(companyEntry);
    };

    return (
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
                <form onSubmit={handleSubmit}>
                    <Typography variant="h6" gutterBottom>
                        Company Information
                    </Typography>
                    <Grid container spacing={3}>
                        <Grid item xs={12}>
                            <TextField
                                required
                                label="Company Name"
                                name="name"
                                fullWidth
                                value={companyEntry.name}
                                onChange={handleChange}
                            />
                        </Grid>
                        <Grid item xs={3}>
                            <TextField
                                required
                                select
                                label="Tax ID Type"
                                name="taxIdType"
                                fullWidth
                                value={companyEntry.taxIdType}
                                onChange={handleChange}
                            >
                                {Object.values(TinType).map((type) => (
                                    <MenuItem key={type} value={type}>
                                        {type}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                label="Tax ID Number"
                                name="taxIdNumber"
                                fullWidth
                                value={companyEntry.taxIdNumber}
                                onChange={handleChange}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="DUNS Number"
                                name="duns"
                                fullWidth
                                value={companyEntry.duns}
                                onChange={handleChange}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="Website"
                                name="website"
                                type="url"
                                fullWidth
                                value={companyEntry.website}
                                onChange={handleChange}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                select
                                label="Industry"
                                name="industry"
                                fullWidth
                                value={companyEntry.industry}
                                onChange={handleChange}
                            >
                                {Object.values(IndustryType).map((type) => (
                                    <MenuItem key={type} value={type}>
                                        {type}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                    </Grid>
                    <Typography variant="h6" gutterBottom style={{marginTop: '20px'}}>
                        Address Information
                    </Typography>
                    {companyEntry.addresses?.map((address, index) => (
                        <Grid container spacing={3} key={index}>
                            <Grid item xs={3}>
                                <TextField
                                    select
                                    label="Address Type"
                                    name="addressType"
                                    fullWidth
                                    value={address.addressType}
                                    onChange={(e) => handleAddressChange(index, e)}
                                >
                                    {Object.values(AddressType).map((type) => (
                                        <MenuItem key={type} value={type}>
                                            {type}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    label="Address Line 1"
                                    name="addressLine1"
                                    fullWidth
                                    value={address.addressLine1}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    label="Address Line 2"
                                    name="addressLine2"
                                    fullWidth
                                    value={address.addressLine2}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    label="Address Line 3"
                                    name="addressLine3"
                                    fullWidth
                                    value={address.addressLine3}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    label="Address Line 4"
                                    name="addressLine4"
                                    fullWidth
                                    value={address.addressLine4}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={9}>
                                <TextField
                                    label="City"
                                    name="city"
                                    fullWidth
                                    value={address.city}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <TextField
                                    label="State"
                                    name="state"
                                    fullWidth
                                    value={address.state}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={6}>
                                <TextField
                                    label="ZIP Code"
                                    name="zipCode"
                                    fullWidth
                                    value={address.zipCode}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <TextField
                                    label="ZIP Code +4"
                                    name="zipCode4"
                                    fullWidth
                                    value={address.zipCode4}
                                    onChange={(e) => handleAddressChange(index, e)}
                                />
                            </Grid>
                        </Grid>
                    ))}
                    <Typography variant="h6" gutterBottom style={{marginTop: '20px'}}>
                        Phone Information
                    </Typography>
                    {companyEntry.phones?.map((phone, index) => (
                        <Grid container spacing={3} key={index}>
                            <Grid item xs={3}>
                                <TextField
                                    select
                                    label="Phone Type"
                                    name="phoneType"
                                    fullWidth
                                    value={phone.phoneType}
                                    onChange={(e) => handlePhoneChange(index, e)}
                                >
                                    {Object.values(PhoneType).map((type) => (
                                        <MenuItem key={type} value={type}>
                                            {type}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Grid>
                            <Grid item xs={4}>
                                <TextField
                                    required
                                    label="Phone Number"
                                    name="phoneNumber"
                                    fullWidth
                                    value={phone.phoneNumber}
                                    onChange={(e) => handlePhoneChange(index, e)}
                                />
                            </Grid>
                            <Grid item xs={2}>
                                <TextField
                                    label="Extension"
                                    name="extension"
                                    fullWidth
                                    value={phone.extension}
                                    onChange={(e) => handlePhoneChange(index, e)}
                                />
                            </Grid>
                        </Grid>
                    ))}
                    <StandardSubmitButton type="submit" variant="contained" color="primary">
                        Save
                    </StandardSubmitButton>
                </form>
            </Paper>
        </Container>
    );
};
