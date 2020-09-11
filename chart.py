import array
from datetime import datetime
import sys
import random

# Pass any command line argument for Web use
# if len(sys.argv) > 1: # if there is use the Web Interface
#     import PySimpleGUIWeb as sg
#     mode = "web"
#     mysize = (20,2)
# else: # default uses the tkinter GUI
import PySimpleGUI as sg
mode = "tkinter"
mysize = (12,1)

from threading import Thread

STEP_SIZE = 1  # can adjust for more data saved than shown
SAMPLES = 100 # number of point shown on the chart
SAMPLE_MAX = 100 # high limit of data points
CANVAS_SIZE = (1000, 600)
LABEL_SIZE = (1000,20)

# create an array of time and data value
pt_values = []
pt_times = []
for i in range(SAMPLES+1): 
    pt_values.append("")
    pt_times.append("")


def main():

    timebar = sg.Graph(LABEL_SIZE, (0, 0),(SAMPLES, 20), background_color='white', key='times')
    graph = sg.Graph(CANVAS_SIZE, (0, 0), (SAMPLES, SAMPLE_MAX),
          background_color='black', key='graph')

    layout = [
        [sg.Quit(button_color=('white', 'red')),sg.Button(button_text="Print Log", button_color=('white', 'green'),key="log"),
         sg.Text('     ',  key='output')],
        [graph],
        [timebar],
    ]
    if mode == 'web':
        window = sg.Window('Pi Trend Chart', layout,
                       web_ip='192.168.0.107', web_port = 8888, web_start_browser=False)
    else:
        window = sg.Window('Pi Trend Chart', layout)

    graph = window['graph']
    output = window['output']

    i = 0
    prev_x, prev_y = 0, 0

    while True: # the Event Loop

        event, values = window.read(timeout=1000)
        if event in ('Quit', None):  # always give ths user a way out
            break
        if event in ('log'): # print the recorded time/data arrays
            print("\nReal Time Data\n")
            for j in range(SAMPLES+1):
                if pt_times[j] == "": #only print updated info
                    break
                print (pt_times[j], pt_values[j])

        # Get data point and time
        data_pt = random.randint(0, 100)
        now = datetime.now()
        now_time = now.strftime("%H:%M:%S")
        # update the point arrays
        pt_values[i] = data_pt       
        pt_times[i] = str(now_time) 

        window['output'].update(data_pt)
        
        if data_pt > SAMPLE_MAX:
            data_pt = SAMPLE_MAX
        new_x, new_y = i, data_pt

        if i >= SAMPLES:
            # shift graph over if full of data
            graph.move(-STEP_SIZE, 0)
            prev_x = prev_x - STEP_SIZE
            # shift the array data points
            for i in range(SAMPLES):
                pt_values[i] = pt_values[i+1]
                pt_times[i] = pt_times[i+1]
                    
        graph.draw_line((prev_x, prev_y), (new_x, new_y), color='red')
        
        prev_x, prev_y = new_x, new_y
        i += STEP_SIZE if i < SAMPLES else 0
    
        
        timebar.erase()
        # add a scrolling time value 
        time_x = i
        timebar.draw_text(text=str(now_time), location=((time_x - 2),7) )
        # add some extra times
        if i >= SAMPLES:
            timebar.draw_text(text=pt_times[int(SAMPLES * 0.25)], location=((int(time_x * 0.25) - 2),7) )
            timebar.draw_text(text=pt_times[int(SAMPLES * 0.5)], location=((int(time_x * 0.5) - 2),7) )
            timebar.draw_text(text=pt_times[int(SAMPLES * 0.75)], location=((int(time_x *0.75) - 2),7) )
        if i > 10:
            timebar.draw_text(text=pt_times[1], location=( 2,7) )
        
    window.close()


if __name__ == '__main__':
    main()