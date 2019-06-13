from collections import namedtuple
from DTItool.mongo_model import db

Position = namedtuple('Position', 'row column')


def append_score(workbook, score_dict=None, top_x=10):
    default_sheet = workbook.active
    new_column_name = "appended top10"
    row_start = 1
    row_end = len(list(default_sheet))
    column_start = 0
    column_end = len(list(default_sheet[1]))

    protein_id_position = get_field_column_position(default_sheet, 'protein_id')
    # default_sheet.set_column(protein_id_position.column, protein_id_position.column, 100)
    default_sheet.column_dimensions['5'].width = 100
    print('protein_id_position', protein_id_position)
    dtinet_top10_scores = []
    neodti_top10_scores = []
    for row in default_sheet.iter_rows():
        protein_id = row[protein_id_position.column].value
        db.get_scores_by_protein_id(protein_id)

def get_field_column_position(sheet, field_name):
    field_row = sheet[1]
    for index, field in enumerate(list(field_row)):
        print(field.value)
        if field.value == field_name:
            # 1 is row
            return Position(row=index, column=1)

