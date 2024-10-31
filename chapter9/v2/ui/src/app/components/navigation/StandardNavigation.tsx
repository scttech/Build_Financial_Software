'use client';
import * as React from "react";
import TopMenuBar from "@/app/components/navigation/TopMenuBar";
import SideBarNav from "@/app/components/navigation/SideBarNav";
import {Box} from "@mui/material";

export default function StandardNavigation() {

    const [open, setOpen] = React.useState(true);
    const toggleDrawer = () => {
        setOpen(!open);
    };

    return (
        <Box sx={{ display: 'flex' }}>
            <TopMenuBar toggleDrawer={toggleDrawer} drawerOpen={open} />
            <SideBarNav toggleDrawer={toggleDrawer} drawerOpen={open} />
        </Box>
);

}
