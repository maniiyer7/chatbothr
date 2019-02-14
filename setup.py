#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask, redirect, url_for, request

import logging
# Flask app should start in global layout
app = Flask(__name__)


# Flask - database connectivity
# hostname='localhost'
# username='postgres'
# password='root'
# database='HRbot'

# def doQuery( conn,name ) :
#     cur = conn.cursor()

#     cur.execute( "SELECT * FROM Employee_details where name ="+name+";" )
#     leave_balance;
#     for leave in cur.fetchall() :
#         print( leave_balance)
#         leave_balance=leave_balance
#     return leave_balance    


# print( "Using psycopg2…")
# import psycopg2
# myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )


rvw_onduty_leave=''' • Step 1 : Enter your Login credentials for the following IP - www.tvslogistics.com/RVW
    • Step 2: Ensure your role in “EMPROLE” or else click “Change Context” and select “EMPROLE”.
    • Step 3: Go to “Request for Leave->BPC -> Leave Management -> Employee Self Service – Leave -> Request for Leave.
a) Select “Leave Type”.
b) Select “Leave from and Leave To”
c) Select “From and To Session”.
d) Select “Leave Reason” and finally click “Submit”.
e) Select “From and to time “, If you select “On Duty”.
f) Submit Leave application
'''
leave_policy=''' Policy Guidelines:
    • Leave cannot be claimed as a matter of right. It may be sanctioned at the discretion of the
    • management.
    • The leave sanctioning authority may refuse or revoke leave of any kind, if there is a business
    • exigency.
    • No leave of any kind can be granted to an employee for a continuous period of more than 30
    • days without the approval of the CEO.
    • In case of medical leave, the sanctioning authority may seek second medical opinion if
    • considered necessary.
    • An employee overstaying his sanctioned leave without permission would render himself liable
    • for disciplinary action.
    • No leave can be granted to an employee who is facing disciplinary action or is under
    • suspension or is under orders of transfer to another unit.
    • An application for leave for more than two days should be made at least one week before the
    • leave is availed. In case of emergency, a telephonic intimation is mandatory without which leave applied for is liable to be rejected.
    • Employee remaining absent unauthorisedly for more than 8 days without any intimation or without a valid reason would be deemed to have abandoned his duties and would render himself liable for disciplinary action.
    • 
Process Guidelines:

        ◦ Application for any kind of leave shall be in the prescribed format. Employee shall mention in the application his contact address and telephone number. In case of Executives having access of RVW, must apply leave on RVW only.
        ◦ On approval of leave applied the application shall be sent / submitted by the concerned Project
in-charge / KAM /Superior to the respective HR dept. that renders support to the unit / project /
office.
        ◦ All leave cards / records of non-executive employees shall be maintained in the respective HR
Dept. under which the hub or the project personnel come.
        ◦ HR department shall make necessary entries in the leave card / attendance register. The
employee in his interest may also verify correctness.
        ◦ In case of non-submission of leave application to the HR dept. within a day of resuming duties
after leave, the period of absence is liable to be treated as loss of pay.
        ◦ Leave Cards / Records shall be updated and reconciled by HR Dept with the help of inputs
        ◦ from the concerned department / KAM / Project in-charge by end of December every year.
        ◦ Leave balance of employees will be given in the employees’ pay-slip every month.

Types of Leave - Governing Principles:

Casual Leave:

1. Casual Leave is intended to meet special circumstances that cannot be foreseen.
2. An employee on Casual Leave is not treated as absent from duty and pay is not forfeited.
3. Casual Leave would accrue from the date of joining on Pro-rata basis.
4. Casual Leave may be availed one day in a month and cannot be availed for more than three
days at a stretch.
5. Sundays and Holidays intervening during a period of Casual Leave are not counted as part of
Casual Leave.
6. Sundays / Public holidays / weekly offs can be suffixed or prefixed to Casual Leave.
7. Casual Leave cannot be carried forward to the next year nor can it be encashed. Unavailed
leave would lapse at the end of the calendar year.
8. Casual leave cannot be combined with any other kind of leave.
9. Employees wanting to avail Casual Leave have to obtain prior sanction at least a day before
availing or should have submitted their leave application to HR Dept. immediately after
resuming work.

Sick Leave:

1. Sick leave may be sanctioned to meet requirements of an employee to nurse / attend to his/her
sickness.
2. Employees covered under ESI Act would not be eligible for Sick Leave.
3. Sick leave will be admissible only after completion of one year service.
4. Admissible number of day’s sick leave shall be credited in advance in respect of employees
whose services are confirmed. If the employee resigns during the year pro rata recovery shall be
made.
5. Sick Leave application for more than three days shall be supported by a medical certificate /
fitness certificate. Else the period of absence would be treated as Loss of pay.
7. Sick leave is not encashable and cannot be accumulated / carried forward and would lapse at
the end of every year.
8. Sick Leave can be granted to an employee to nurse injury / sickness along with PL.
9. Intervening Holidays/National Holidays/Weekly Offs shall be taken into account for the
stretch of sick leave taken.

Privilege Leave:

1. An employee who has worked for a period of 240 days or more during a calendar year shall be
allowed Privilege Leave during the subsequent calendar year. For those employees who join
during the year, proportionate credit of Privilege Leave will be considered.
2. The eligibility of leave and accumulation to the workman and executives is given above.
3. The above accumulation restriction does not apply to Grade X Executives.
4. Privilege Leave cannot be suffixed or pre-fixed with Casual Leave but can be suffixed /
prefixed with Sick Leave.
5. Privilege Leave at credit can be taken for adjusting the notice period in case of resignation.
6. Privilege Leave at credit may be encashed on resignation /retirement/removal from service and
would be calculated on the last basic pay / consolidated salary drawn. It may also be availed as
leave preparatory to retirement.
7. Only PL can be taken for availing LTA.
8. PL credit for the ensuing year shall be given annually, on 1st Jan.
9. Pro-rata recoveries shall be made from employees leaving the company during the year.
'''


