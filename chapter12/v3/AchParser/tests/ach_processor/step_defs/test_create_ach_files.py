from datetime import datetime
from pathlib import Path
from random import randint, choice

import pytest
from pytest_bdd import scenarios, given, parsers, when, then

# Load scenarios
scenarios("../features/ach_file_creation.feature")
scenarios("../features/ach_file_exceptions.feature")

# Get the directory of our file
current_file_dir = Path(__file__).resolve().parent


def get_absolute_path(relative_path):
    return current_file_dir / relative_path


def create_file_header(setup_info):
    yymmdd = datetime.now().strftime("%y%m%d")
    hhmm = datetime.now().strftime("%H%M")
    return f"101{setup_info['immediate_destination']}{setup_info['immediate_origin']}{yymmdd}{hhmm}{setup_info['file_id']}{setup_info.get('record_size', '094')}{setup_info.get('blocking_factor', '10')}1{setup_info.get('DEST_NAME','DEST NAME              ')}{setup_info.get('ORIGIN_NAME','ORIGIN NAME            ')}XXXXXXXX\n"


def create_batch_header(setup_info, batch_number):
    today_yymmdd = str(datetime.today().strftime("%y%m%d"))
    day_of_year = str(datetime.today().timetuple().tm_yday).rjust(3, "0")
    batch_number = str(batch_number).rjust(7, "0")
    if setup_info["standard_entry_class"] == "IAT":
        batch_header = (
            f"5{setup_info['service_class_code']}"
            f"                "  # IAT Indicator
            f"FF"  # Foreign Exchange Indicator
            f"3"  # Foreign Exchange Reference Indicator
            "               "  # Foreign Exchange Reference
            "US"  # ISO Destination Country Code
            f"{setup_info['company_id']}"  # Originator Identification
            f"{setup_info["standard_entry_class"]}"  # Standard Entry Class Code
            "GIFT      "  # Company Entry Description
            "USD"  # ISO Originating Currency Code
            "USD"  # ISO Destination Currency Code
            f"{setup_info.get('effective_entry_date',today_yymmdd)}"  # Effective Entry Date
            f"{setup_info.get('settlement_date',day_of_year)}"  # Settlement Date
            f"{setup_info.get('originator_status_code','1')}"  # Originator Status Code
            f"{setup_info.get('odfi','06100001')}"  # Originating DFI Identification
            f"{setup_info.get('batch_number', batch_number)}\n"
        )
    else:
        batch_header = (
            f"5{setup_info['service_class_code']}"
            f"{setup_info['company_name']}"
            f"{setup_info.get('company_discretionary_data','DiscretionaryData   ')}"
            f"{setup_info['company_id']}"
            f"{setup_info['standard_entry_class']}"
            f"{setup_info.get('company_entry_description','Comp desc ')}"
            f"{setup_info.get('company_descriptive_date',today_yymmdd)}"
            f"{setup_info.get('effective_entry_date',today_yymmdd)}"
            f"{setup_info.get('settlement_date',day_of_year)}"
            f"{setup_info.get('originator_status_code','1')}"
            f"{setup_info.get('odfi','06100001')}"
            f"{setup_info.get('batch_number', batch_number)}\n"
        )
    return batch_header


def create_file_control(
    setup_info, file_control_entry_hash, total_debits_in_file, total_credits_in_file
):
    total_credits_in_file = str(total_credits_in_file).rjust(12, "0")
    total_debits_in_file = str(total_debits_in_file).rjust(12, "0")
    file_control_entry_hash = str(file_control_entry_hash).rjust(10, "0")
    batch_count = str(setup_info["batch_count"]).rjust(6, "0")
    entry_count = str(setup_info["entry_count"] * setup_info["batch_count"]).rjust(
        8, "0"
    )
    return (
        f"9{setup_info.get('file_control_batch_count', batch_count)}"
        f"{setup_info.get('file_control_block_count', '000010')}"
        f"{setup_info.get('file_control_entry_count', entry_count)}"
        f"{setup_info.get('file_control_entry_hash', file_control_entry_hash)}"
        f"{setup_info.get('file_control_total_debits', total_debits_in_file)}"
        f"{setup_info.get('file_control_total_credits', total_credits_in_file)}"
    ).ljust(94, " ")


