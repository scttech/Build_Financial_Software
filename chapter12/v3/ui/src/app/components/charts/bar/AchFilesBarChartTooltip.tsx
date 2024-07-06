import {formatCurrency} from "@/app/utils/CurrencyUtils";
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import Paper from "@mui/material/Paper";
import {TooltipProps} from "recharts/types/component/Tooltip";


export function AchFilesBarChartToolTip ({ active, payload, label }: TooltipProps<string, string>)  {
    if (active && payload?.length) {
        const credits = payload[0].value ?? '0.0';
        const debits = payload[1].value ?? '0.0';
        const filename: string = payload[0].payload.filename ?? '';
        return (
            <Tooltip title={<Typography>{`Value: ${label}`}</Typography>} arrow>
                <Paper sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
                    <Typography variant="h6">{filename}</Typography>
                    <Typography>Credits: {formatCurrency(Number.parseFloat(credits))}</Typography>
                    <Typography>Debits: {formatCurrency(Number.parseFloat(debits))}</Typography>
                </Paper>
            </Tooltip>
        );
    }

    return null;
}