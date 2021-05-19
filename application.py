from flask import *
import io
import csv
import pandas as pd
import numpy
import odf
import statistics
from pandas_ods_reader import read_ods
import odf
from matplotlib import pyplot as plt


# Importing the data from the original .ods files
# replacing the empty info with 0 for more accurate results
# and stocking the averages/standard deviations in arrays 

data_frame1 = read_ods("raw_data/certification_pix_2018_2019.ods",1)
data_frame1=data_frame1.replace("-",0)
avg1=data_frame1.mean()
std1=data_frame1.std()


data_frame2 = read_ods("raw_data/certification_pix_2019_2020.ods",1)
data_frame2=data_frame2.replace("-",0)
avg2=data_frame2.mean()
std2=data_frame2.std()

data_frame3 = read_ods("raw_data/certification_pix_2020_2021.ods",1)
data_frame3=data_frame3.replace("-",0)
avg3=data_frame3.mean()
std3=data_frame3.std()


idcomp =["1.1","1.2","1.3","2.1","2.2","2.3","2.4","3.1","3.2","3.3","3.4","4.1","4.2","4.3","5.1","5.2"]

# the box_plot data


# Getting the data for the box_plot
# from the matplotlib graph using get_ydata()

def get_box_plot_data(labels, bp):
    rows = []

    for i in range(len(labels)):
        dict1 = {}
        dict1['lowest'] = bp['whiskers'][i*2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['higher_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['highest'] = bp['whiskers'][(i*2)+1].get_ydata()[1]
        dict1['id'] = i+1
        rows.append(list(dict.values(dict1)))

    return rows


# the pie charts
# functions that calculate percentages of students who passed a skill & those who didn't
result = []
cpt = 0

def calculate_percentages(df):
  file_idcomp = list(df.columns)
  for i in range(16):
    number_columns = df.loc[:,file_idcomp[i]]
    column = number_columns.values
    cpt = 0
    for j in range(len(df)):
      if(column[j] == 0):
        cpt -= 1
    result.append([((len(df)+cpt)/len(df))*100,(-cpt/len(df))*100])
    cpt = 0
  return result




###NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)




# sending the pie chart data


@app.route("/piechart_2018_2019.csv")
def send_piechart1():
  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")

  # getting the data
  result = []
  cpt = 0

  #fonction qui trace les boites à moustaches directement à partir de la dataframe
  #elle fait tout le boulot HiHi
  data_to_send = calculate_percentages(data_frame1)

  # list of list of the data that we have to send

  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("cert","not_cert"))
  for i in range(16):
    writer.writerow([round(data_to_send[i][0],2),round(data_to_send[i][1],2)])


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=piechart1.csv"
  output.headers["Content-type"] = "text/csv"
  return output



@app.route("/piechart_2019_2020.csv")
def send_piechart2():
  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")

  # getting the data
  #
  result = []
  cpt = 0

  #fonction qui trace les boites à moustaches directement à partir de la dataframe
  #elle fait tout le boulot HiHi
  data_to_send = calculate_percentages(data_frame2)

  # list of list of the data that we have to send

  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("cert","not_cert"))
  for i in range(16):
    writer.writerow([round(data_to_send[i][0],2),round(data_to_send[i][1],2)])


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=piechart2.csv"
  output.headers["Content-type"] = "text/csv"
  return output



@app.route("/piechart_2020_2021.csv")
def send_piechart3():
  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")

  # getting the data
  result = []
  cpt = 0

  #fonction qui trace les boites à moustaches directement à partir de la dataframe
  #elle fait tout le boulot HiHi
  data_to_send = calculate_percentages(data_frame3)

  # list of list of the data that we have to send

  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("cert","not_cert"))
  for i in range(16):
    writer.writerow([round(data_to_send[i][0],2),round(data_to_send[i][1],2)])


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=piechart3.csv"
  output.headers["Content-type"] = "text/csv"
  return output



#sending box_plot data

@app.route("/boitem_2018_2019.csv")
def send_boitem1():



  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")

  # getting the data
  data = pd.DataFrame.transpose(data_frame1)
  #fonction qui trace les boites à moustaches directement à partir de la dataframe
  #elle fait tout le boulot HiHi
  bp = plt.boxplot(data)

  # list of list of the data that we have to send
  result = get_box_plot_data(idcomp,bp)

  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("lowest", "lower_quartile", "median" , "higher_quartile", "highest", "id"))
  for i in range(16):
  	writer.writerow((result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5]))


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=boitem1.csv"
  output.headers["Content-type"] = "text/csv"
  return output



