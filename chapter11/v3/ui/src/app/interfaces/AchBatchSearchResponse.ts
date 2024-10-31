export interface AchBatchSearchResponse {
    /**
     * Unique identifier for the ACH file.
     * @title File ID
     */
    file_id: string;

    /**
     * Unique identifier for the ACH Batch Header.
     * @title Batch Header ID
     */
    batch_header_id: string;

    /**
     * The name of the ACH file.
     * @title Filename
     * @maxLength 255
     */
    filename: string;

    /**
     * The name of the individual or company for the entry.
     * @title Individual Name
     * @maxLength 22
     */
    company_name: string;

    /**
     * The total credit entry dollar amount for the batch.
     * @title Total Credit Entry Dollar Amount
     * @maxDigits 10
     * @decimalPlaces 2
     */
    total_credit_entry_dollar_amount: string;

    /**
     * The debit entry dollar amount for the batch.
     * @title Total Debit Entry Dollar Amount
     * @maxDigits 10
     * @decimalPlaces 2
     */
    total_debit_entry_dollar_amount: string;

    /**
     * The number of entry/addenda records in the batch.
     * @title Entry and Addenda Count
     * @maxDigits 10
     */
    entry_addenda_count: string;
}
