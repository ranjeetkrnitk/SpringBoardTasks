from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Ranjeet's MP3 Player")
#root.iconbitmap('')
root.geometry("500x450")

# initialize Pygame Mixer
pygame.mixer.init()

# Grab Song Length Time Info
def play_time():
    # Grab Current Song Time
    current_time = pygame.mixer.music.get_pos() / 1000
    
    # Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Get song length from Mutagen
    # Get Current Song
    current_song = song_box.curselection()
    song = song_box.get(current_song)

    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Output time to status bar
    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

    # Update Slider Position
    my_slider.config(value=int(current_time))

    # Update Time
    status_bar.after(1000, play_time)



#Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='songs/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # Strip File Info
    # song = song.replace("/Users/ranjeetkumar/SpringBoard/SelfProject/Mp3Player/songs/", "")
    # song = song.replace(".mp3", "")
    # Add Song to List Box
    song_box.insert(END, song)

# Add Many Songs to Playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='songs/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    
    # Loop throung Songs to replace directory info and mp3
    for song in songs:
        # Strip File Info
        # song = song.replace("/Users/ranjeetkumar/SpringBoard/SelfProject/Mp3Player/songs/", "")
        # song = song.replace(".mp3", "")
        # Add Song to List Box
        song_box.insert(END, song)

# Play selected song
def play():
    song = song_box.get(ACTIVE)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Call the Play Time Function to get Song Length. 
    play_time()

    # Update Slider to position
    slider_position = int(song_length)
    my_slider.config(to=slider_position, value=0)

# Stop playing Current Song
def stop():
    pygame.mixer.music.stop()
    #song_box.selection_clear(ACTIVE)

    # Clear the Status Bar
    status_bar.config(text='')

# Play Previous Song
def next_song():
    # get the Current Tuple Number
    next_one = song_box.curselection()
    # Add One to the Current Song Number
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    #Load and Play the Next Song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Move Active bar in Playlist
    song_box.selection_clear(0,END)
    song_box.activate(next_one)

    song_box.selection_set(next_one, last=None)

def previous_song():
    # get the Current Tuple Number
    prev_one = song_box.curselection()
    # Add One to the Current Song Number
    prev_one = prev_one[0] - 1
    song = song_box.get(prev_one)
    #Load and Play the Next Song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Move Active bar in Playlist
    song_box.selection_clear(0,END)
    song_box.activate(prev_one)

    song_box.selection_set(prev_one, last=None)


# Delete a Song
def delete_song():
    # Delete the Anchored Song
    song_box.delete(ANCHOR)
    # Stop Song if Playing
    pygame.mixer.music.stop()

def delete_all_songs():
    # Delete All the Songs
    song_box.delete(0,END)
    # Stop Song if Playing
    pygame.mixer.music.stop()
    pass

# Create Global Pause Variable
global paused
paused = False

# Pause and Unpause Current Song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Get Slider Function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


# Create Playlist Box
song_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# Define Player Control Buttons Images
back_btn_img = PhotoImage(file='icons/PNG/Previous.png',)
forward_btn_img = PhotoImage(file='icons/PNG/Next.png')
play_btn_img = PhotoImage(file='icons/PNG/Play.png')
pause_btn_img = PhotoImage(file='icons/PNG/Pause.png')
stop_btn_img = PhotoImage(file='icons/PNG/Stop.png')

# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()

# Create Player Controls
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu

my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)

# Add Many Songs to playlist
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_song)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All song from Playlist", command=delete_all_songs)


#Create Ststus Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Create Music Position Slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.pack(pady=30)

# Create Temp Slider Label
slider_label = Label(root, text="0")
slider_label.pack(pady=10)

root.mainloop()