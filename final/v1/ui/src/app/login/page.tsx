'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {authenticate} from "@/app/lib/actions";
import { useFormState } from 'react-dom';
import { useLayoutEffect, useState} from "react";
import {useRouter} from "next/navigation";
import AlertMessage from "@/app/components/dialogs/AlertMessage";
import Tooltip from "@mui/material/Tooltip";
import StandardNavigation from "@/app/components/navigation/StandardNavigation";


function Copyright(props: any) {
    return (
        <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/">
                Futuristic Fintech
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function SignIn() {
    const [errorMessage, dispatch] = useFormState(authenticate, undefined);
    const [showErrorDialog, setShowErrorDialog] = useState<boolean>(false);
    const route = useRouter();

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {

        event.preventDefault();
        const formData = new FormData(event.currentTarget);

        dispatch(formData);
    };

    useLayoutEffect(() => {
        if (errorMessage && errorMessage !== 'success') {
            setShowErrorDialog(true);
        } else if (errorMessage === 'success') {
            route.push('/uploads');
            setShowErrorDialog(false);
        }
    }, [errorMessage, route]);

    return (
        <ThemeProvider theme={defaultTheme}>
            <Box sx={{ display: 'flex' }}>
                <CssBaseline />
                <StandardNavigation />
            <Container component="main" maxWidth="xs">
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >

                    {showErrorDialog && <AlertMessage
                        open={showErrorDialog}
                        setOpen={() => setShowErrorDialog(false)}
                        title={"Error Signing In"}
                        message={"Either your email or password is incorrect. Please try again."}
                    />}
                    <Box
                    component={"img"}
                    sx={{
                        height: 233, // You can adjust the height
                        width: 350, // and width as needed
                        maxHeight: { xs: 250, md: 250 },
                        maxWidth: { xs: 250, md: 250 },
                    }}
                    alt="Company Logo"
                    src="/images/logo-light.png"
                    />
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <Tooltip title={"Use admin@futuristicfintech.com and password"} placement={"top"}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                        />
                        </Tooltip>
                        <Tooltip title={"Password is just 'password'"} placement={"top"}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                        />
                            </Tooltip>
                        <Button
                            type="submit"
                            fullWidth
                            variant="outlined"
                            name="signin"
                            id="signin"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign In
                        </Button>
                    </Box>
                </Box>
                <Copyright sx={{ mt: 4, mb: 4 }} />
            </Container>
                </Box>
        </ThemeProvider>
    );
}