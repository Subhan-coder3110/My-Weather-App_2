import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Entre City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.descrip_label = QLabel(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.descrip_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.descrip_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("City_label")
        self.city_input.setObjectName("City_input")
        self.get_weather_button.setObjectName("Get_weather_button")
        self.temperature_label.setObjectName("Temperature_label")
        self.emoji_label.setObjectName("Emoji_label")
        self.descrip_label.setObjectName("Description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;          
            }      
            QLabel#City_label{
                font-size: 40px;
                font-style: italic;                
            }
            QLineEdit#City_input{
                font-size: 40px;               
            }
            QPushButton#Get_weather_button{
                 font-size: 30px;
                 font-weight: bold;           
            }
            QLabel#Temperature_label{
                 font-size: 75px;
            }
            QLabel#Emoji_label{
                 font-size: 100px;
                 font-family: segoe UI emoji;            
            }
            QLabel#Description_label{
                 font-size: 50px;
            }                
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "87c6dc5ff77b4aa9fea5f282eafa6905"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as htttp_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unautherized\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable\nServer is down")
                case 504:
                    self.display_error("Gareway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{htttp_error}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your Internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out")
        except requests.exceptions.T00ManyRedirects:
            self.display_error("Too many Redirects\n Check the url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
     
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.descrip_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperture_k = data["main"]["temp"]
        temperture_c = temperture_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        
        self.temperature_label.setText(f"{temperture_c:.0f}°c")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.descrip_label.setText( weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌥️"    
        elif 500 <= weather_id <= 531:
            return "🌧️" 
        elif 600 <= weather_id <= 622:
            return "☀️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771 :
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"





if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())