# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import db
from scapp import app
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKFKJH

from scapp.models import View_Loan_Expected

import datetime,time,xlwt,re
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换

from scapp.models import SC_Loan_Product

# 贷款根据状态分类——7. 预期的贷款 
@app.route('/Report/dkgjztfl_7', methods=['GET'])
def dkgjztfl_7():
	loan_product = SC_Loan_Product.query.all()
	return render_template("Report/dkgjztfl_7.html",loan_product=loan_product)

# 贷款根据状态分类——7. 预期的贷款 
@app.route('/Report/dkgjztfl_7_search/<int:page>', methods=['POST'])
def dkgjztfl_7_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " 1=1"
    if loan_type != '0':
        sql += " and loan_type='"+loan_type+"' "
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    view_Loan_expected = View_Loan_Expected.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Report/dkgjztfl_7_search.html",loan_type=loan_type,customer_name=customer_name,
        view_Loan_expected=view_Loan_expected)

# 贷款根据状态分类——7. 预期的贷款--导出
@app.route('/Report/dkgjztfl_7_export', methods=['POST'])
def dkgjztfl_7_export():
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " 1=1"
    if loan_type != '0':
        sql = " and loan_type='"+loan_type+"' "
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    #data = View_Loan_Expected.query.filter(sql)
    query_sql = "select clear_date,customer_name,itelephone,loan_account,total,principal,interest,"
    query_sql += "ratio,installmenst,loan_manager from view_loan_expected where "
    query_sql += sql
    data=db.engine.execute(query_sql)

    exl_hdngs=['还贷日期','客户名称','电话','还款帐号','还款总额','应还本金','应还利息','贷款利率','还款顺序号','信贷员']

    type_str = 'date text text text text text text text text text'#1
    types= type_str.split()

    exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
    types_to_xf_map={
        'int':ezxf(num_format_str='#,##0'),
        'date':ezxf(num_format_str='yyyy-mm-dd'),
        'datetime':ezxf(num_format_str='yyyy-mm-dd HH:MM:SS'),
        'ratio':ezxf(num_format_str='#,##0.00%'),
        'text':ezxf(),
        'price':ezxf(num_format_str='￥#,##0.00')
    }

    data_xfs=[types_to_xf_map[t] for t in types]
    date=datetime.datetime.now()
    year=date.year
    month=date.month
    day=date.day
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'预期的贷款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'预期的贷款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)

