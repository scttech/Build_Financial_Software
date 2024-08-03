'use client';
import React from 'react';
import Button from '@mui/material/Button';

interface FileUploadButtonProps {
    onFileChange: (file: File) => void;
}

const FileUploadButton: React.FC<FileUploadButtonProps> = ({ onFileChange }) => {
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0] && onFileChange) {
            onFileChange(event.target.files[0]);
        }
    };

    return (
        <label htmlFor="upload-button">
            <input
                accept=".ach"
                id="upload-button"
                type="file"
                style={{ display: 'none' }}
                onChange={handleFileChange}
            />
            <Button variant="contained" component="span">
                Upload File
            </Button>
        </label>
    );
};

export default FileUploadButton;
