from flask import Flask, render_template, request
import pickle
app = Flask(__name__)
# model = bz2.BZ2File('random_forest_regression_model_compressed.pbz2', 'rb')
model = pickle.load(open("actual.pkl", "rb"))
# model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type=0
    Seller_Type=0
    Transmission_Type=0
    # order
    # name  year  km_driven  fuel  seller_type  transmission  owners  mileage engine  max_power  seats
    #fuel - Diesel - 1 Petrol - 3 CNG - 2
    # 
    if request.method == 'POST':
        Model = request.form['model']
        Year = int(request.form['Year'])
        kms_driven=float(request.form['kms_driven'])
        Fuel_Type_Form=request.form['Fuel_Type']
        Mileage = float(request.form['Mileage'])
        if(Fuel_Type_Form=='Petrol'):
            Fuel_Type=3
        elif(Fuel_Type_Form == 'Diesel'):
            Fuel_Type=1
        else:
            Fuel_Type=2
        Seller_Type=request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            Seller_Type=1
        else:
            Seller_Type=0	
        Transmission_Type_Form=request.form['Transmission_Type']
        if(Transmission_Type_Form=='Manual'):
            Transmission_Type=1
        else:
            Transmission_Type=0
        Owner=int(request.form['Owner'])
        Mileage = float(request.form['Mileage'])
        Engine_CC = int(request.form['Engine_CC'])
        Max_Power = float(request.form['Max_Power'])
        Seats = int(request.form['Seats'])
        # order
        # name  year  km_driven  fuel  seller_type  transmission  owner  mileage engine  max_power  seats
        user_input = [[1249,Year,kms_driven,Fuel_Type,Seller_Type,Transmission_Type,Owner,Mileage,Engine_CC,Max_Power,Seats]]
        # app.logger.info(user_input)
        prediction=model.predict([[1249,2014,145500,1,1,1,0,23.40,1248.0,74.00,5.0]])
        # prediction = model.predict(user_input)
        app.logger.info(user_input)
        output=(prediction[0])
        if output<0:
            return render_template('predict.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('predict.html',prediction_text="You Can Sell The Car at {} Rupees".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)