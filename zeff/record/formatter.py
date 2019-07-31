"""Zeff CLI record formatter."""
__docformat__ = "reStructuredText en"


import sys
import itertools
import textwrap


def format_record_restructuredtext(
    record,
    out=sys.stdout,
    structured_sort=lambda k: k.name,
    unstructured_sort=lambda k: k.group_by if k.group_by is not None else "",
):
    """Convert a record to a reStructuedText document.

    :param record: Record to format.

    :param out: A file type object to write the record in. Default `stdout`.

    :param structured_sort: A function of one argument that will be
        used to sort the structured data items. The default is to
        sort by the name of the item.

    :param unstructured_sort: A function of one argument that will be
        used to sort the unstructured data items. The default is to
        sort on `group_by`.
    """

    def print_table_header(columns):
        for name, width in columns:
            print(f"+-{'-'*width}-", end="", file=out)
        print("+", file=out)

        for name, width in columns:
            print(f"| {name}{' '*(width-len(name))} ", end="", file=out)
        print("|", file=out)

        for name, width in columns:
            print(f"+={'='*width}=", end="", file=out)
        print("+", file=out)

    def print_table_entry(data, columns):
        cstrs = [(str(d), w) for d, (n, w) in zip(data, columns)]
        cstrs = [textwrap.wrap(s, w) for s, w in cstrs]
        for rstrs in itertools.zip_longest(*cstrs):
            for index, vstr in enumerate(rstrs):
                width = columns[index][1]
                if vstr is None:
                    print(f"| {' '*width} ", end="", file=out)
                else:
                    print(f"| {vstr:<{width}} ", end="", file=out)
            print("|", file=out)
        for _, width in columns:
            print(f"+-{'-'*width}-", end="", file=out)
        print("+", file=out)

    def print_structured_item_table(structured_data):
        columns = compute_column_widths(
            structured_data.structured_data_items,
            ["name", "data_type", "target", "value"],
            [16, 8, 6, 32],
        )
        print_table_header(columns)

        data_items = list(structured_data.structured_data_items)
        data_items.sort(key=structured_sort)
        for sdi in data_items:
            data = [sdi.name, sdi.data_type.name, sdi.target.name, sdi.value]
            print_table_entry(data, columns)

    def print_unstructured_item_table(unstructured_data):
        columns = compute_column_widths(
            unstructured_data.unstructured_data_items,
            ["file_type", "group_by", "data", "accessible"],
            [8, 8, 8, 16],
        )
        print_table_header(columns)

        data_items = list(unstructured_data.unstructured_data_items)
        data_items.sort(key=unstructured_sort)
        for udi in data_items:
            data = [udi.file_type, udi.group_by, udi.data, udi.accessible]
            print_table_entry(data, columns)

    def compute_column_widths(items, names, mins):
        widths = list(mins)
        for item in items:
            for index, width in enumerate(widths):
                value = getattr(item, names[index])
                width = max(len(str(value)), width)
                widths[index] = width
        if sum(widths) + len(widths) * 3 + 1 > 132:
            reduce = sum(widths) + len(widths) * 3 + 1 - 132
            maxcol = max(widths)
            widths[widths.index(maxcol)] = maxcol - reduce
        return list(zip(names, widths))

    print("=" * len(str(record)))
    print(record)
    print("=" * len(str(record)))

    print()
    print("Structured Data")
    print("===============")
    print_structured_item_table(record.structured_data)

    print(file=out)
    print("Unstructured Data", file=out)
    print("=================", file=out)
    print_unstructured_item_table(record.unstructured_data)
