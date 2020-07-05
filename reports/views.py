from django.shortcuts import render
import openpyxl
import pandas as pd
import numpy as np


def report_view(request):
    return render(request, 'reports.html')


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
        writer = pd.ExcelWriter('Mybook.xlsx', engine='xlsxwriter')

        ws = pd.read_excel(excel_file, report_name[report_type])
        ws.to_excel(writer, sheet_name=report_name[report_type])
        print(report_type == "applied_limit")
        if report_type == "applied_limit":
            pv_data = pd.pivot_table(ws, 'Id Card Number', ['Respondent type'], columns=['Limit Status'],
                                     aggfunc=np.count_nonzero, margins=True)

            pv_sheet = write_pivot(writer,pv_data)
            return render(request, 'reports.html', {"excel_data": pv_sheet})
        elif report_type == "loan_repayment":
            pv_data = pd.pivot_table(ws, 'Repaid amount', ['Offer availed date / Repayment Date'], columns=['Respondent type'],
                                     aggfunc=np.sum, margins=True)

            return render(request, 'reports.html', {"excel_data": write_pivot(writer,pv_data)})


def write_pivot(writer,pivot_data):
    pivot_data.to_excel(writer, sheet_name='pivot')
    writer.save()
    pivot_sheet = pd.read_excel(writer, sheet_name='pivot')
    return pivot_sheet;

