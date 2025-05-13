import datetime
import logging
import pathlib
from tkinter import ttk

import polars as pl
import xlsxwriter

from common import NoSkuColumnsFound, call_with_progress, load_file
from common.constants import (
    HIDDEN_SKU_COLUMN,
    LOOKUP_COLUMN,
    QUANTITY_ON_HAND,
    SKU_SUBSTR,
)


def filter_dataframe(
    df: pl.DataFrame, values: list, *, name: str = None, is_null: bool = True
) -> pl.DataFrame:
    # Identify columns that contain the substring 'sku'
    columns = [col for col in df.columns if SKU_SUBSTR in col.lower()]
    if not columns:
        raise NoSkuColumnsFound(name, columns)

    # Create a new column \`__SKU__\` that captures the matched SKU
    df = df.with_columns(
        pl.coalesce(
            *[pl.when(pl.col(c).is_in(values)).then(pl.col(c)) for c in columns]
        ).alias(HIDDEN_SKU_COLUMN)
    )

    # Filter rows to include only matched SKUs or unmatched SKUs based on is_null
    # Filter rows to include only rows that did not match any SKU
    if is_null:
        return df.filter(pl.col(HIDDEN_SKU_COLUMN).is_null())
    else:
        return df.filter(pl.col(HIDDEN_SKU_COLUMN).is_not_null())


def join_inventory_restock(
    inventory_df: pl.DataFrame, restock_df: pl.DataFrame
) -> pl.DataFrame:
    # Join on "SKU"
    return inventory_df.join(
        restock_df, on=HIDDEN_SKU_COLUMN, how="left", suffix="_inv"
    )


def filter_quantity_on_hand(df: pl.DataFrame) -> pl.DataFrame:
    # Filter the DataFrame to exclude rows with days on hand less than 2
    return df.filter(
        pl.col(QUANTITY_ON_HAND).cast(pl.Int64, strict=False).fill_null(0).fill_nan(0) >= 2
    )

def main(
    restock_report_path: pathlib.Path,
    inventory_file_path: pathlib.Path,
    *,
    progress_bar: ttk.Progressbar = None,
):
    # disable polars dtype warning
    logging.getLogger("fastexcel.types.dtype").disabled = True
    restock_report = call_with_progress(load_file, progress_bar, restock_report_path)
    inventory_file = call_with_progress(load_file, progress_bar, inventory_file_path)

    skus = restock_report[LOOKUP_COLUMN].to_list()

    # Filter the inventory file to exclude SKUs present in the restock report
    filtered_inventory_df = call_with_progress(
        filter_dataframe, progress_bar, inventory_file, skus, name="Inventory"
    )

    filtered_restock_df = call_with_progress(
        filter_dataframe, progress_bar, restock_report, skus, name="Restock Report", is_null=False
    )

    # Join the filtered inventory DataFrame with the restock report
    joined_dataframe = call_with_progress(
        join_inventory_restock, progress_bar, filtered_inventory_df, filtered_restock_df
    )

    # Filter the joined DataFrame to exclude rows with days on hand less than 2
    filtered_dataframe = call_with_progress(
        filter_quantity_on_hand, progress_bar, joined_dataframe
    )

    # Remove all the joined columns
    filtered_dataframe = filtered_dataframe.select(
        [col for col in filtered_dataframe.columns if "_inv" not in col]
    ).drop(HIDDEN_SKU_COLUMN)

    # Save the output DataFrame to an Excel file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_file_path = f"output_{timestamp}.xlsx"
    print(f"Writing output to {output_file_path}")
    wb = xlsxwriter.Workbook(output_file_path)
    call_with_progress(filtered_dataframe.write_excel, progress_bar, wb)
    wb.close()
    return output_file_path
