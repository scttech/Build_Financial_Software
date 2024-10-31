from datetime import datetime
from pathlib import Path
from random import randint, choice

import pytest
from pytest_bdd import scenarios, given, parsers, when, then

# Load scenarios
scenarios("../features/ach_file_creation.feature")


def create_file_header(setup_info):
    yymmdd = datetime.now().strftime("%y%m%d")
    hhmm = datetime.now().strftime("%H%M")
    return f"101{setup_info['immediate_destination']}{setup_info['immediate_origin']}{yymmdd}{hhmm}A094101DEST NAME              ORIGIN NAME            XXXXXXXX\n"


def create_batch_header(setup_info, batch_number):
    return f"5{setup_info['service_class_code']}{setup_info['company_name']}DiscretionaryData   {setup_info['company_id']}{setup_info['standard_entry_class']}Comp desc 021623230216047106100001{str(batch_number).rjust(7,'0')}\n"


def create_file_control(setup_info, total_debits_in_file, total_credits_in_file):
    total_credits_in_file = str(total_credits_in_file).rjust(12, "0")
    total_debits_in_file = str(total_debits_in_file).rjust(12, "0")
    batch_count = str(setup_info["batch_count"]).rjust(6, "0")
    entry_count = str(setup_info["entry_count"] * setup_info["batch_count"]).rjust(
        8, "0"
    )
    return f"9{batch_count}000010{entry_count}0198019800{total_debits_in_file}{total_credits_in_file}                                       "


def create_entries(setup_info, batch_number):
    entries = ""
    total_credit_amount = 0
    total_debit_amount = 0
    for i in range(setup_info["entry_count"]):
        trace_number = str(batch_number).rjust(7, "0") + str(i + 1).rjust(8, "0")
        amount = str(
            randint(setup_info["low_amount"], setup_info["high_amount"])
        ).rjust(10, "0")
        tran_code = choice(setup_info["transaction_code"])
        individual_name = choice(setup_info["individual_names"])
        if tran_code == "22":
            total_credit_amount += int(amount)
        else:
            total_debit_amount += int(amount)
        entries += f"6{tran_code}267084131123              {amount}01223344       {individual_name}LC0{trace_number}\n"

    return {
        "total_credit_amount": total_credit_amount,
        "total_debit_amount": total_debit_amount,
        "entries": entries,
    }


def create_batch_trailer(
    setup_info, batch_number, total_debit_amount, total_credit_amount
):
    return f"8{setup_info['service_class_code']}{str(setup_info['entry_count']).rjust(6,'0')}0033003300{str(total_debit_amount).rjust(12, '0')}{str(total_credit_amount).rjust(12,'0')}{setup_info['company_id']}                         06100001{str(batch_number).rjust(7,'0')}\n"


@pytest.fixture
def setup_info():
    return {}


@given(parsers.re(r'I want to create an ACH file named "(?P<filename>.*)"'))
def given_i_want_to_create_an_ach_file(setup_info, filename):
    setup_info["filename"] = filename


@given(
    parsers.re(
        r'I want to have an immediate destination of "(?P<immediate_destination>.*)"'
    )
)
def set_immediate_destination(setup_info, immediate_destination):
    setup_info["immediate_destination"] = immediate_destination.rjust(10, " ")


@given(parsers.re(r'I want to have an immediate origin of "(?P<immediate_origin>.*)"'))
def set_immediate_origin(setup_info, immediate_origin):
    setup_info["immediate_origin"] = immediate_origin.rjust(10, " ")


@given(
    parsers.re(
        r'I want to have (?P<batch_count>\d+) batch with ACH credits only and a standard entry class code of "(?P<standard_entry_class>.*)"'
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
    parsers.re(
        r'I want to have (?P<batch_count>\d+) batch with ACH debits only and a standard entry class code of "(?P<standard_entry_class>.*)"'
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
    parsers.re(
        r'I want to have (?P<batch_count>\d+) batch with ACH credits and debits and a standard entry class code of "(?P<standard_entry_class>.*)"'
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
    parsers.re(
        'I want to have company name "(?P<company_name>.*)" and company id "(?P<company_id>.*)"'
    )
)
def set_company_name(setup_info, company_name, company_id):
    setup_info["company_name"] = company_name.ljust(16, " ")
    setup_info["company_id"] = company_id.ljust(10, " ")


@when("my ACH is created")
def create_ach_file(setup_info):
    total_debits_in_file = 0
    total_credits_in_file = 0
    with open(f'../output/{setup_info["filename"]}', "w", encoding="utf8") as f:
        f.write(create_file_header(setup_info))
        for batch_number in range(1, setup_info["batch_count"] + 1):
            f.write(create_batch_header(setup_info, batch_number))
            entry_results = create_entries(setup_info, batch_number)
            total_debits_in_file += entry_results["total_debit_amount"]
            total_credits_in_file += entry_results["total_credit_amount"]
            f.write(entry_results["entries"])
            f.write(
                create_batch_trailer(
                    setup_info,
                    batch_number,
                    entry_results["total_debit_amount"],
                    entry_results["total_credit_amount"],
                )
            )
        f.write(
            create_file_control(setup_info, total_debits_in_file, total_credits_in_file)
        )


@then(parsers.re('I should have a file named "(?P<expected_file_name>.*)"'))
def validate_file_exists(expected_file_name):
    file_path = Path(f"../output/{expected_file_name}")
    if not file_path.exists():
        raise AssertionError(f"File {file_path} does not exist")


@then(parsers.parse("there should be {expected_batch_count:d} batch in the file"))
def validate_batch_count(setup_info, expected_batch_count):
    count = 0
    with open(f"../output/{setup_info['filename']}", "r", encoding="utf8") as f:
        for line in f:
            if line.startswith("5"):
                count += 1
    assert (
        count == expected_batch_count
    ), f"Expected {expected_batch_count}, but got {count}"


@then(parsers.parse("there should be {expected_entry_count:d} entries in the file"))
def validate_entry_count(setup_info, expected_entry_count):
    count = 0
    with open(f"../output/{setup_info['filename']}", "r", encoding="utf8") as f:
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
