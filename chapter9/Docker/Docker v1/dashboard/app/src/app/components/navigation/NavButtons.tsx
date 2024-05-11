import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import DashboardIcon from "@mui/icons-material/Dashboard";
import ListItemText from "@mui/material/ListItemText";
import {CloudUpload} from "@mui/icons-material";
import PeopleIcon from "@mui/icons-material/People";
import BarChartIcon from "@mui/icons-material/BarChart";
import * as React from "react";
import {useRouter} from "next/navigation";

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
            <ListItemButton onClick={() => route.push("/companies")}>
                <ListItemIcon>
                    <PeopleIcon />
                </ListItemIcon>
                <ListItemText primary="Companies" />
            </ListItemButton>
            <ListItemButton onClick={() => route.push("/reports")}>
                <ListItemIcon>
                    <BarChartIcon />
                </ListItemIcon>
                <ListItemText primary="Reports" />
            </ListItemButton>
        </>
    );
}