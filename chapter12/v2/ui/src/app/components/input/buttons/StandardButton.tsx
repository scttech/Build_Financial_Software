// components/StyledButton.tsx
import { Button } from '@mui/material';
import { styled } from '@mui/system';

const StyledButton = styled(Button)({
  marginTop: '20px',
  color: 'black', // Default text color
  '&:hover': {
    color: 'white', // Text color on hover
  },
});

export default StyledButton;
