import {Box} from '@mui/material';
import {createTheme, ThemeProvider} from "@mui/material/styles";

interface ImageProps {
    base64: string;
    alt?: string;
    width?: string;
    maxWidth?: string;
}

const isBase64Image = (base64: string) => {
    const regex = /^data:image\/[a-zA-Z]+;base64,/;
    if (!regex.test(base64)) {
        return '';
    } else {
        return base64;
    }
}

export default function ImageBase64({base64, alt = 'Image', width = '100%', maxWidth = '100px'}: Readonly<ImageProps>) {

    const imageSource = isBase64Image(base64);

    return (
        <Box
            component="img"
            src={imageSource}
            alt={alt}
            sx={{
                width: width,
                maxWidth: maxWidth,
            }}
        />
    );
}
