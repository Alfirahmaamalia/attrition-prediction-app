from flask import Flask, render_template, request, jsonify
import os
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_view.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_view():
    prediction = None
    prediction_label = None
    error_message = None
    
    if request.method == 'POST':
        try:
            # Get form data
            # Get form data
            age = request.form.get('age', type=float)
            monthly_income = request.form.get('monthlyIncome', type=float)
            years_at_company = request.form.get('yearsAtCompany', type=float)
            years_with_curr_manager = request.form.get('yearsWithCurrManager', type=float)
            department = request.form.get('department')
            job_role = request.form.get('jobRole')
            marital_status = request.form.get('maritalStatus')
            over_time = request.form.get('overTime')
            gender = request.form.get('gender')
            job_satisfaction = request.form.get('jobSatisfaction', type=int)
            environment_satisfaction = request.form.get('environmentSatisfaction', type=int)
            
            # Validate inputs
            input_values = [age, monthly_income, years_at_company, years_with_curr_manager, 
                            department, job_role, marital_status, over_time, gender, 
                            job_satisfaction, environment_satisfaction]
                            
            if any(v is None or str(v).strip() == "" for v in input_values):
                error_message = "Semua field harus diisi"
            else:
                # Import prediction function
                try:
                    from modelling import predict
                    
                    # Prepare input data
                    input_data = {
                        'Age': age,
                        'MonthlyIncome': monthly_income,
                        'YearsAtCompany': years_at_company,
                        'YearsWithCurrManager': years_with_curr_manager,
                        'Department': department,
                        'JobRole': job_role,
                        'MaritalStatus': marital_status,
                        'OverTime': over_time,
                        'Gender': gender,
                        'JobSatisfaction': job_satisfaction,
                        'EnvironmentSatisfaction': environment_satisfaction
                    }
                    
                    # Make prediction
                    result = predict(input_data)
                    
                    if isinstance(result, dict) and "prediction" in result:
                        prediction = result["prediction"]
                        probability = result["probability"]
                        prediction_label = "Berisiko Attrition" if prediction == "Yes" else "Aman (Tidak Attrition)"
                    else:
                        prediction = result
                        probability = None
                        prediction_label = "Berisiko Attrition" if "Yes" in str(result) else "Aman (Tidak Attrition)"
                        
                except ImportError:
                    error_message = "Model module tidak ditemukan. Pastikan modelling.py sudah ada."
                except Exception as e:
                    error_message = f"Error dalam prediksi: {str(e)}"
                    print(traceback.format_exc())
        
        except Exception as e:
            error_message = f"Error memproses form: {str(e)}"
            print(traceback.format_exc())
    
    return render_template('form_prediction.html', 
                         prediction=prediction, 
                         probability=probability if 'probability' in locals() else None,
                         prediction_label=prediction_label,
                         error_message=error_message)

@app.route('/health')
def health():
    """Health check endpoint untuk deployment"""
    return jsonify({"status": "healthy", "message": "App is running"}), 200

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)