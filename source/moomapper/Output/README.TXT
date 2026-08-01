Moo Mapper (for GTA III & Vice City) Beta 0.94
=====================================================

This is Delfi's (Jernej L.) generally fixed version of moomapper.

it contains not just gui changes.. see log:

update 1.2.2005
i added fixes to object rotations by PatrickW

i changed the about box layout a bit ;)

update 1.2.2005
settings dialog can now change col surface drawing colors

i speeded up coll rendering by reducing coll model searching 
count by storing its pointer once the coll is found

ipl path editing now shows gta-vc world internal coords instead unmultiplied path format.

update 31.1.2005
COL rendering mode support (only disk files right now, img cols support later (or never) )

update: 23.1.2005
texture view shows alpha names in the list too, and displays alpha transparency, 
you can now also control the background color of texture display.

the secondary view now also displays transparency, the alpha transparency 
checkbox has been now also fixed so you can toggle transparency.

i added projection control - you can set anything from almost orthogonal to extremely perspective, 
a reset button was added too.

the depth culling has been increased to 80000 meters, so you can now zoom out farther than before 
and it won't cut triangles, the limit os now good enough to do cool huge screenshoots.

the radar z level and projection trackbars now don't take focus so using mouse wheel to zoom view 
won't change them anymore.

the coordinates text box has been fixed - as long as it has focus it will not change.

i removed some redurnant calls in the rendering routines - it renders half milisecond faster :P
the debug log now displays actual errors while parsing text files if it finds any.

the FPS label has been moved to toolbar

Update: 14.1.2005
FULL path nodes editing support including mouse moving like you are used to do with objects.

i fixed a bug in kcow's code that made path files saved useless unless you did some 
fixing by hand, he mistaken some item count numbers..


Update: 13.1.2005
full zone and cullzone rendering, zones and paths picking routines are underway!
experimentaly added occl sections support, i have no clue what that occlu.ipl 
does but i want to render and see it..

the zones are see-trough in vice-city mode but not gta3 mode, i am still triying 
to figure out what causes this but i know one thing - that i would like to drop 
gta3 support in favour of san andreas support when it comes out.

some additions to the error checker

more gui changes like the toolbar on bottom of screen and some fixed dialog 
boxes are now sizeable - like texture preview window.


Update: 9.1.2005
*experimental cull and zone rendering
alpha opacity transparent faces now render transparent, so you 
can now see trough windows just like in the game!!


My brand new hard drive yesterday reached 49° from testing and the temperature was so 
high it seems, that it couldn't recalibrate to next day until it cooled down, i thought 
it broken and i lost all the changes in moomapper, that would be shame eh? so now i'll 
share the source code of today's latest version with you, i think it is stable enough right?


Update: 8.1.2005
i fixed a serious bug that made all IDE files saved with editor useless, 
the bug is present in all of my "fixed" releases
it has to do with text parser where i somehow managed to comment-out proper 
saving of the "unknown" number that was actualy dff model clump count 
(like damaged models for street lamps have 2 models in 1 file - multi clumps) was 
broken with implementing faster text parser.. these bugs can be now 
detected and fixed in moomapper's check for problems feature 
that was enchanged a lot, it can fix some easy errors and detect more of them, 
error reports are now also more descriptive.


Update: 6.1.2005

shows game name in title bar
redesigned ide, ipl... editors
path rendering!!
settings dialog with some advanced options
new menu & button icons :)


Update: 8.12.2004

multiple games support (YAY!)
fixes 32 bit image bug - green and blue were swaped
fixes 8 bit image issuses on ATI cards that don't 
  natively support palettized images
fixes radar scale issuses
some useul features like radar Z-height were added

TODO:
vertex prelightning
better alpha rendering

my contact info:
stdcall@gmail.com
http://www.gtatools.com

otherwise, original moomapper author is: 

       Name: KCow (Alastair Burr)
     E-Mail: moomapper@chronetal.co.uk
        WWW: http://www.chronetal.co.uk/gta/
