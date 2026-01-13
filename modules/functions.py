import argparse

def str_to_bool(v: str) -> bool:
    true_opt = ("yes", "y", "true", "t", "1")
    false_opt = ("no", "n", "false", "f", "0")

    if v.lower() in true_opt:
        return True
    elif v.lower() in false_opt:
        return False
    else:
        raise argparse.ArgumentTypeError(
            f"Boolean value excepted, evaluated from following option set: True = {true_opt}, False = {false_opt}"
        )

parser = argparse.ArgumentParser(description="Python script to run SQL queries.")

parser.add_argument(
    "-d",
    "--dev",
    type=str_to_bool,
    default=False,
    help="Run in developer mode for detailed errors.",
)

args = parser.parse_args()

def get_sql_query(default_query: str) -> str:
    multi_line_sql_query = []
    line_count = 1

    print("Enter SQL query(end final line with ';' to complete the query):\n")
    while True:
        single_line_query = input(f"{line_count}. ").strip()

        # Skip adding to list if user presses ENTER key
        if single_line_query == "":
            print("Refrain from pressing ENTER key without writing a query.")
            continue

        multi_line_sql_query.append(single_line_query)
        line_count += 1

        if single_line_query.endswith(";"):
            break

    final_query = " ".join(multi_line_sql_query)

    if final_query == ";":
        print(f"\nNo query specified. Using the default query:\n{default_query}\n")
        return default_query

    print(f"\nFinal query: {final_query}\n")
    return final_query

