import pandas as pd
import pickle as pk
import streamlit as st
import base64
from streamlit_option_menu import option_menu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"

#Creating a new option menu
with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["Home","Price Predict","About","Contact Us"],
        icons=["house-heart-fill","car-front-fill","info-circle-fill","envelope-heart-fill"],
        menu_icon=["list"],
        default_index=0,
        ) 
   
#Price Predict Option
    
if selected=="Price Predict":
    page_bg_img = get_base64_of_bin_file('images/pricebg.jpg')

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url({page_bg_img});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    model=pk.load(open('model.pkl','rb'))
    st.markdown("""
    <style>
    .gradient-title {
        font-size: 48px;
        font-family: 'Arial Black', sans-serif;
        background: linear-gradient(90deg, #FF69B4, #DA70D6, #8A2BE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
    }
    </style>
    <h1 class="gradient-title">USED CAR PRICE PREDICTOR</h1>
""", unsafe_allow_html=True)

    data=pd.read_csv('Cardetails.csv')

    def get_brand_name(car_name):
        car_name = car_name.split(' ')[0]
        return car_name.strip()
    data['name'] = data['name'].apply(get_brand_name)

    name = st.selectbox('Select Car Brand', data['name'].unique())
    year = st.slider('Car Manufactured Year', 1994,2024)
    km_driven = st.slider('No of kms Driven', 11,200000)
    fuel = st.selectbox('Fuel type',data['fuel'].unique())
    seller_type = st.selectbox('Seller  type',data['seller_type'].unique())
    transmission = st.selectbox('Transmission type',data['transmission'].unique())
    owner = st.selectbox('Seller  type',data['owner'].unique())
    mileage = st.slider('Car Mileage', 10,40)
    engine = st.slider('Engine CC', 700,5000)
    max_power = st.slider('Max Power', 0,200)
    seats = st.slider('No of Seats', 5,10)

    st.markdown("""
        <style>
        div.stButton > button {
            font-size: 70px;
            padding: 10px 60px;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("PREDICT"):
        input_data_models = pd.DataFrame(
        [[name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,seats]],
        columns=['name','year','km_driven','fuel','seller_type','transmission','owner','mileage','engine','max_power','seats'])
    
        input_data_models['owner'].replace(['First Owner', 'Second Owner', 'Third Owner',
            'Fourth & Above Owner', 'Test Drive Car'],
                           [1,2,3,4,5], inplace=True)
        input_data_models['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'],[1,2,3,4], inplace=True)
        input_data_models['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'],[1,2,3], inplace=True)
        input_data_models['transmission'].replace(['Manual', 'Automatic'],[1,2], inplace=True)
        input_data_models['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
            'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
            'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
            'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
            'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
                          [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
                          ,inplace=True)

        car_price = model.predict(input_data_models)

        st.markdown(f"<h1 style='font-size:30px; color:white;'>Car Price is going to be ₹{car_price[0]}</h1>", unsafe_allow_html=True)

#Home 
if selected=="Home":
   
    page_bg_img = get_base64_of_bin_file('images/homebg.jpg')

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url({page_bg_img});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
        )
    
    st.markdown("<h1 style='text-align: left; font-family: Arial black; font-size: 40px; color: white'>Empowering Choices with<br><span style='color: limegreen'>Price Insights</span></h1>", unsafe_allow_html=True)
    

#About Page
if selected == "About":
    page_bg_img = get_base64_of_bin_file('images/aboutbg.jpg')

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url({page_bg_img});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1 style='text-align: left; color: white;'>ABOUT</h1>", unsafe_allow_html=True)

    st.markdown("""
    <h6 style='text-align: justify; font-size: 18px; color: white;'>
        Welcome to our Used Car Price Prediction App, your reliable companion for making informed decisions in the used car market. Our application leverages advanced machine learning algorithms and comprehensive data analysis to predict the market value of used cars accurately.
    </h6>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align: left; font-family: Arial black; font-size: 25px; color: white;'>
        Our<span style='color: limegreen'> Mission</span>
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: justify; font-size: 18px; color: white;'>
        <strong>Empowering Choices with Price Insights</strong><br>
        We aim to empower users by providing transparent, data-driven price insights that help buyers and sellers make informed decisions. Whether you're looking to buy a used car at a fair price or sell your vehicle with confidence, our app is designed to meet your needs.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align: left; font-family: Arial black; font-size: 25px; color: white;'>
        Key<span style='color: limegreen'> Features</span>
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <ul style='text-align: justify; color: white; font-size: 18px;'>
        <li><strong>Accurate Predictions:</strong> Our machine learning models are trained on extensive datasets to ensure precise price predictions.</li>
        <li><strong>User-Friendly Interface:</strong> Easily input your car's details and get instant price estimates.</li>
        <li><strong>Comprehensive Data:</strong> Our app considers a wide range of factors, including make, model, year, mileage, condition, and market trends.</li>
        <li><strong>Real-Time Updates:</strong> Stay up-to-date with the latest market values and trends.</li>
        <li><strong>Comparative Analysis:</strong> Compare prices across different models and regions to find the best deals.</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color: limegreen;'>How It Works</h2>", unsafe_allow_html=True)

    st.markdown("""
    <ol style='text-align: justify; color: white; font-size: 18px;'>
        <li><strong>Input Vehicle Details:</strong> Enter specific details about the car, such as make, model, year, mileage, and condition.</li>
        <li><strong>Data Processing:</strong> Our algorithm processes the input data and compares it with historical sales data and current market trends.</li>
        <li><strong>Price Prediction:</strong> The app provides a predicted price range, giving you a clear understanding of the car's market value.</li>
        <li><strong>Decision Support:</strong> Use the predicted price to negotiate better deals, whether buying or selling.</li>
    </ol>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color: limegreen;'>Why Choose Us?</h2>", unsafe_allow_html=True)

    st.markdown("""
    <ul style='text-align: justify; color: white; font-size: 18px;'>
        <li><strong>Accuracy:</strong> We use state-of-the-art machine learning techniques to deliver reliable price estimates.</li>
        <li><strong>Transparency:</strong> Our predictions are backed by data, ensuring transparency and trust.</li>
        <li><strong>Convenience:</strong> Get price predictions anytime, anywhere, without the need for manual research.</li>
        <li><strong>Expertise:</strong> Our team comprises experienced data scientists and automotive industry experts dedicated to providing the best service.</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color: limegreen;'>Contact Us</h2>", unsafe_allow_html=True)

    st.markdown("""
    <h4 style='text-align: justify; color: white; font-size: 18px;'>
        If you have any questions, feedback, or need assistance, please don't hesitate to reach out to us at [contact information]. We're here to help you make the best choices in the used car market.
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: justify; color: white; font-size: 18px;'>Thank you for choosing our Used Car Price Prediction App. We look forward to assisting you in your journey to buy or sell used cars with confidence.</h4>", unsafe_allow_html=True)

#Contact Us Page
if selected == "Contact Us":
 
    st.title("Contact Me")
    with st.form(key='contact_form'):
        st.subheader("We'd love to hear from you!")
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        emailFlag = False

        # Email validation
        if email:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(email_pattern, email):
                emailFlag = True
            else:
                emailFlag = False
                st.error("Invalid email address. Please try again.")

        submit_button = st.form_submit_button("Send")

        if submit_button and emailFlag:
            receiver_email = "sharanrollins.690@gmail.com"
            sender_email = "sharanrollins.690@gmail.com"
            password = "tvcq rdky uenf pudg"

            subject = "Mail from Value Wheels"
            body = f"""
            <html>
            <body>
                <h2>Mail from Value Wheels</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong><br>{message}</p>
            </body>
            </html>
            """
            try:
                message_obj = MIMEMultipart()
                message_obj["From"] = sender_email
                message_obj["To"] = receiver_email
                message_obj["Subject"] = subject
                message_obj.attach(MIMEText(body, "html"))

                with st.spinner("Sending your email..."):
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.send_message(message_obj)

                st.success(f"Thank you, {name}! Your message has been sent successfully. We will get back to you soon.")
            except smtplib.SMTPAuthenticationError:
                st.error("Authentication failed. Please check your email and password.")
            except smtplib.SMTPException as e:
                st.error(f"SMTP error occurred: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# Adding footer at the bottom of the page content
def add_footer():
    footer = """
    <style>
    .footer {
        width: 100%;
        height: 5%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-size: 13px;
        position: fixed;  
        bottom: 0;
        left:0;
    }
    </style>
    <div class="footer">
        <p>© 2024 Sharan. All rights reserved. | Built with ❤️ using Streamlit</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# Call this function in your Streamlit app wherever appropriate
if selected != "Home" and selected != "Price Predict":
    add_footer()