def calculate_routing_number_check_digit(routing_number: str):
    routing_number = routing_number.rjust(8, "0")

    if len(routing_number) != 8:
        raise ValueError("Routing number must have exactly 8 digits")

    # Convert string to a list of integers
    digits = [int(d) for d in routing_number]

    # Multiply and sum
    total = (
        digits[0] * 3
        + digits[1] * 7
        + digits[2] * 1
        + digits[3] * 3
        + digits[4] * 7
        + digits[5] * 1
        + digits[6] * 3
        + digits[7] * 7
    )

    # Final calculation
    check_digit = (10 - (total % 10)) % 10

    return check_digit


def create_iat_entries_and_addenda(
    setup_info, tran_code, rdfi, check_digit, amount, individual_name, trace_number
):
    # Create the IAT entry
    entries = (
        "6"  # Record Type Code
        f"{tran_code}"  # Transaction Code
        f"{setup_info.get('rdfi', rdfi)}{setup_info.get('check_digit', check_digit)}"
        f"{setup_info.get('iat_number_of_addenda', '0007')}"
        "             "  # Reserved
        f"{setup_info.get('amount', amount)}"
        f"{setup_info.get('account_number', '123'.ljust(35, ' '))}"
        "  "  # Reserved
        " "  # Gateway Operator OFAC Screening Indicator
        " "  # Secondary OFAC Screening Indicator
        "1"  # Addenda Record Indicator
        f"{setup_info.get('trace_number', trace_number)}\n"
    )
    # Create Addenda 710
    entries += (
        "7"  # Record Type Code
        "10"  # Addenda Type Code
        "WEB"  # Transaction Type Code
        f"{setup_info.get('amount', amount).rjust(18, '0')}"
        "                      "  # Foreign Trace Number
        f"{individual_name.ljust(35, ' ')}"  # Receiving Company Name/Individual Name
        "      "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )
    # Create Addenda 711
    entries += (
        "7"  # Record Type Code
        "11"  # Addenda Type Code
        "ELENA SANTIAGO                     "  # Originator Name
        "CALLE FICTICIA 123                 "  # Originator Address
        "              "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )
    # Create Addenda 712
    entries += (
        "7"  # Record Type Code
        "12"  # Addenda Type Code
        "BILBAO*BIZKAIA\\                    "  # Originator City & State/Province
        "ES*48001\\                          "  # Originator Country and Postal Code
        "              "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )
    # Create Addenda 713
    # 713IBERIA GLOBAL BANK                 011234567890                        US           3172961
    entries += (
        "7"  # Record Type Code
        "13"  # Addenda Type Code
        "IBERIA GLOBAL BANK                 "  # Originating DFI Name
        "01"  # Originating DFI Identification Number Qualifier
        f"{setup_info.get('odfi','06100001').ljust(34, ' ')}"  # Originating DFI Identification
        "US "  # Originating DFI Country Code
        "          "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )

    # Create Addenda 714
    # 714METROPOLIS TRUST BANK              01247611456
    entries += (
        "7"  # Record Type Code
        "14"  # Addenda Type Code
        f"{setup_info.get('DEST_NAME', 'DEST NAME').ljust(35, ' ')}"  # Receiving DFI Name
        "01"  # Receiving DFI Identification Number Qualifier
        "247611456                         "  # Receiving DFI Identification
        "US "  # Receiving DFI Branch Country Code
        "          "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )

    # Create Addenda 715
    # 715               9999 NORTH BROADWAY                                                  3172961
    entries += (
        "7"  # Record Type Code
        "15"  # Addenda Type Code
        "               "  # Receiver Identification Number
        "9999 NORTH BROADWAY                "  # Receiver Street Address
        "                                  "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )

    # Create Addenda 716
    # 716NEW YORK*NY\                       US*10001\                                        3172961
    entries += (
        "7"  # Record Type Code
        "16"  # Addenda Type Code
        "NEW YORK*NY\                       "  # Receiver City & State/Province
        "US*10001\                          "  # Receiver Country and Postal Code
        "              "  # Reserved
        f"{setup_info.get('trace_number', trace_number)[-7:]}\n"  # Right most 7 digits of trace number
    )

    return entries


