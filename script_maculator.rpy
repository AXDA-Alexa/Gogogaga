# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define MC = Character("Sigma1", color="#fff176", ) 
define SC = Character("Sigma2", color="#ba68c8")

# The game starts here.

label start:
    "Here we go..."
    MC "I'm hungry."
    SC "Sybau, today we're going to learn about Dostoevsky and his novel \"Crime and Punishment\""

label sprites:
    MC "I am still hungry"
    show MC hungry with moveinleft
    SC "Go and eat smth then, we will discuss the mission later"
    show SC with moveinright
    
    #de adaugat dialog


label backround:
    scene bg louvre
    with fade 
    play music "Crowd noises.mp3" fadein 0.25 volume 0.5

    MC "Delicios, I like the ice cream here"
    show MC hungry                                                     #De schimbat sprite-ul!!!!!!!!!!!!!!!!
   
    SC "About the mission you should attend"
    show SC 

    MC "HOLY SMOKESSSSS-"
    show MC simple  
    
    stop music fadeout 1.0 

    #The sound of music should lower as the sprite dialoge will appear

label mission:
    scene night alley
    with fade

    MC "UGHGHHHHGFahgdhaa... how can she be so annoying"
    show MC simple          #add annoyed profile


    return
