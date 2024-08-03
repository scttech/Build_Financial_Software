import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Typography from "@mui/material/Typography";
import Badge from "@mui/material/Badge";
import NotificationsIcon from "@mui/icons-material/Notifications";
import MuiAppBar, {AppBarProps as MuiAppBarProps} from '@mui/material/AppBar';

import * as React from "react";
import {useEffect, useState} from "react";
import {styled} from "@mui/material/styles";
import {DRAWER_WIDTH} from "@/app/constants/Constants";

interface AppBarProps extends MuiAppBarProps {
    open?: boolean;
}

interface TopMenuBarProps {
    toggleDrawer(): void;
    drawerOpen: boolean;
}

const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})<AppBarProps>(({ theme, open }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
        marginLeft: DRAWER_WIDTH,
        width: `calc(100% - ${DRAWER_WIDTH}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    }),
}));

export default function TopMenuBar({toggleDrawer, drawerOpen}: TopMenuBarProps) {

    const [open, setOpen] = useState(drawerOpen);

    useEffect(() => {
        setOpen(drawerOpen);
    }, [drawerOpen]);

    return (
    <AppBar position="absolute" open={open}>
        <Toolbar
            sx={{
                pr: '24px', // keep right padding when drawer closed
            }}>
            <IconButton edge="start" color="inherit" aria-label="open drawer" onClick={toggleDrawer}
                sx={{
                    marginRight: '36px',
                    ...(open && { display: 'none' }),
                }}>
                <MenuIcon />
            </IconButton>
            <Typography component="h1" variant="h6" color="inherit" noWrap sx={{ flexGrow: 1 }}>
                Dashboard
            </Typography>
            <IconButton color="inherit">
                <Badge badgeContent={4} color="secondary">
                    <NotificationsIcon />
                </Badge>
            </IconButton>
        </Toolbar>
    </AppBar>
    );
}