payslip_generation=''' Step 1 : Enter your Login credentials for the following IP - www.tvslogistics.com/RVW
Step 2: Ensure your role in “EMPROLE” or else click “Change Context” and select “EMPROLE”
Step 3: Go to “Pay Slip” -BPC -> Payroll -> Payroll Additional Reports -> Payslip.
    A. Select “Payroll Calendar” as “ Payroll for Regular/Exit” 
    B. Select “Payroll” as “REGULAR PAYROLL TVS” 
    C. Finally click “Payslip” button and Payslip also generate- How to export as “PDF” format -Steps as mentioned below
''' 

salary_queries='''For any salary queries & clarifications write the mail to- lslpayroll@tvslsl.com or contact payroll team members '''

mobile_reimbursements= ''' As per Policy, you need to get one time approval from Business Head / Functional Head and forward the mail to santhosh@tvslsl.com / abdul.a@tvslsl.com to give access to claim.  Mobile Reimbursement will be paid to Asst. Officer to Officer grade executives along with salary every month and Executives in AM & Above cadre has to apply in RVW to get reimbursement.'''

lta_bills_claims='''Employees in Deputy Manager & above grade who are all completed one year of service are eligible to avail LTA. As per Policy, you must take 6 days leave (Excluding W.Off/ Holidays) for claiming LTA. After applying leave in RVW, please submit LTA application Form duly signed by your Line Manager and submit hard copy to  Mr. Santhosh Kumar (santhosh@tvslsl.com). ''' 

notice_period = ''' All confirmed executives has to serve 90 days Notice Period as per the terms on your appointment.''' 

tvs_way=''' It is a set of behaviours desired in a TVS Executive in line with the organization’s values of 
Professional Integrity 
Integrity, as a concept is the consistency of actions, values, methods, measures, principles, expectations and outcomes. It is the quality of having a sense of honesty and truthfulness
Cost Optimization
 Finding an alternative with the most cost effective or highest achievable performance under the given constraints, by maximizing desired factors and minimizing undesired ones.
Service Delivery
 To manage the performance of services to clients as agreed in the contract and ensures that the Service Levels are achieved.
Relentlessly Lean 
Constantly focuses on improving efficiency and eliminating waste in the system. Builds the culture of efficiency through the LSS process. Optimises cost and realises value in every spending.
Collaborative Innovation 
Constantly makes improvements through breakthrough ideas involving all stakeholders. Encourages ideas, suggestions and actively support their implementation. Looks for the best practices to learn from and replicate in the business.
Passionately Reliable 
Passionately works towards delivering commitments consistently. Accepts accountability to ensure delivery. Puts customer needs on top of the agenda. Reviews and debottlenecks to deliver the commitments. '''


vison_mission = '''Values
    • Trust
    • Value
    • Service


Vision
We aim to be a leading Indian MNC and a partner of choice for our customers, in providing customised, integrated supply chain solutions across the globe
Mission
To Deliver unique, value added supply chain solutions and create a committed, partnership-like approach with customers
 ''' 

fnf=''' Resignation Letter duly accepted by Line Manager has to be forwarded to HR Team. 
No Dues Clearance should be obtained from all departments and Exit Interview Form to be produced before date of relieving. 
In case of any queries on F&F settlement, please contact Mr. Nandhakumar- nandhakumar.m@tvslsl.com 
Any escalations, please send mail to srk@tvslsl.com'''


pf_queries= ''' For any PF /ESI related queries & clarifications write the mail to- sureshj@tvslsl.com or contact statutory team directly. ''' 

