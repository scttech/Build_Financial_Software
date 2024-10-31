import {describe, it} from "@jest/globals";
import expect from "expect";
import {computeBatchTotals} from "@/app/components/ach/batches/AchBatchStatistics";
import {AchBatchEntriesResponse} from "@/app/fileDetails/[fileId]/batchDetails/[batchId]/page";
import Decimal from "decimal.js";

describe('Compute Batch Totals', () => {
        it('Has a debit for 1', () => {
            const achBatchEntriesResponse: AchBatchEntriesResponse[] = [{
                id: 'test1',
                transaction_code: 27,
                application: "Checking",
                transaction_description: "Debit",
                amount: "1.00",
                individual_name: "John Doe",
                account_number_last_4: "*********1234",
                addenda_count: 0
            }]
            const result = computeBatchTotals(achBatchEntriesResponse)
            expect(result.debit.toNumber()).toBe(new Decimal("1").toNumber())
        })

        it('Totals Debits correctly', () => {
            const achBatchEntriesResponse: AchBatchEntriesResponse[] = [{
                id: 'test1',
                transaction_code: 27,
                application: "Checking",
                transaction_description: "Debit",
                amount: "1.00",
                individual_name: "John Doe",
                account_number_last_4: "*********1234",
                addenda_count: 0
            }, {
                id: 'test2',
                transaction_code: 27,
                application: "Checking",
                transaction_description: "Debit",
                amount: "5.00",
                individual_name: "John Doe",
                account_number_last_4: "*********1234",
                addenda_count: 0
            }]
            const result = computeBatchTotals(achBatchEntriesResponse)
            expect(result.debit.toNumber()).toBe(new Decimal("6").toNumber())
        })

    }
)