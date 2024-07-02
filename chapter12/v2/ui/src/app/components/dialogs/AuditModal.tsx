import React, {FC} from 'react';
import { Modal, Box, Typography, Button } from '@mui/material';
import {AuditResponse} from "@/app/interfaces/AuditResponse";
import {convertDateFormat} from "@/app/utils/DateUtils";

interface AuditModalProps {
  open: boolean;
  onClose: () => void;
  auditData: AuditResponse | null;
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

const AuditModal: FC<AuditModalProps> = ({ open, onClose, auditData }: Readonly<AuditModalProps>) => {
  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="audit-modal-title"
      aria-describedby="audit-modal-description"
    >
      <Box sx={style}>
        <Typography id="audit-modal-title" variant="h6" component="h2">
          Audit Log Details
        </Typography>
        <Box>
        <Typography id="audit-modal-description" sx={{ mt: 2 }} fontWeight={'fontWeightBold'}>
          Audit Log ID:
        </Typography>
        <Typography>{auditData?.audit_log_id}</Typography>
          </Box>
        <Typography fontWeight={'fontWeightBold'}>
          Created At:
        </Typography>
        <Typography>{auditData?.created_at ? convertDateFormat(auditData?.created_at.toString()) : 'N/A'}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          User ID:
        </Typography>
        <Typography>{auditData?.user_id}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          IP Address:
        </Typography>
        <Typography>{auditData?.ip_address}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          User Agent:
        </Typography>
        <Typography>{auditData?.user_agent}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          HTTP Request:
        </Typography>
        <Typography>{auditData?.http_request}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          HTTP Response:
        </Typography>
        <Typography>{auditData?.http_response}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          URL:
        </Typography>
        <Typography>{auditData?.url}</Typography>
        <Typography fontWeight={'fontWeightBold'}>
          Message:
        </Typography>
        <Typography>{auditData?.message}</Typography>
        <Button onClick={onClose} sx={{ mt: 2 }}>
          Close
        </Button>
      </Box>
    </Modal>
  );
};

export default AuditModal;