def create_entries(setup_info, batch_number):
    entries = ""
    total_credit_amount = 0
    total_debit_amount = 0
    batch_entry_hash = 0
    for i in range(setup_info["entry_count"]):
        setup_info["FILE_ENTRY_COUNT"] += 1
        trace_number = str(batch_number).rjust(8, "0") + str(
            setup_info["FILE_ENTRY_COUNT"]
        ).rjust(7, "0")
        amount = str(
            randint(setup_info["low_amount"], setup_info["high_amount"])
        ).rjust(10, "0")
        rdfi = choice(setup_info.get("rdfi", ["26708413"]))
        check_digit = calculate_routing_number_check_digit(rdfi)
        batch_entry_hash += int(rdfi)
        batch_entry_hash = int(str(batch_entry_hash)[-10:])
        tran_code = choice(setup_info["transaction_code"])
        individual_name = choice(setup_info["individual_names"])
        addenda_indicator = "0"
        if tran_code == "22":
            total_credit_amount += int(amount)
        else:
            total_debit_amount += int(amount)
        if setup_info["standard_entry_class"] == "IAT":
            entries += create_iat_entries_and_addenda(
                setup_info,
                tran_code,
                rdfi,
                check_digit,
                amount,
                individual_name,
                trace_number,
            )
        else:
            entries += (
                f"6{tran_code}"
                f"{setup_info.get('rdfi', rdfi)}{setup_info.get('check_digit', check_digit)}"
                f"{setup_info.get('account_number', '123              ')}"
                f"{setup_info.get('amount', amount)}"
                f"{setup_info.get('individual_identification_number', '01223344       ')}"
                f"{setup_info.get('individual_name', individual_name)}"
                f"{setup_info.get('discretionary_data', 'LC')}"
                f"{setup_info.get('addenda_record_indicator', addenda_indicator)}"
                f"{setup_info.get('trace_number', trace_number)}\n"
            )

    return {
        "total_credit_amount": total_credit_amount,
        "total_debit_amount": total_debit_amount,
        "batch_entry_hash": batch_entry_hash,
        "entries": entries,
    }


def create_batch_trailer(
    setup_info, batch_number, total_debit_amount, total_credit_amount
):
    return f"8{setup_info['service_class_code']}{str(setup_info['entry_count']).rjust(6, '0')}0033003300{str(total_debit_amount).rjust(12, '0')}{str(total_credit_amount).rjust(12, '0')}{setup_info['company_id']}                         {setup_info.get('odfi','06100001')}{str(batch_number).rjust(7, '0')}\n"


@pytest.fixture
def setup_info():
    return {}


@given(parsers.parse('I want to create an ACH file named "{filename}"'))
def given_i_want_to_create_an_ach_file(setup_info, filename):
    setup_info["filename"] = filename
    setup_info["file_id"] = "A"


@given(
    parsers.parse(
        'I want to create an ACH file named "{filename}" with a File ID of "{file_id}"'
    )
)
def given_i_want_to_create_an_ach_file_and_file_id(setup_info, filename, file_id):
    setup_info["filename"] = filename
    setup_info["file_id"] = file_id


@given(
    parsers.parse(
        'I want to have an immediate destination of "{immediate_destination}"'
    )
)
def set_immediate_destination(setup_info, immediate_destination):
    setup_info["immediate_destination"] = immediate_destination.rjust(10, " ")


