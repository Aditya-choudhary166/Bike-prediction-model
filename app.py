from flask import Flask,render_template,request,url_for
import joblib
import mysql.connector 
import pandas as pd
import numpy as np

##load the model
model=joblib.load(r"C:\Users\jatad\OneDrive\Desktop\MITRC-4-SEM\python\bike_prediction_model.lb")

##initialize the flask application
app=Flask(__name__)

##mysql databaase connectivity-->

def get_db_connection():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="9079285970",
            database="bike_prediction"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to mysql:{err}")
        return None

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/project")
def project():
    return render_template("project.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/history',methods=["GET","POST"])
@app.route('/history1', methods=["GET", "POST"])
def history():
    brand_name_filter = request.values.get("brand_name_filter", None)

    conn = get_db_connection()
    historical_data = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            if brand_name_filter:
                query = "SELECT * FROM bike_prediction WHERE brand_name = %s"
                cursor.execute(query, (brand_name_filter,))
            else:
                query = "SELECT * FROM bike_prediction"
                cursor.execute(query)

            historical_data = cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error fetching data from mysql: {err}")
        finally:
            cursor.close()
            conn.close()

    return render_template('history.html', historical_data=historical_data)

# def history():
#     brand_name_filter=request.form.get(
#         "brand_name_filter",None

#     )

 

#     conn=get_db_connection()
#     historical_data=[]

#     if conn:
#         cursor=conn.cursor(dictionary=True)
#         try:
#             if brand_name_filter:
#                 query="SELECT *FROM bike_prediction Where brand_name= %s"
#                 cursor.execute(query,(brand_name_filter,))
#             else:
#                 query="SELECT *FROM bike_prediction"
#                 cursor.execute(query)
                
#                 ##fetch all the data
#                 historical_data=cursor.fetchall()

#         except mysql.connection.Error as err:
    
#                 print("Error fetching data from mysql:{err}")
#         finally:
#              cursor.close()
#              conn.close()
#         return render_template('history.html',historical_data=historical_data)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            brand_name = request.form['brand_name']
            owner_name = request.form['owner']
            age_bike = request.form['age']
            power_bike = int(float(request.form['power']))
            kms_driven_bike = int(float(request.form['kms_driven']))

            bike_numbers = {
                'TVS': 0, 'Royal Enfield': 1, 'Triumph': 2, 'Yamaha': 3,
                'Honda': 4, 'Hero': 5, 'Bajaj': 6, 'Suzuki': 7, 'Benelli': 8,
                'KTM': 9, 'Mahindra': 10, 'Kawasaki': 11, 'Ducati': 12, 
                'Hyosung': 13, 'Harley-Davidson': 14, 'Jawa': 15, 'BMW': 16,
                'Indian': 17, 'Rajdoot': 18, 'LML': 19, 'Yezdi': 20,
                'MV': 21, 'Ideal': 22
            }

            brand_name_encoded = bike_numbers.get(brand_name, -1)
            if brand_name_encoded == -1:
                return render_template('project.html', prediction="Invalid Brand Selected")

            input_data = np.array([[int(owner_name), brand_name_encoded,
                                    kms_driven_bike, int(age_bike), power_bike]])

            prediction = model.predict(input_data)[0]
            prediction = round(prediction, 2)

            # Database insert code
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                query = """
                    INSERT INTO bike_prediction 
                    (owner_name, brand_name, kms_driven_bike, age_bike, power_bike, prediction)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                user_data = (int(owner_name), brand_name, kms_driven_bike, int(age_bike), power_bike, prediction)
                cursor.execute(query, user_data)
                conn.commit()
                cursor.close()
                conn.close()

            return render_template('project.html', prediction=prediction)

        except Exception as e:
            return render_template('project.html', prediction=f"Error: {str(e)}")
         
    
#   ##prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     if request.method == 'POST':
#         try:
#             brand_name = request.form['brand_name']
#             owner_name = request.form['owner']  # corrected
#             age_bike = request.form['age']      # corrected
#             # power_bike = int(request.form['power'])
#             # kms_driven_bike = int(request.form['kms_driven'])
#             power_bike = int(float(request.form['power']))
#             kms_driven_bike = int(float(request.form['kms_driven']))


        #     # Mapping brand names
        #     bike_numbers = {
        #         'TVS': 0, 'Royal Enfield': 1, 'Triumph': 2, 'Yamaha': 3,
        #         'Honda': 4, 'Hero': 5, 'Bajaj': 6, 'Suzuki': 7, 'Benelli': 8,
        #         'KTM': 9, 'Mahindra': 10, 'Kawasaki': 11, 'Ducati': 12, 
        #         'Hyosung': 13, 'Harley-Davidson': 14, 'Jawa': 15, 'BMW': 16,
        #         'Indian': 17, 'Rajdoot': 18, 'LML': 19, 'Yezdi': 20,
        #         'MV': 21, 'Ideal': 22
        #     }

        #     # Encode brand name
        #     brand_name_encoded = bike_numbers.get(brand_name, -1)

        #     # Check brand is valid
        #     if brand_name_encoded == -1:
        #         return render_template('project.html', prediction="Invalid Brand Selected")

        #     # Convert inputs properly
        #     input_data = np.array([[int(owner_name), brand_name_encoded,
        #                             kms_driven_bike, int(age_bike), power_bike]])

        #     # Prediction
        #     prediction = model.predict(input_data)[0]
        #     prediction = round(prediction, 2)

        #     return render_template('project.html', prediction=prediction)

        # except Exception as e:
        #     return render_template('project.html', prediction=f"Error: {str(e)}")





            
            
            ##save the prediction to database
            conn=get_db_connection()
            if conn:
                cursor=conn.cursor()
                query="INSERT INTO bike_prediction(owner_name,brand_namekms_driven_bike,age_bike,power_bike,prediction) VALUES(%s,%s,%s,%s,%s,%s)"
                user_data=(owner_name,brand_name,kms_driven_bike,age_bike,power_bike)
                cursor.execute(query,user_data)
                conn.commit()
                cursor.close()
                conn.close()

            
                
            

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',
            port=2525)
    



#     <div class="button-group">
#   <a href="{{ url_for('project') }}"><button>My Project</button></a>
#   <a href="{{ url_for('contact') }}"><button>Contact Us</button></a>
#   <a href="{{ url_for('history') }}"><button>History</button></a>
# </div>
