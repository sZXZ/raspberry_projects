import prometheus_client
from miio import AirPurifierMiot
from py.utils import code_secrets

def main():
    prometheus_client.start_http_server(8000)
    air = AirPurifierMiot(ip=code_secrets.MIAIR["ip"], token=code_secrets.MIAIR["token"], model='zhimi.airp.rmb1')
    aqi = prometheus_client.Gauge('aqi', 'air quality 0-1000')
    humidity = prometheus_client.Gauge('humidity', 'relative humidity 0-100')
    temperature = prometheus_client.Gauge('temperature', 'temperature')
    motor_speed = prometheus_client.Gauge('motor_speed', 'rpm of the unit')
    while True:
        try:
            status = air.status()
            aqi.set(int(status.aqi))
            humidity.set(int(status.humidity))
            temperature.set(int(status.temperature))
            motor_speed.set(int(status.motor_speed))
        except Exception as ex:
            print(ex)
    
if __name__ == "__main__":
    main()
