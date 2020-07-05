from django.shortcuts import render
import openpyxl
import pandas as pd
import numpy as np


def report_view(request):
    return render(request, 'reports.html')


def index(request):
    report_name = {
        "applied_limit": "Applied Limit Report",
        "loan_repayment": "Loan Repayment Report"
    }
    if "GET" == request.method:
        return render(request, 'reports.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        report_type = str(request.POST["report_type"])

        _writer = pd.ExcelWriter('Mybook.xlsx', engine='xlsxwriter')
        ws = pd.read_excel(excel_file, report_name[report_type])
        ws.to_excel(_writer, sheet_name=report_name[report_type])

        pivot_data = pd.pivot_table(ws, 'Id Card Number', ['Respondent type'], columns=['Limit Status'], aggfunc=np.count_nonzero, margins=True)
        print(pivot_data)
        pivot_data.to_excel(_writer, sheet_name='pivot')
        _writer.save()
        pivot_sheet = pd.read_excel(_writer, sheet_name='pivot')

        return render(request, 'reports.html', {"excel_data": pivot_sheet})
