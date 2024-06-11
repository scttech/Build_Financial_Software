import {Box} from '@mui/material';
import {createTheme, ThemeProvider} from "@mui/material/styles";

interface ImageProps {
    base64: string;
    alt?: string;
    width?: string;
    maxWidth?: string;
}

const defaultTheme = createTheme();

export default function ImageBase64({base64, alt = 'Image', width = '100%', maxWidth='100px' }: Readonly<ImageProps>) {

    return (
        <ThemeProvider theme={defaultTheme}>
            <Box
                component="img"
                src={`${base64}`}
                alt={`${alt}`}
                sx={{
                    width: width,
                    maxWidth: maxWidth,
                }}
            />
        </ThemeProvider>
    );
}
