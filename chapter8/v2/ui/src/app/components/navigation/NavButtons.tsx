import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import DashboardIcon from "@mui/icons-material/Dashboard";
import ListItemText from "@mui/material/ListItemText";
import {CloudUpload, Logout} from "@mui/icons-material";
import * as React from "react";
import {useRouter} from "next/navigation";
import {logout} from "@/app/lib/actions";

export default function MainListItems() {

    const route = useRouter();

    return (
        <>
            <ListItemButton onClick={() => route.push("/")}>
                <ListItemIcon>
                    <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
            </ListItemButton>
            <ListItemButton onClick={() => route.push("/uploads")}>
                <ListItemIcon>
                    <CloudUpload />
                </ListItemIcon>
                <ListItemText primary="Uploads" />
            </ListItemButton>
            <ListItemButton onClick={() => logout()}>
                <ListItemIcon>
                    <Logout />
                </ListItemIcon>
                <ListItemText primary="Signout" />
                </ListItemButton>
        </>
    );
}