tvs_tenets = ''' Professional Integrity 
Integrity, as a concept is the consistency of actions, values, methods, measures, principles, expectations and outcomes.
It is the quality of having a sense of honesty and truthfulness.
PI 1 I will close all issues within agreed timelines.
•       Planning the functions keeping in mind the venture priorities.
•       Committing desired services consistently after considering the plan of action.
•       Spotting and removing barriers to meet the commitments within the agreed timelines.
•       Breaking bigger projects into many smaller manageable tasks that need to be done.
PI 2 I will lead by example in a transparent manner
•       Operational transparency with all stake holders.
•       Taking the responsibility and becoming accountable for the processes assigned.
•       Creating ownership and personal commitment to work.
 
PI 3 I will ensure strict adherence to norms, policies and processes. Dos
•       Abiding by the governing policies and norms of the organization.
•       Communicating and clarifying policies and norms established.
•       Escalating deviations if any, to the reporting level.
•       Becoming aware of any deviations and avoiding its recurrence.
PI4 I will act in the best interest of the organization Dos
•       Continuously adding value to the working environment.   
•       Keeping the interest of the organization in the mind.
•       Putting TVS first in all the activities.
•       Monitoring competitors to enjoy competitive advantage.
•       Taking responsibility to coach, develop and improve individual performance.
 
Cost Optimization
Finding an alternative with the most cost effective or highest achievable performance under the given constraints, by maximizing desired factors and minimizing undesired ones. In comparison, maximization means trying to attain the highest or maximum result or outcome without regard to cost or expense.
CO 1 I will not incur any expenses which is not budgeted.
    • I will estimate operational costs in the light of current market trend and with the knowledge of past history.
    • I will seek sufficient sanction in the budgets for operations and implementation of processes.
    • I will ensure proper utilization of allotted revenues to the projects and practices.
    • Reduce the current risk levels posed by non-compliance with internal policies and external tax/government regulations to stay within the budget.
 
CO 2 I will obtain the acceptance of superiors/right stake holders before I incorporate any cost increase in the system.
    • Sensing and alerting any cost increase in the system to the respective reporting authorities.
    • Following the protocols in such processes and involving the superiors and right stake holders in decision making.
    • Attending to significant cost deviations more urgently than to insignificant cost deviations.  
 
CO3 I will continuously eliminate waste and maximize resource utilization
    • Exploring the avenues regularly to eliminate waste and non value added practices in TVS.
    • Estimating and deploying the required resources and ensure optimum utilization of the available resources to reduce its wastage.
    • Measuring the core processes and analyzing the processes that work and improving those that don’t, so as to remove waste and add value.
    • Focusing individual effort on continuous improvement and work simplification.
    • Encouraging people to optimize the success of the organization by working together rather than trying to increase the resource allocation for their own areas.
 
Service Delivery
To manage the performance of services to clients as agreed in the contract and ensure that the Service Levels are achieved.
 
SD 1 I will ensure service delivery as agreed in SLAs and KDs
 
    • Defining service level agreements (SLA’S) related to contracted services and  Ensuring SLA’s are achieved and client expectations are met.
    • Spotting and acting on opportunities to improve service delivery as agreed.
    • Empowering the subordinates to reach the agreed levels of results and develop team processes.
    • To ensure that systems, processes and methodologies as specified are followed to sure effective monitoring, control and support of service delivery.
    • Ensuring that the teams use and improve best practices models to gain competitive advantage.
SD 2 I will develop processes to improve and maximize service quality 
    • Continuously improving the existing processes and adopting changes for better results.
    • Flexibility to experiment new processes within the permissible risk levels.
    • Keeping in mind the needs of the customers, customer feedback and external market knowledge while developing new processes.
SD 3 I will value and enhance my relationships with all stake holders
    • To build services relationships with clients.
.
    • Attend client service review meetings; areas covered will include performance reports, service improvements, quality and processes.
    • To develop and facilitate workshops and training courses.
    • Building external relationships to benefit the business and cultivating networks to ensure collaboration, integration and alignment. ''' 
# @app.route('/test',methods = ['POST', 'GET'])
# def test():
#     return "Hello world"

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    
    logging.debug('This is a debug message')
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    #r = make_response(res)
    # r.headers['Content-Type'] = 'application/json'
    return res


def makeWebhookResult(req):

    if req.get("result").get("action") != "leave-types":
       return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("leaves")

    # leave_bal=doQuery( myConnection ,zone)
    # myConnection.close()

    cost = {'rvw on duty':rvw_onduty_leave,'leave':rvw_onduty_leave,'leave policy':leave_policy,'payslip generation':payslip_generation,
            'salary queries':salary_queries,'mobile reimbusements':mobile_reimbursements,'lta bills claims':lta_bills_claims,
            'notice period':notice_period,'tvs way':tvs_way,'vison mission':vison_mission,'fnf':fnf,'pf queries':pf_queries,'tvs tenets':tvs_tenets}

    speech = "The answer to " + zone + " is " + str(cost[zone])
    #print(leave_bal)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        #9636446568
        "source": "leave-balance"
    }

if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))

    #print ("Starting app on port %d" %(port))

    app.run(debug=True,port=80, host='0.0.0.0')