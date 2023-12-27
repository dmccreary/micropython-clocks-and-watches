# Scale Test

def drawTime12h(hour, minute, x, y, width, height):
    # horizontal
    x1 = .73
    x2 = .73
    x3 = 3.0 # digit width
    x4 = 1.35
    x5 = .5
    x6 = .35
    x7 = 1.5
    x8 = .35
    x9 = .5 # colon width and height

    # vertical
    y1 = 5.31
    y2 = 1.58 # to top colon
    y3 = .68 # between colons

    total_width = x1 + x2 + 3*x3 + x4 + x5 + x6 + x7
    print("total width:", total_width)
    total_height = y1
    
    # calculate the scaling ratios
    x_scale = width / total_width
    y_scale = height / total_height 
    
    digit_width = x3 * x_scale
    digit_height = y1 * y_scale
    print("x scale:", x_scale, "y scale:", y_scale)
    
    if hour > 12:
        hour12 = hour - 12
    
    # hour tens
    if hour12 > 10:
        oled.rect(x,y,int(x1*x_scale),int(y1*y_scale))
        
    # hour ones x,y,w,h
    drawDigit(hour % 10, int((x + x1 + x2)*x_scale), y, int(x3*x_scale), int(y1*y_scale))
    
    # minute tens ones digit, x,y,w,h
    min_tens_x = int((x + x1 + x2 + x3 + x4)*x_scale)
    drawDigit(minute // 10, min_tens_x, y, int(x3*x_scale), int(y1*y_scale))
    
    # minute  ones x,y,w,h
    min_ones_x = int((x + x1 + x2 + 2*x3 + x4 + x5)*x_scale)
    drawDigit(minute % 10, min_ones_x, y, int(x3*x_scale), int(y1*y_scale))

    # draw colon
    colon_size = x9
    # top colon
    oled.rect(int((x+x1+x2+x3+x8)*x_scale), y+int(y2*y_scale), colon_size, colon_size)
    # bottom colon
    oled.rect(int((x+x1+x2+x3+x8)*x_scale), y+int((y2+y3)*y_scale), colon_size, colon_size)
    
    # AM/PM
    if hours < 12:
        am_pm_text = 'am'
    else:
        am_pm_text = 'pm'
    am_pm_x = min_ones_x + int((x3+x6)*x_scale)
    oled.text(am_pm_text, am_pm_x, y + int(y1*y_scale)) 

drawTime12h(hour, minute, 0, 0, 100, 50)