@app.route("/boitem_2019_2020.csv")
def send_boitem2():



  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")

  # getting the data
  data = pd.DataFrame.transpose(data_frame2)
  
  #fonction qui trace les boites à moustaches directement à partir de la dataframe
  #elle fait tout le boulot HiHi
  bp = plt.boxplot(data)

  # list of list of the data that we have to send
  result = get_box_plot_data(idcomp,bp)

  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("lowest", "lower_quartile", "median" , "higher_quartile", "highest", "id"))
  for i in range(16):
  	writer.writerow((result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5]))


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=boitem1.csv"
  output.headers["Content-type"] = "text/csv"
  return output



@app.route("/boitem_2020_2021.csv")
def send_boitem3():



  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")

  # getting the data
  data = pd.DataFrame.transpose(data_frame3)
  #fonction qui trace les boites à moustaches directement à partir de la dataframe
  #elle fait tout le boulot HiHi
  bp = plt.boxplot(data)

  # list of list of the data that we have to send
  result = get_box_plot_data(idcomp,bp)

  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("lowest", "lower_quartile", "median" , "higher_quartile", "highest", "id"))
  for i in range(16):
  	writer.writerow((result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5]))


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=boitem1.csv"
  output.headers["Content-type"] = "text/csv"
  return output








# Sending the information for the year 2018/2019 to the designated route

@app.route("/certification_pix_2018_2019.csv")
def send_data1():

  # Creating the csv file
  csvdata1 = io.StringIO()
  writer = csv.writer(csvdata1,delimiter=",")


  # Storing the averages & stds in an array to ease putting it in a csv file
  result=[	[avg1[0],avg1[1],avg1[2],avg1[3],avg1[4],avg1[5],avg1[6],avg1[7],avg1[8],avg1[9],avg1[10],avg1[11],avg1[12],avg1[13],avg1[14],avg1[15]],
            [std1[0],std1[1],std1[2],std1[3],std1[4],std1[5],std1[6],std1[7],std1[8],std1[9],std1[10],std1[11],std1[12],std1[13],std1[14],std1[15]]]


  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("avg", "std"))
  for i in range(16):
  	writer.writerow((result[0][i],result[1][i]))


  #making the csv file available in the route
  output = make_response(csvdata1.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=data1.csv"
  output.headers["Content-type"] = "text/csv"
  return output



# Sending the information for the year 2018/2019 to the designated route

@app.route("/certification_pix_2019_2020.csv")
def send_data2():

  #Creating the csv file
  csvdata2 = io.StringIO()
  writer = csv.writer(csvdata2,delimiter=",")

  # Storing the averages & stds in an array to ease putting it in a csv file
  result=[[avg2[0],avg2[1],avg2[2],avg2[3],avg2[4],avg2[5],avg2[6],avg2[7],avg2[8],avg2[9],avg2[10],avg2[11],avg2[12],avg2[13],avg2[14],avg2[15]],
            [std2[0],std2[1],std2[2],std2[3],std2[4],std2[5],std2[6],std2[7],std2[8],std2[9],std2[10],std2[11],std2[12],std2[13],std2[14],std2[15]]]


  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("avg", "std"))
  for i in range(16):
  	writer.writerow([result[0][i],result[1][i]])


  #making the csv file available with the route
  output = make_response(csvdata2.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=data2.csv"
  output.headers["Content-type"] = "text/csv"
  return output




# On renvoie les résultats de l'année 2020/2021

@app.route("/certification_pix_2020_2021.csv")
def send_data3():

  #Creating the csv file
  csvdata3 = io.StringIO()
  writer = csv.writer(csvdata3,delimiter=",")

  # Storing the averages & stds in an array to ease putting it in a csv file
  result=[[avg3[0],avg3[1],avg3[2],avg3[3],avg3[4],avg3[5],avg3[6],avg3[7],avg3[8],avg3[9],avg3[10],avg3[11],avg3[12],avg3[13],avg3[14],avg3[15]],
          [std3[0],std3[1],std3[2],std3[3],std3[4],std3[5],std3[6],std3[7],std3[8],std3[9],std3[10],std3[11],std3[12],std3[13],std3[14],std3[15]]]


  # Creating a csv file with two columns( avg : averages & stds : standard deviations )
  # listing 16 rows, each one for a a PIX skill ( pix is a test that has 16 skills )
  writer.writerow(("avg", "std"))
  for i in range(16):
  	writer.writerow([result[0][i],result[1][i]])


  #making the csv file available with the route
  output = make_response(csvdata3.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=data3.csv"
  output.headers["Content-type"] = "text/csv"
  return output



@app.route("/")
def main_page():
	# the main page of the website
	return render_template("index.html")






#NE SURTOUT PAS MODIFIER
if __name__ == "__main__":
	app.run(host='127.0.0.1', debug=True, port=5000)