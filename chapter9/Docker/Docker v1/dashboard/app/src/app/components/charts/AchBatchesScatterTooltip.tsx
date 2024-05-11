import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import Paper from "@mui/material/Paper";
import {TooltipProps} from "recharts/types/component/Tooltip";


export function AchBatchesScatterTooltip ({ active, payload, label }: TooltipProps<string, string>)  {
    if (active && payload && payload.length) {
        const value = payload[1].value ?? '0.0';
        return (
            <Tooltip title={<Typography>{`Value: ${label}`}</Typography>} arrow>
                <Paper sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
                    <Typography variant="h6">Total Debits and Credits</Typography>
                    {formatCurrency(Number.parseFloat(value))}
                </Paper>
            </Tooltip>
        );
    }

    return null;
}