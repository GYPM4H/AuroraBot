import numpy as np

def format_aurora_prob_message(probability):
    """
    Format a message containing the aurora probability.
    
    Args:
        probability (float): The aurora probability.
    
    Returns:
        str: A formatted message.
    """
    return f"🌌 The current aurora probability is {probability}%."

def format_kp_index_message(kp_index, timestamp):
    """
    Format a message containing the KP index and timestamp.
    
    Args:
        kp_index (float): The KP index.
        timestamp (str): The timestamp of the KP index data.
    
    Returns:
        str: A formatted message.
    """
    return f"⚠️ The current KP index is {kp_index} (Timestamp: {timestamp})."

def format_rx_index_message(rx_index_data):
    """
    Format a message containing the RX index data.
    
    Args:
        rx_index_data (dict): The RX index data for Tartu.
    
    Returns:
        str: A formatted message.
    """
    # Example message formatting logic
    # You may adjust this logic as per your use-case.
    
    latest_hour_rx = rx_index_data['latest_hour_rx']
    msg = (
        f"🧲 RX Index Data for {rx_index_data['city']}:\n"
        f"- Latest Hour RX: {latest_hour_rx['value']} ({latest_hour_rx['color']})\n"
        # Add more RX index data fields as per your needs...
    )
    return msg

def format_weather_message(cloud_density, 
                           weather_description, 
                           temperature_kelvin, 
                           humidity):
    """
    Format a message containing weather data.
    
    Args:
        cloud_density (float): The cloud density.
        weather_description (str): The weather description.
        temperature_kelvin (float): The temperature in Kelvin.
        humidity (float): The humidity.
    
    Returns:
        str: A formatted message.
    """
    # Convert temperature to Celsius for user-friendly messaging
    temperature_celsius = np.round(float(temperature_kelvin) - 273.15, 2)
    
    return (
        f"Weather Update:\n"
        f"☁️ - <b>Clouds density:</b> {cloud_density}%\n"
        f"🌤️ - <b>Weather:</b> {weather_description.capitalize()}\n"
        f"🌡️ - <b>Temperature:</b> {temperature_celsius:.2f}°C\n"
        f"💧 - <b>Humidity:</b> {humidity}%"
    )

def format_aurora_data_message(kp_index, 
                               timestamp, 
                               rx_index,
                               aurora_prob,  
                               color_emoji_map, 
                               cloud_density, 
                               weather_description, 
                               temperature_kelvin, 
                               humidity):
    """
    Format a message containing weather data.
    
    Args:
        kp_index (float): The KP index.
        timestamp (str): The timestamp of the KP index data.
        rx_index_data (dict): The RX index data for Tartu.
        aurora_prob (float): The aurora probability.
        color_emoji_map (dict): A dictionary mapping color codes to emojis.
        cloud_density (float): The cloud density.
        weather_description (str): The weather description.
        temperature_kelvin (float): The temperature in Kelvin.
        humidity (float): The humidity.
    
    Returns:
        str: A formatted message.
    """

    rx_now_color_code = rx_index['latest_hour_rx']['color']
    rx_now_emoji = color_emoji_map.get(rx_now_color_code, "❓")

    rx_min_color_code = rx_index['next_hour_min_rx']['color']
    rx_min_emoji = color_emoji_map.get(rx_min_color_code, "❓")

    rx_max_color_code = rx_index['next_hour_max_rx']['color']
    rx_max_emoji = color_emoji_map.get(rx_max_color_code, "❓")

    temperature_celsius = np.round(float(temperature_kelvin) - 273.15, 2)

    message_text = (
    f"📊 <b>Aurora Data:</b>\n"
    f"🕒 <b>Timestamp:</b> {timestamp} UTC\n\n"
    f"🌍 <b>Location:</b> Tartu, Estonia\n"
    f"📍 <b>Coordinates:</b> [58.38, 26.72]\n\n"
    f"🧲 <b>Magnetic Field Data:</b>\n\n"
    f"  • <b>Current RX:</b> {rx_index['latest_hour_rx']['value']} nT | Colour: {rx_now_emoji}\n\n"
    f"  • <b>Next Hour Min RX:</b> {rx_index['next_hour_min_rx']['value']} nT | Colour: {rx_min_emoji}\n\n"
    f"  • <b>Next Hour Max RX:</b> {rx_index['next_hour_max_rx']['value']} nT | Colour: {rx_max_emoji}\n\n\n"
    f"🌌 <b>Aurora Probability:</b> {aurora_prob}%\n\n"
    f"⚠️ <b>KP Index:</b> {kp_index}\n\n"
    f"🌤️ <b>Weather:</b> {weather_description}\n"
    f"🌡️ <b>Temperature:</b> {temperature_celsius}°C\n"
    f"☁️ <b>Clouds density:</b> {cloud_density}%\n"
    f"💧 <b>Humidity:</b> {humidity}%\n"
    )

    return message_text