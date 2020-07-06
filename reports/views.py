import os

from django.shortcuts import render
import openpyxl
import pandas as pd
import numpy as np
from django.http import HttpResponse
from datetime import date

from pyshop.settings import BASE_DIR


def report_view(request):
    return render(request, 'reports.html')


def download_report(request):
    filename = 'Pivots.xlsx'
    content = pd.read_excel(BASE_DIR + '/' + filename)
    response = HttpResponse(content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Pivots-' + date.today( ).isoformat( ) + '.xlsx'
    return response


def index(request):
    report_name = {
        "applied_limit": "Applied Limit Report",
        "loan_repayment": "Loan Repayments Report"
    }
    if "GET" == request.method:
        return render(request, 'reports.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        report_type = str(request.POST["report_type"])
        print(report_type)
        writer = pd.ExcelWriter('Pivots.xlsx', engine='xlsxwriter')

        ws = pd.read_excel(excel_file, report_name[report_type])
        ws.to_excel(writer, sheet_name=report_name[report_type])
        print(report_type == "applied_limit")
        if report_type == "applied_limit":
            pv_data = pd.pivot_table(ws, 'Id Card Number', ['Respondent type'], columns=['Limit Status'],
                                     aggfunc=np.count_nonzero, margins=True)

            pv_sheet = write_pivot(writer, pv_data)
            return render(request, 'reports.html', {"excel_data": pv_sheet})
        elif report_type == "loan_repayment":
            pv_data = pd.pivot_table(ws, 'Repaid amount', ['Offer availed date / Repayment Date'],
                                     columns=['Respondent type'],
                                     aggfunc=np.sum, margins=True)
            return render(request, 'reports.html', {"excel_data": write_pivot(writer, pv_data)})


def write_pivot(writer, pivot_data):
    pivot_data.to_excel(writer, sheet_name='pivot')
    writer.save( )
    pivot_sheet = pd.read_excel(writer, sheet_name='pivot')

#    for i, data in enumerate(pivot_sheet.values):
 #       indices = np.where(np.isnan(data), dtType='float')
        #for j, col in enumerate(data):

            #if isinstance(col, float) and np.isnan(col):
                # print(f'{col} -{isinstance(col,float)}')
             #   print(type(data))

                # print(f'{i} - {j}')
        # print(f'{str(data)} - {str(data).isnumeric()}')
        # print(np.isnan(data))
        # data[np.isnan(data)] = 0

    return pivot_sheet;
