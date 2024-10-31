import React, {FC} from 'react';
import {Box, Button, Modal, Typography} from '@mui/material';
import {AchExceptionDetailsResponse} from "@/app/interfaces/AchExceptionDetailsResponse";

interface ExceptionModalProps {
  open: boolean;
  onClose: () => void;
  exceptionData: AchExceptionDetailsResponse | null;
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '50%',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

const ExceptionsModal: FC<ExceptionModalProps> = ({ open, onClose, exceptionData }: Readonly<ExceptionModalProps>) => {
  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="audit-modal-title"
      aria-describedby="audit-modal-description"
    >
      <Box sx={style}>
        <Typography id="audit-modal-title" variant="h6" component="h2">
          Exception Details
        </Typography>
        { exceptionData?.company_name !== '' &&
            <Box>
        <Typography id="audit-modal-description" sx={{ mt: 2 }} fontWeight={'fontWeightBold'}>
          Company Name:
        </Typography>
        <Typography>{exceptionData?.company_name}</Typography>
        </Box>
        }
        <Typography fontWeight={'fontWeightBold'}>
          Unparsed Record:
        </Typography>
        <Typography sx={{ fontSize: 'small' }}>{exceptionData?.unparsed_record}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          Error Code:
        </Typography>
        <Typography>{exceptionData?.exception_code}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          Description:
        </Typography>
        <Typography>{exceptionData?.description}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          Recovery Action:
        </Typography>
        <Typography>{exceptionData?.recovery_option ?? 'None Provided'}</Typography>
        <Button onClick={onClose} sx={{ mt: 2 }}>
          Close
        </Button>
      </Box>
    </Modal>
  );
};

export default ExceptionsModal;
