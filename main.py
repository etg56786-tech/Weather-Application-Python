import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import country_converter as coco


class WeatherApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.city = QLabel("WeatherApp:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather!", self)
        self.temp_widget = QLabel( self)
        self.feels_like = QLabel( self)
        self.weather_icon = QLabel( self)
        self.weather_description = QLabel(self)
        self.country_name = QLabel(self)
        self.trademark = QLabel("Made by Ethan Chen!", self)
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("Ethan's Weather Application")
        self.setWindowIcon(QIcon('C:/Users/ethan/downloads/EasilyPythonic LOgo'))
        self.city_input.setPlaceholderText("Enter City Name:")
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.city)
        v_layout.addWidget(self.city_input)
        v_layout.addWidget(self.get_weather_button)
        v_layout.addWidget(self.temp_widget)
        v_layout.addWidget(self.feels_like)
        v_layout.addWidget(self.weather_icon)
        v_layout.addWidget(self.weather_description)
        v_layout.addWidget(self.country_name)
        v_layout.addWidget(self.trademark)

        self.setLayout(v_layout)
        self.city.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_widget.setAlignment(Qt.AlignCenter)
        self.feels_like.setAlignment(Qt.AlignCenter)
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_description.setAlignment(Qt.AlignCenter)
        self.trademark.setAlignment(Qt.AlignCenter)
        self.country_name.setAlignment(Qt.AlignCenter)

        self.city.setObjectName("city")
        self.city_input.setObjectName("city_input")
        self.temp_widget.setObjectName("temp_widget")
        self.weather_icon.setObjectName("weather_icon")
        self.weather_description.setObjectName("weather_description")
        self.get_weather_button.setObjectName("get_weather_button")
        self.feels_like.setObjectName("feels_like")
        self.country_name.setObjectName("country_name")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Montserrat;
                font-weight: bold;
                }
            QLabel#city{
                font-family: Montserrat;
                font-weight: bold;
                font-size: 40px;
                background-color: light purple;
                border: 1px solid black;
                border-radius: 10px;
                }
            QPushButton#get_weather_button{
                font-family: Montserrat;
                font-style: Bold;
                font-size: 30px;
                border: 1px solid black;
                border-radius: 10px;
                background-color: hsl(247, 88%, 83%);                
                }
            QLineEdit#city_input{
                font-size: 67px;
                border: 6px solid black;
                border-radius: 10px;
                }
            QLabel#temp_widget{
                font-size: 40px;
                font-family: Segoe UI emoji;
                }
            QLabel#feels_like{
                font-size: 18px;
                border: 2px solid purple;
                background-color: hsl(275, 79%, 81%);
                }
            QLabel#country_name{
                font-size: 15px;
                font-weight: bold;
                }
            QLabel#weather_icon{
                font-size: 105px;
                font-family: Noto Color Emoji;
                border: 1px solid blue;
                }
            QLabel#weather_description{
                font-size: 35px;
                font-weight: bold;
                background-color: hsl(266, 53%, 81%);
                border: 3px solid black;
                
                }
            QPushButton#get_weather_button:hover{
                background-color: hsl(246, 100%, 91%);
            }
            QLabel#trademark{
                "font-weight: bold;"
                }
                
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        api = "d46a1d366bec101dd915ac61155d5e9b"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"


        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_err:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request, check your input?")
                case 401:
                    self.display_error("Unauthorized access, check your API key?")
                case 403:
                    self.display_error("Forbidden, check your API key?")
                case 404:
                    self.display_error("Not found, check your input?")
                case 500:
                    self.display_error("Internal Server Error, try again later?")
                case 502:
                    self.display_error("Bad Gateway, try again later?")
                case 503:
                    self.display_error("Server is down")
                case 504:
                    self.display_error("Gateway Timeout, try again later?")
                case _:
                    self.display_error(f"HTTP Error, {http_err}")
        except requests.exceptions.ConnectionError as connection_err:
            self.display_error("Connection Error, check your internet?")
        except requests.exceptions.Timeout as timeout_err:
            self.display_error("Timeout Error, check your input?")
        except requests.exceptions.RequestException as request_err:
            self.display_error(f"Request Error, check your input?, {request_err}")
    def display_error(self, message):
        self.temp_widget.setStyleSheet("font-size: 40px;")
        self.temp_widget.setText(message)
        self.weather_icon.setText("?")
        self.weather_description.setText("Nothing")
        self.feels_like.setText("?")
    def display_weather(self, data):
        print(data)
        temperature = (data["main"]["temp"] * 9/5) - 459.67
        self.temp_widget.setText(f"{temperature:.0f}° F")
        self.temp_widget.setStyleSheet("font-size: 65px;")
        feels_like = (data["main"]["feels_like"] * 9/5) - 459.67
        self.feels_like.setText(f"Feels like: {feels_like:.0f}° F")
        weather_id = data["weather"][0]["id"]
        weather_desc = data["weather"][0]["description"]
        self.weather_description.setText(f"{weather_desc.capitalize()} at {self.city_input.text().capitalize()}")
        country = coco.convert(names=data["sys"]["country"], to="name")
        self.country_name.setText(f"📍 Located in {country}")
        self.weather_icon.setText(self.get_weather_img(weather_id))


    @staticmethod
    def get_weather_img(weather_id):
        match weather_id:
            case _ if 200 <= weather_id < 300:
                return "⛈️"
            case _ if 300 <= weather_id < 400:
                return "🌦️"
            case _ if 500 <= weather_id < 600:
                return "🌧️"
            case _ if 600 <= weather_id < 700:
                return "🌨️"
            case _ if 700 <= weather_id < 800:
                return "🌫️"
            case _ if weather_id == 800:
                return "☀️"
            case _ if 800 <= weather_id < 900:
                return "☁️"
            case _:
                return ""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApplication()
    window.show()
    sys.exit(app.exec_())
