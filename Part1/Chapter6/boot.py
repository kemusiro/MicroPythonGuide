MYBOARD = "pico"

if MYBOARD == "pico":
    import common.config.pico as config
elif MYBOARD == "picow":
    import common.config.picow as config
elif MYBOARD == "esp32":
    import common.config.esp32 as config
