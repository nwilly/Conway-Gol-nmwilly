# -*- coding: utf-8 -*-

import tkinter as tk

import math
import random
import time
import gol_board
import image_utility as imgu


class gol_gui:
    '''Class creates and manages GUI and unser input


    attributes:
        main_window, the top level Tk frame
        canvas, the Canvas object created in main_window
        current, the time point currently being displayed
        timeline, the bottom slider in main_window which controls current
        scale, how many pixels in the display are used per board cell
        generations, the number of generations currently calculated
        gol, gol_board object containing info on the current simulation
        imgs, list of PhotoImage which are then drawn to canvas
        display, reference to the PhotoImage currently drawn
    '''

    def __init__(self):
        '''Initial app setup.  Create and populate main window and load the
        title screen map using default values.

        NOTE: the code is not as fast as I would want, so on some computers
        opeining the title screen may be egregious.  I tried to choose settings
        that won't take any time to run but that was only tested on my
        computer.
        '''

        # setup main_window
        self.main_window = tk.Tk()
        self.__init_menu__()
        self.canvas = tk.Canvas(self.main_window)
        self.canvas.pack()
        self.timeline = tk.Scale(self.main_window,
                                 from_=1, to=100,
                                 orient='horizontal',
                                 command=self.timeline_update)
        self.timeline.pack()

        # set default values and open/runS title_creen.gif'
        self.scale = 1
        self.generations = 32
        self.open_img('./maps/title_screen.gif')
        self.main_window.mainloop()

    def __init_menu__(self):
        '''Create the menu and associates those buttons with commands'''

        # reference for convenience
        root = self.main_window

        menu = tk.Menu(root)
        root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New', command=self.new_dialog)
        filemenu.add_command(label='Open...', command=self.browse_img)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=root.destroy)
        viewmenu = tk.Menu(menu)
        menu.add_cascade(label='View', menu=viewmenu)
        viewmenu.add_command(label='Settings', command=self.setting_dialog)

    def new_dialog(self):
        '''Create the dialog box that appears when you click file->new in
        the menu.

        This window allows you to create random starting states with
        dimension height x width.  Each pixel is set to be alive using the
        specified probability.  The simulation is run to the specified number
        of generations.  You may specify a random seed; a random seed is
        provided. The values are accessible by querying the attribute reference
        self.top and searching its children.  The function rand_img is called
        when ok_butt is clicked.'''
        top = tk.Toplevel()

        self.top = top
        top.title('Random Game')

        # create parameter labels
        tk.Label(top, text='Width: ').grid(row=0, column=0, sticky='e')
        tk.Label(top, text='Height: ').grid(row=1, column=0, sticky='e')
        tk.Label(top, text='Probability: ').grid(row=2, column=0, sticky='e')
        tk.Label(top, text='Generations: ').grid(row=3, column=0, sticky='e')
        tk.Label(top, text='Seed: ').grid(row=4, column=0, sticky='e')

        # create input elements
        w_scale = tk.Scale(top, from_=1, to=128,
                           orient='horizontal', name='w_scale')
        w_scale.grid(row=0, column=1)
        w_scale.set(32)

        h_scale = tk.Scale(top, from_=1, to=128,
                           orient='horizontal', name='h_scale')
        h_scale.grid(row=1, column=1)
        h_scale.set(32)
        self.h_scale = h_scale

        prob_scale = tk.Scale(top, from_=0, to=1, orient='horizontal',
                              resolution=0.01, name='prob_scale')
        prob_scale.set(0.5)
        prob_scale.grid(row=2, column=1)
        self.prob_scale = prob_scale

        gen_scale = tk.Scale(top, from_=1, to=512, name='gen_scale')
        gen_scale.config(orient='horizontal')
        gen_scale.set(64)
        gen_scale.grid(row=3, column=1)

        seed_entry = tk.Entry(top, name='seed_entry')
        seed_entry.insert(0, str(int(random.random()*10**6)))
        seed_entry.grid(row=4, column=1)

        # create ok and cancel buttons
        ok_butt = tk.Button(top, text='Ok', command=self.rand_image)
        ok_butt.grid(row=5, column=1)

        cancel_butt = tk.Button(top, text='cancel', command=top.destroy)
        cancel_butt.grid(row=5, column=0)

    def rand_image(self):
        '''Take the information given in the dialog created in new_dialog and
        makes a new, random simulation.

        It first checks if a valid seed value was given.  If not, an error
        window appears.  If the seed value was valid, it create a new
        simulation from a random board.  It then closes the dialog from
        new_dialog.
        '''

        if self.top.nametowidget('seed_entry').get().isdigit() is False:
            tk.messagebox.showerror('Error',
                                    'Seed value must be a positive integer.')
            return

        x = int(self.top.nametowidget('w_scale').get())
        y = int(self.top.nametowidget('h_scale').get())
        self.generations = int(int(self.top.nametowidget('gen_scale').get()))
        p = float(self.top.nametowidget('prob_scale').get())
        seed = int(self.top.nametowidget('seed_entry').get())

        board = imgu.create_random_board(x, y, p, seed)
        self.new_start_board(board, self.generations)
        self.top.destroy()

    def setting_dialog(self):
        '''Create the settings dialog which allows you to re-run the current
        simulation under different settings.

        Reference to this window is saved as self.top.  You can set the
        boundary condition, the born numbers, the survive numbers, the number
        of generations claculated, and the neighborhood radius. Upon clicking
        ok_butt, this runs set_settings.
        '''

        top = tk.Toplevel()
        self.top = top

        # This is a reference to the state of the bc radio button.  Used in
        # set_settings.
        self.bc_var = tk.StringVar()

        rb1 = tk.Radiobutton(top, text='Torus', variable=self.bc_var,
                             value='torus')
        rb1.select()
        rb2 = tk.Radiobutton(top, text='Dead', variable=self.bc_var,
                             value='dead')
        rb1.grid(row=0, column=1)
        rb2.grid(row=1, column=1)

        # Create parameter labels
        tk.Label(top, text='Boundary Condition').grid(row=0, column=0)

        tk.Label(top, text='Born Numbers:').grid(row=2, column=0, sticky='e')
        tk.Label(top, text='Survive Numbers:').grid(row=3,
                                                    column=0, sticky='e')
        tk.Label(top, text='Generations: ').grid(row=4, column=0, sticky='e')
        tk.Label(top, text='Neighborhood Radius: ').grid(row=5,
                                                         column=0, sticky='e')

        # Create parameter entry points and set default values
        born_entry = tk.Entry(top, name='born_entry')
        born_entry.insert(0, '3')
        born_entry.grid(row=2, column=1)

        born_entry = tk.Entry(top, name='survive_entry')
        born_entry.insert(0, '2, 3')
        born_entry.grid(row=3, column=1)

        gen_scale = tk.Scale(top, from_=1, to=512, name='gen_scale')
        gen_scale.config(orient='horizontal')
        gen_scale.set(64)
        gen_scale.grid(row=4, column=1)

        rad_scale = tk.Scale(top, from_=1, to=5, name='rad_scale')
        rad_scale.config(orient='horizontal')
        rad_scale.set(1)
        rad_scale.grid(row=5, column=1)

        # Create ok and cancel buttons.
        ok_butt = tk.Button(top, text='Ok', command=self.set_settings)
        ok_butt.grid(row=6, column=1)

        cancel_butt = tk.Button(top, text='cancel', command=top.destroy)
        cancel_butt.grid(row=6, column=0)

    def set_settings(self):
        '''Take parameters given in the settings dialog box and re-run the
        current simulation.

        If the born or survive numbers are not in a appropriate format (a
        sequence of intergers seperated by commas) an error window will appear.
        The settings dialog box is destroyed afterwards.'''

        born = self.top.nametowidget('born_entry').get()
        born = self.string2list(born)

        survive = self.top.nametowidget('survive_entry').get()
        survive = self.string2list(survive)

        if born is None or survive is None:
            tk.messagebox.showerror('Error',
                                    'Born numbers and survive number(s) must \
                                    be integers seperated with commas.')
            return

        self.gol.boundary_condition = self.bc_var.get()
        self.gol.k_radius = int(self.top.nametowidget('rad_scale').get())
        self.gol.generations = int(self.top.nametowidget('gen_scale').get())
        self.gol.born_numbers = born
        self.gol.survive_numbers = survive

        self.gol.run()
        board = self.gol.states[0]

        self.scale = self.set_img_scale(board)
        self.imgs = imgu.all_board2img(self.gol.states)
        self.draw_img(self.imgs[0])
        self.current = 0

        self.update_canvas(board)
        self.timeline.config(to=len(self.imgs),
                             length=self.display.width())
        self.timeline.pack()

        self.top.destroy()

    def open_img(self, path):
        '''Load an image from location path and use it to start a new sim.
        Throws TclError if file is not found and does nothing.

        inputs:
            path, string loacting the file path
        '''

        try:
            img = tk.PhotoImage(file=path)
        except tk.TclError:
            return

        board = imgu.img2board(img)

        self.new_start_board(board, self.generations)

    def browse_img(self):
        '''Select an image from a file browser and use it tostart a new sim.'''

        filetypes = (('gif images', '*.gif'), ('all files', '*.*'))

        path = tk.filedialog.askopenfilename(initialdir='./maps',
                                             title='Select File',
                                             filetypes=filetypes)
        if path is None:
            return
        img = tk.PhotoImage(file=path)
        board = imgu.img2board(img)
        self.new_start_board(board, self.generations)

    def play(self, loop, delay):
        '''Display all images in self.imgs in sucession.

        inputs:
            loop, boolean if True, the current frame loops
            delay, float number of seconds to delay between renders
        '''

        t = self.current
        self.playing = True
        while(t < len(self.gol.states)):

            self.draw_img(self.imgs[t])
            self.timeline.set(int(t+1))

            t += 1
            self.current = t
            if(loop and t == len(self.gol.states)):
                t = 0

            time.sleep(delay)

            if self.playing is False:
                break

    def new_start_board(self, board, generations):
        '''Run a new sim from starting state board, and performs all GUI
        updates necessary.

        inputs:
            board, 2d list the new starting state
            generations, int the number of generations to run the sim
        '''

        self.scale = self.set_img_scale(board)
        self.gol = gol_board.gol_board(board, generations)
        self.imgs = imgu.all_board2img(self.gol.states)
        self.draw_img(self.imgs[0])
        self.current = 0

        self.update_canvas(board)
        self.timeline.config(to=len(self.imgs),
                             length=self.display.width())
        self.timeline.pack()

    def timeline_update(self, t):
        '''Update the drawn image whenever the timeline slider is moved.'''

        self.draw_img(self.imgs[int(t)-1])
        self.current = int(t)-1

    def update_canvas(self, board):
        '''Adjust the size of canvas based on the size of 2d list board.

        Use set_img_scale to get a good scale from current sim and screen sizes

        input:
            board, 2d list a state from the new sim
        '''

        scale = self.set_img_scale(board)
        size = self.get_size(board)

        self.canvas.config(width=size[1]*scale,
                           height=size[0]*scale)
        self.canvas.pack()

    def draw_board(self, board):
        '''Convert board to an img and draw it to the canvas.

        input:
            board, 2d list
        '''
        img = imgu.board2img(board)
        self.draw_img(img)

    def draw_img(self, img):
        '''Draw img to the canvas.

        input:
            img, PhotoImage
        '''

        self.canvas.delete('all')
        self.display = img.zoom(x=self.scale, y=self.scale)
        self.canvas.create_image(0, 0, image=self.display, anchor=tk.NW)
        self.canvas.update()

    def set_img_scale(self, board):
        '''Calculate appropriate image scaling to use based on sim size and
        screen reoslution.

        Scale is calculated such that the canvas is not wider than the screen
        nor is it taller than 75% of the screen.

        input:
            board, 2d list
        '''

        root = self.main_window
        size = self.get_size(board)

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        self.scale = min(math.floor(width/size[1]),
                         math.floor(height*.75/size[0]))

        self.scale = max(self.scale, 1)

        return self.scale

    def get_size(self, board):
        '''Convenience function, return dimension of 2d list'''
        return [len(board), len(board[0])]

    def string2list(self, s):
        '''Take a string and try to return a list of ints.

        s is expected to be a sequence of integers separated by a comma and
        optionally a space.

        inputs:
            s, string
        output:
            lst, a list of ints or, if an error was hit, None
        '''

        s = s.replace(' ', '')
        s = s.split(',')
        try:
            lst = [int(i) for i in s]
        except ValueError:
            print('Non-integer input')
            return None

        return lst
