import tkinter as tk
import tkinter.ttk as ttk

class TtkScale(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        ttk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.showvalue = kwargs.pop('showvalue', True)
        self.tickinterval = kwargs.pop('tickinterval', 0)
        self.digits = kwargs.pop('digits', '0')
        
        if 'command' in kwargs:
            # add self.display_value to the command
            fct = kwargs['command']
            
            def cmd(value):
                fct(value)
                self.display_value(value)
                
            kwargs['command'] = cmd
        else:
            kwargs['command'] = self.display_value
            
        self.scale = ttk.Scale(self, **kwargs)
        
        # get slider length
        style = ttk.Style(self)
        style_name = kwargs.get('style', '%s.TScale' % (str(self.scale.cget('orient')).capitalize()))
        self.sliderlength = style.lookup(style_name, 'sliderlength', default=30)
        
        self.extent = kwargs['to'] - kwargs['from_']
        self.start = kwargs['from_']
        # showvalue
        if self.showvalue:
            ttk.Label(self, text=' ').grid(row=0)
            self.label = ttk.Label(self, text='0')
            self.label.place(in_=self.scale, bordermode='outside', x=0, y=0, anchor='s')
            self.display_value(self.scale.get())
            
        self.scale.grid(row=1, sticky='ew')
        
        # ticks
        if self.tickinterval:
            ttk.Label(self, text=' ').grid(row=2)
            self.ticks = []
            self.ticklabels = []
            nb_interv = round(self.extent/self.tickinterval)
            formatter = '{:.' + str(self.digits) + 'f}'
            for i in range(nb_interv + 1):
                tick = kwargs['from_'] + i * self.tickinterval
                self.ticks.append(tick)
                self.ticklabels.append(ttk.Label(self, text=formatter.format(tick)))
                self.ticklabels[i].place(in_=self.scale, bordermode='outside', x=0, rely=1, anchor='n')
            self.place_ticks()

        self.scale.bind('<Configure>', self.on_configure)
        
    def convert_to_pixels(self, value):
        return ((value - self.start)/ self.extent) * (self.scale.winfo_width()- self.sliderlength) + self.sliderlength / 2
        
    def display_value(self, value):
        # position (in pixel) of the center of the slider
        x = self.convert_to_pixels(float(value))
        # pay attention to the borders
        half_width = self.label.winfo_width() / 2
        if x + half_width > self.scale.winfo_width():
            x = self.scale.winfo_width() - half_width
        elif x - half_width < 0:
            x = half_width
        self.label.place_configure(x=x)
        formatter = '{:.' + str(self.digits) + 'f}'
        self.label.configure(text=formatter.format(float(value)))
    
    def place_ticks(self):
        # first tick 
        tick = self.ticks[0]
        label = self.ticklabels[0]
        x = self.convert_to_pixels(tick)
        half_width = label.winfo_width() / 2
        if x - half_width < 0:
            x = half_width
        label.place_configure(x=x)
        # ticks in the middle
        for tick, label in zip(self.ticks[1:-1], self.ticklabels[1:-1]):
            x = self.convert_to_pixels(tick)
            label.place_configure(x=x)
        # last tick
        tick = self.ticks[-1]
        label = self.ticklabels[-1]
        x = self.convert_to_pixels(tick)
        half_width = label.winfo_width() / 2
        if x + half_width > self.scale.winfo_width():
            x = self.scale.winfo_width() - half_width
        label.place_configure(x=x)
        
    def on_configure(self, event):
        """Redisplay the ticks and the label so that they adapt to the new size of the scale."""
        self.display_value(self.scale.get())
        if self.tickinterval:
            self.place_ticks()