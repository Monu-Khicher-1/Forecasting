from email.policy import default
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def name(x):
    match x:
        case 0:
            return "Jan"
        case 1:
            return "Feb"
        case 2:
            return "Mar"
        case 3:
            return "Apr"
        case 4:
            return "May"
        case 5:
            return "Jun"
        case 6:
            return "Jul"
        case 7:
            return "Aug"
        case 8:
            return "Sep"
        case 9:
            return "Oct"
        case 10:
            return "Nov"
        case 11:
            return "Dec"
        case default:
            return "None"

def Col(x):
    match x:
        case 0:
            return "B"
        case 1:
            return "C"
        case 2:
            return "D"
        case 3: 
            return "E"
        case 4:
            return "F"
        case 5:
            return "G"
        case 6:
            return "H"
        case 7:
            return "I"
        case 8:
            return "J"
        case 9:
            return "K"
        case 10:
            return "L"
        case 11:
            return "M"
        case 12:
            return "N"
        case 13:
            return "O"
        case 14:
            return "P"
        case 15: 
            return "Q"
        case 16:
            return "R"
        case 17:
            return "S"
        case 18:
            return "T"
        case default:
            return "U"
##############################################################################################

book=Workbook()
sheet=book.active
row=1

###############################################################################################
inp1=input("Enter year: ")
start_date=int(input("Start Date: "))
start_month=int(input("Start Month: "))

PATH="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(PATH)
driver.get("https://www.iexindia.com/marketdata/areaprice.aspx")
try:
    elem1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_InnerContent_ddlPeriod")))
    period=Select(elem1)
    period.select_by_value('SR')

    initial=True
    for a in range(1):
        
        year=str(int(inp1)+a)
        for month in range(start_month-1,12):
            month_range=30
            if (month==0) or(month==2)or(month==4)or(month==6)or(month==7)or(month==9)or(month==11) :
                month_range=31
            elif(month==1 and ((2015+a)%4==0)):
                month_range=29
            elif(month==1):
                month_range=28

            if(not initial):
                start_date=1
            initial=False
            for date in range(start_date-1,month_range):
                year_elem= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scwYears")))
                month_elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scwMonths")))
                date_cell=list()
                for i in range(35):
                                cell_id="scwCell_"+str(i)
                                date_cell.append(driver.find_element(By.ID,cell_id))
                from_date=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_InnerContent_calFromDate_txt_Date")))
                to_date=driver.find_element(By.ID,"ctl00_InnerContent_calToDate_txt_Date")
                update_report=driver.find_element(By.ID,"ctl00_InnerContent_btnUpdateReport")
                from_date.click()
                Year=Select(year_elem)
                Year.select_by_value(year)
                Month=Select(month_elem)
                month_name=name(month)
                Month.select_by_value(month_name)
                for i in range(35):
                    if(date_cell[i].text==str(date+1)):
                        date_cell[i].click()
                to_date.click()
                Year=Select(year_elem)
                Year.select_by_value(year)
                Month=Select(month_elem)
                month_name=name(month)
                Month.select_by_value(month_name)

                for i in range(35):
                    if(date_cell[i].text==str(date+1)):
                        date_cell[i].click()

                update_report.click()
                driver.implicitly_wait(2)

                ddmmyy=str(date+1)+"/"+str(month+1)+"/"+year+" "
                print(ddmmyy)
                for i in range(96):
                    print(ddmmyy,end=" ")
                    sheet["A"+str(row)]=ddmmyy
                    if(i<10):
                        print("|| "+str(i)+"  ||",end=" ")
                    else:
                        print("|| "+str(i)+" ||",end=" ")
                    for j in range(14):
                        XPath="/html/body/form/div[3]/section[2]/div/div/div/span[3]/div/table/tbody/tr[5]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr["+str(i+3)+"]/td["+str(j+2)+"]/div"
                        if(i==0):
                            XPath="/html/body/form/div[3]/section[2]/div/div/div/span[3]/div/table/tbody/tr[5]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr["+str(i+3)+"]/td["+str(j+4)+"]/div"
                        elif (i%4==0):
                            XPath="/html/body/form/div[3]/section[2]/div/div/div/span[3]/div/table/tbody/tr[5]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr["+str(i+3)+"]/td["+str(j+3)+"]/div"
                        val=driver.find_element(By.XPATH, XPath)
                        print(val.text,end=" ")
                        if j==0:
                            sheet[Col(j)+str(row)]=val.text
                        elif(val.text=='-'):
                            sheet[Col(j)+str(row)]
                        else:
                            sheet[Col(j)+str(row)]=float(val.text)
                    print()
                    row+=1

finally:
    fname="market_data_"+year+"from_12.xlsx"
    book.save(fname)
    print("Done.")