@given(
    parsers.parse(
        'I want to have an immediate destination of "{immediate_destination}" with a destination name of "{destination_name}"'
    )
)
def set_immediate_destination_and_name(
    setup_info, immediate_destination, destination_name
):
    setup_info["immediate_destination"] = immediate_destination.rjust(10, " ")
    setup_info["DEST_NAME"] = destination_name.ljust(23, " ")


@given(parsers.parse('I want to have an immediate origin of "{immediate_origin}"'))
def set_immediate_origin(setup_info, immediate_origin):
    setup_info["immediate_origin"] = immediate_origin.rjust(10, " ")


@given(
    parsers.parse(
        'I want to have an immediate origin of "{immediate_origin}" with an origin name of "{origin_name}"'
    )
)
def set_immediate_origin(setup_info, immediate_origin, origin_name):
    setup_info["immediate_origin"] = immediate_origin.rjust(10, " ")
    setup_info["ORIGIN_NAME"] = origin_name.ljust(23, " ")


@given(
    parsers.parse(
        "I want to have {batch_count:d} batch with ACH credits only and a "
        'standard entry class code of "{standard_entry_class}"'
    )
)
def set_number_of_credit_batches_to_create(
    setup_info, batch_count, standard_entry_class
):
    setup_info["batch_count"] = int(batch_count)
    setup_info["service_class_code"] = "220"
    setup_info["transaction_code"] = ["22"]
    setup_info["standard_entry_class"] = standard_entry_class


@given(
    parsers.parse(
        "I want to have {batch_count:d} batch with ACH debits only and a "
        'standard entry class code of "{standard_entry_class}"'
    )
)
def set_number_of_debit_batches_to_create(
    setup_info, batch_count, standard_entry_class
):
    setup_info["batch_count"] = int(batch_count)
    setup_info["service_class_code"] = "225"
    setup_info["transaction_code"] = ["27"]
    setup_info["standard_entry_class"] = standard_entry_class


@given(
    parsers.parse(
        "I want to have {batch_count:d} batch with ACH credits and debits and a "
        'standard entry class code of "{standard_entry_class}"'
    )
)
def set_number_of_mixed_batches_to_create(
    setup_info, batch_count, standard_entry_class
):
    setup_info["batch_count"] = int(batch_count)
    setup_info["service_class_code"] = "200"
    setup_info["transaction_code"] = ["22", "27"]
    setup_info["standard_entry_class"] = standard_entry_class


@given(
    parsers.parse(
        "I want {entry_count:d} entries per batch with random amounts between {low_amount:d} and {high_amount:d}"
    )
)
def set_entry_count_and_amounts(setup_info, entry_count, low_amount, high_amount):
    setup_info["entry_count"] = entry_count
    setup_info["low_amount"] = low_amount
    setup_info["high_amount"] = high_amount


@given(
    parsers.parse(
        'I want to have company name "{company_name}" and company id "{company_id}"'
    )
)
def set_company_name(setup_info, company_name, company_id):
    setup_info["company_name"] = company_name[:16].ljust(16, " ")
    setup_info["company_id"] = company_id.ljust(10, " ")


@when("my ACH is created")
def create_ach_file(setup_info):
    total_debits_in_file = 0
    total_credits_in_file = 0
    file_control_entry_hash = 0
    setup_info["FILE_ENTRY_COUNT"] = 0
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    with open(absolute_path, "w", encoding="utf8") as f:
        f.write(create_file_header(setup_info))
        for batch_number in range(1, setup_info["batch_count"] + 1):
            f.write(create_batch_header(setup_info, batch_number))
            entry_results = create_entries(setup_info, batch_number)
            total_debits_in_file += entry_results["total_debit_amount"]
            total_credits_in_file += entry_results["total_credit_amount"]
            file_control_entry_hash += int(entry_results["batch_entry_hash"])
            file_control_entry_hash = int(str(file_control_entry_hash)[-10:])
            f.write(entry_results["entries"])
            f.write(
                create_batch_trailer(
                    setup_info,
                    batch_number,
                    entry_results["total_debit_amount"],
                    entry_results["total_credit_amount"],
                )
            )
        # Write the final record out
        f.write(
            create_file_control(
                setup_info,
                file_control_entry_hash,
                total_debits_in_file,
                total_credits_in_file,
            )
        )


