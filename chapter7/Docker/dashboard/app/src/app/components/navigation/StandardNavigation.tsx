'use client';
import * as React from "react";
import TopMenuBar from "@/app/components/navigation/TopMenuBar";
import SideBarNav from "@/app/components/navigation/SideBarNav";

export default function StandardNavigation() {

    const [open, setOpen] = React.useState(true);
    const toggleDrawer = () => {
        setOpen(!open);
    };

    return (
        <>
            <TopMenuBar toggleDrawer={toggleDrawer} drawerOpen={open} />
            <SideBarNav toggleDrawer={toggleDrawer} drawerOpen={open} />
        </>
);

}
