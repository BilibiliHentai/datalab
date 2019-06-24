import xlsxwriter
import io


def excel_both(drug_name, dtinet_score_entries, neodti_score_entries):
    output = io.BytesIO()
    f = xlsxwriter.Workbook(output, {'in_memory': True})

    dtinet_sheet = f.add_worksheet('DTInet')
    keys = [
        'Protein id', 'Protein name', 'DTInet score',
        'DTInet ranking', 'Sequence'
    ]
    display_keys = [
        'Drug name', 'Sequence', 'Uniprot', 'gene name', 'Label'
    ]
    for i, j in enumerate(display_keys):
        dtinet_sheet.write(0, i, j)
    dtinet_sheet.set_column(0, 3, 15)
    for i, d in enumerate(dtinet_score_entries):
        dtinet_sheet.write(i+1, 0, drug_name)
        dtinet_sheet.write(i+1, 1, d['smiles'])
        dtinet_sheet.write(i+1, 2, d['protein_id'])
        dtinet_sheet.write(i+1, 3, d['protein_name'])
        dtinet_sheet.write(i+1, 4, d['label'])
    neodti_sheet = f.add_worksheet('NeoDTI')

    for i, j in enumerate(display_keys):
        neodti_sheet.write(0, i, j)
    neodti_sheet.set_column(0, 3, 15)
    neodti_sheet.set_column(4, 4, 1000)
    for i, d in enumerate(dtinet_score_entries):
        dtinet_sheet.write(i+1, 0, drug_name)
        dtinet_sheet.write(i+1, 1, d['smiles'])
        dtinet_sheet.write(i+1, 2, d['protein_id'])
        dtinet_sheet.write(i+1, 3, d['protein_name'])

    f.close()
    output.seek(0)
    content = output.read()
    output.close()

    return content


def excel_dtinet(dtinet_score_entries):
    output = io.BytesIO()
    f = xlsxwriter.Workbook(output, {'in_memory': True})

    dtinet_sheet = f.add_worksheet('DTInet')
    keys = [
        'Protein id', 'Protein name', 'DTInet score',
        'DTInet ranking', 'Label', 'Sequence',
    ]
    for i, j in enumerate(keys):
        dtinet_sheet.write(0, i, j)
    dtinet_sheet.set_column(0, 3, 15)
    dtinet_sheet.set_column(5, 5, 500)
    for i, d in enumerate(dtinet_score_entries):
        dtinet_sheet.write(i+1, 0, d['protein_id'])
        dtinet_sheet.write(i+1, 1, d['protein_name'])
        dtinet_sheet.write(i+1, 2, d['DTInet_score'])
        dtinet_sheet.write(i+1, 3, d['DTInet_ranking'])
        dtinet_sheet.write(i+1, 4, d['label'])
        dtinet_sheet.write(i+1, 5, d['smiles'])

    f.close()
    output.seek(0)
    content = output.read()
    output.close()

    return content


def excel_neodti(neodti_score_entries):
    output = io.BytesIO()
    f = xlsxwriter.Workbook(output, {'in_memory': True})

    neodti_sheet = f.add_worksheet('NeoDTI')
    keys = [
        'Protein id', 'Protein name', 'NeoDTI score',
        'NeoDTI_ranking', 'label', 'Sequence'
    ]
    for i, j in enumerate(keys):
        neodti_sheet.write(0, i, j)
    neodti_sheet.set_column(0, 3, 15)
    neodti_sheet.set_column(5, 5, 1000)
    for i, d in enumerate(neodti_score_entries):
        neodti_sheet.write(i+1, 0, d['protein_id'])
        neodti_sheet.write(i+1, 1, d['protein_name'])
        neodti_sheet.write(i+1, 2, d['NeoDTI_score'])
        neodti_sheet.write(i+1, 3, d['NeoDTI_ranking'])
        neodti_sheet.write(i+1, 4, d['label'])
        neodti_sheet.write(i+1, 5, d['smiles'])

    f.close()    
    output.seek(0)
    content = output.read()
    output.close()

    return content


def common_singlesheet_excel(score_entries, titles, sheet_name):
    output = io.BytesIO()
    f = xlsxwriter.Workbook(output, {'in_memory': True})

    dtinet_sheet = f.add_worksheet(sheet_name)
    keys = titles
    for i, j in enumerate(keys):
        if j == "smiles":
            dtinet_sheet.write(0, i, "sequence")
            continue
        if j == "sequence":
            dtinet_sheet.write(0, i, "smiles")
            continue
        dtinet_sheet.write(0, i, j)
    dtinet_sheet.set_column(0, len(keys)-1, 15)
    for i, d in enumerate(score_entries):
        for j, v in enumerate(keys):
            dtinet_sheet.write(i+1, j, d[v])

    f.close()
    output.seek(0)
    content = output.read()
    output.close()

    return content