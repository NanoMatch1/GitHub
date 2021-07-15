import blessed
import time

term = blessed.Terminal()

print(term.height, term.width)

print(term.number_of_colors)

print(term.green_reverse('to the moon'))
print(term.white_on_green('to the moon'))
print(term.red('to the moon'))
print(term.blue('to the moon'))
print(term.green('to the moon'))
print(term.purple_on_green('to the moon'))
print(term.white_on_purple('to the moon'))
print(term.white_on_firebrick3('system'))

print(term.bright_yellow('hay'))
# print(term.bright_purple('hay'))
print(term.bright_blue('hay'))


print(term.blink('OMG'))
print(term.underline_bold_green_on_yellow('omg'))

with term.fullscreen(), term.cbreak():
    print(term.home + term.aqua_on_magenta + term.clear)
    # print(term.white_on_fuchsia)
    # print(term.black)
    print(term.move_y(term.height // 2) + term.center('press any key').rstrip())
    # print(term.red('anoi'))

    term.inkey()

print(term.orangered)
print('yoyo')
print('yoasdyo')
print('yffffffffoyo')
print('yoygggggggggggggggo')
print(term.normal)
print('nrom')
print(term.on_fuchsia)