@then(parsers.parse('I should have a file named "{expected_file_name}"'))
def validate_file_exists(expected_file_name):
    file_path = (
        current_file_dir / Path(f"ach_processor/output/{expected_file_name}").resolve()
    )
    if not file_path.exists():
        raise AssertionError(f"File {file_path} does not exist")


@then("I should have a file of the same name")
def validate_file_exists_with_same_name(setup_info):
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    if not absolute_path.exists():
        raise AssertionError(f"File {absolute_path} does not exist")


@then(parsers.parse("there should be {expected_batch_count:d} batch in the file"))
def validate_batch_count(setup_info, expected_batch_count):
    count = 0
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    with open(absolute_path, "r", encoding="utf8") as f:
        for line in f:
            if line.startswith("5"):
                count += 1
    assert (
        count == expected_batch_count
    ), f"Expected {expected_batch_count}, but got {count}"


@then(parsers.parse("there should be {expected_entry_count:d} entries in the file"))
def validate_entry_count(setup_info, expected_entry_count):
    count = 0
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    with open(absolute_path, "r", encoding="utf8") as f:
        for line in f:
            if line.startswith("6"):
                count += 1
    assert (
        count == expected_entry_count
    ), f"Expected {expected_entry_count}, but got {count}"


@given(parsers.parse('I want to use individual names of "{individual_names}"'))
def set_individual_names(setup_info, individual_names):
    setup_info["individual_names"] = [
        name.strip().ljust(22, " ") for name in individual_names.split(",")
    ]


@given("I want to have individual names with an invalid length")
def individual_name_length(setup_info):
    updated_names = []
    for name in setup_info["individual_names"]:
        random_number = randint(1, 21)
        updated_names.append(name[:random_number])
    setup_info["individual_names"] = updated_names


@then(
    parsers.parse(
        'there should be a "{expected_file_id}" in the File ID field of the file header'
    )
)
def validate_file_id(setup_info, expected_file_id):
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    with open(absolute_path, "r", encoding="utf8") as f:
        for line in f:
            if line.startswith("1") and line[33:34] == expected_file_id:
                return
    raise ValueError(
        f"Expected '{expected_file_id}' in the File ID field, but it was not found"
    )


@given(parsers.parse('I want to override the field "{field_name}" to be "{new_value}"'))
def override_field_with_value(setup_info, field_name, new_value):
    setup_info[field_name] = new_value


@then(
    parsers.parse(
        'there should be a "{expected_blocking_factor}" in the blocking factor field of the file header'
    )
)
def validate_blocking_factor(setup_info, expected_blocking_factor):
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    with open(absolute_path, "r", encoding="utf8") as f:
        for line in f:
            if line.startswith("1") and line[37:39] == expected_blocking_factor:
                return
    raise ValueError(
        f"Expected '{expected_blocking_factor}' in the blocking factor field, but it was not found"
    )


@then(
    parsers.parse(
        'there should be a "{expected_value}" in the record type {record_type:d} in field '
        "starting at {start:d} and ending at {end:d}"
    )
)
def validate_field(setup_info, expected_value, record_type, start, end):
    absolute_path = get_absolute_path(Path(f"../output/{setup_info['filename']}"))
    with open(absolute_path, "r", encoding="utf8") as f:
        for line in f:
            if line.startswith(f"{record_type}") and line[start:end] == expected_value:
                return
    raise ValueError(
        f"Expected '{expected_value}' in the blocking factor field, but it was not found"
    )
