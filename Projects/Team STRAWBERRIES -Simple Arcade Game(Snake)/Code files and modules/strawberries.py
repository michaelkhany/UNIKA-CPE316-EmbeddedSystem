
def display(screen):
    screen.fill(0)
    screen.text("stra",0,0,1)
    screen.text("wber",0,7,1)
    screen.text("ries",0,15,1)
    screen.pixel(8,31,1)
    screen.pixel(9,31,1)
    screen.pixel(7,30,1)
    screen.pixel(8,30,1)
    screen.pixel(9,30,1)
    screen.pixel(10,30,1)
    screen.pixel(6,29,1)
    screen.pixel(7,29,1)
    # screen.pixel(8,29,1)
    screen.pixel(9,29,1)
    screen.pixel(10,29,1)
    screen.pixel(11,29,1)
    screen.pixel(6,28,1)
    screen.pixel(7,28,1)
    screen.pixel(8,28,1)
    screen.pixel(9,28,1)
    screen.pixel(10,28,1)
    screen.pixel(11,28,1)
    for i in range(5,13):
        screen.pixel(i,27,1)
        screen.pixel(i,26,1)
    for i in range(6,12):
        screen.pixel(i,25,1)
    screen.pixel(8,24,1)
    screen.pixel(9,24,1)
    screen.pixel(7,23,1)
    screen.pixel(6,23,1)
    screen.pixel(7,22,1)
    screen.pixel(10,23,1)
    screen.pixel(10,27,0)
    screen.pixel(7,26,0)
    screen.show()
    
