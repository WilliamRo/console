# Copyright 2020 William Ro. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
# This file incorporates work covered by the following copyright and
# permission notice:
#
#   Copyright (c) 2008-2011 Volvox Development Team
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to
#   deal in the Software without restriction, including without limitation the
#   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#   sell copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#   IN THE SOFTWARE.
#
#   Author: Konstantin Lepa <konstantin.lepa@gmail.com>
# ====-==================================================================-======
"""Methods for printing colored symbols, may be with special attributes.

This module depends on termcolor package.
See https://pypi.org/project/termcolor/

Examples:
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from termcolor import colored, cprint

# The lines below will yield exactly the same outputs
cprint('Hello, World!', 'red', 'on_cyan')
write_line('Hello, World!', 'red', 'on_cyan')
write_line('#{Hello, World!}{red}{on_cyan}')

# The lines below will yield exactly the same outputs
print(colored('Hello', 'red') + ', ' + colored('World', 'green') + '!')
write_line('#{Hello}{red}, #{World}{green}!')
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
import os
import re
import time
from sys import stdout


__all__ = ['parse', 'write_line', 'write', 'clear_line']

fancy_text = True


# region: Code from termcolor.py

ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            list(range(1, 9))
            ))
        )
del ATTRIBUTES['']


HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            list(range(40, 48))
            ))
        )


COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 38))
            ))
        )


RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if all([color is None, on_color is None, attrs is None]): return text
    if os.getenv('ANSI_COLORS_DISABLED') is None and fancy_text:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text

# endregion: Code from termcolor.py

# region: Enumerates

class TextColors:
  GREY = 'grey'
  RED = 'red'
  GREEN = 'green'
  YELLOW = 'yellow'
  BLUE = 'blue'
  MAGENTA = 'magenta'
  CYAN = 'cyan'
  WHITE = 'white'

class TextHighlights:
  ON_GREY = 'on_grey'
  ON_RED = 'on_red'
  ON_GREEN = 'on_green'
  ON_YELLOW = 'on_yellow'
  ON_BLUE = 'on_blue'
  ON_MAGENTA = 'on_magenta'
  ON_CYAN = 'on_cyan'
  ON_WHITE = 'on_white'

class Attributes:
  BOLD = 'bold'
  DARK = 'dark'
  UNDERLINE = 'underline'
  BLINK = 'blink'
  REVERSE = 'reverse'
  CONCEALED = 'concealed'

# endregion: Enumerates

# region: Private Methods

def _render(text, *args):
  """Renders text using colored.

  Arguments in the back, if exist, will overwrite the previous ones,
  except for ATTRIBUTE arguments, which will be gathered to a list.

  :param text: text to be rendered
  :param args: arguments for rendering
  :return: rendered text and raw text
  """
  color, highlight, attributes = None, None, []
  for arg in args:
    if arg in COLORS.keys():
      color = arg
    elif arg in HIGHLIGHTS.keys():
      highlight = arg
    elif arg in ATTRIBUTES.keys() and arg not in attributes:
      attributes.append(arg)
  return colored(text, color, highlight, attributes), text

# endregion: Private Methods

# region: Public Methods

def parse(text, lead='#'):
  """Parse the given text according to the syntax.

  Pattern: lead + r'(\{.+?\})+'
  Here 'lead' is the leading character that can be specified.
  e.g., if 'lead' is set to '#', the pattern will be r'#(\{.+?\})+'

  Example:
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  from termcolor import colored

  rendered, raw = parse('#{Hello}{red}, #{World}{green}!')
  assert raw == 'Hello, World!'
  # The lines below will yield exactly the same outputs
  print(rendered)
  print(colored('Hello', 'red') + ', ' + colored('World', 'green') + '!')
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  :param text: content to be parsed
  :param lead: the leading character for parsing, '#' by default.
               BETTER NOT CHANGE !!
  :return: rendered line for and raw line, see example above
  """
  assert isinstance(text, str) and isinstance(lead, str)
  # Find units to be colored
  pattern = lead + r'(?:\{.+?\})+'
  units = re.findall(pattern, text)
  # Render each unit
  rendered_text, raw_text = text, text
  for unit in units:
    args = re.findall(r'\{(.+?)\}', unit)
    ren, raw = _render(*args)
    # Update rendered and raw text
    rendered_text = rendered_text.replace(unit, ren)
    raw_text = raw_text.replace(unit, raw)

  # Force to display plain text if fancy text is disabled
  if not fancy_text: rendered_text = raw_text
  return rendered_text, raw_text


def write_line(text, color=None, highlight=None, attributes=None, **kwargs):
  """Write a line with fancy style.

  During parsing, changing the leading character is not supported currently.

  :param text: text to be written
  :param color: should be in
        {red, green, yellow, blue, magenta, cyan, white}
  :param highlight: should be in
        {on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white}
  :param attributes: should be a subset of
        {bold, dark, underline, blink, reverse, concealed}
  :param kwargs: additional keyword arguments for python print function
  :return: raw text
  """
  ren, raw = parse(text)
  print(colored(ren, color, highlight, attributes), **kwargs)
  return raw


def write(text, color=None, highlight=None, attributes=None):
  """Write the given text with fancy style.

  During parsing, changing the leading character is not supported currently.

  :param text: text to be written
  :param color: should be in
        {red, green, yellow, blue, magenta, cyan, white}
  :param highlight: should be in
        {on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white}
  :param attributes: should be a subset of
        {bold, dark, underline, blink, reverse, concealed}
  """
  ren, _ = parse(text)
  stdout.write(colored(ren, color, highlight, attributes))
  stdout.flush()


def print_progress(index=None, total=None, start_time=None, progress=None,
                   bar_width=65):
  """Show progress bar.

  This method is inherited from tframe.utils.console.print_progress.
  The line which the cursor in terminal is positioned will be overwritten.

  :param index: positive scalar, indicating current working progress
  :param total: positive scalar, indicating the scale of total work
  :param start_time: if provided, ETA will be displayed to the right of
                      the progress bar
  :param progress: if provided, 'index' and 'total' will be ignored.
  :param bar_width: width of progress bar, 65 by default
  """
  # Calculate progress if not provided
  if progress is None:
    if index is None or total is None:
      raise ValueError(
        'index and total must be given if progress is not provided')
    progress = 1.0 * index / total
  progress = min(progress, 1.0)

  # Generate tail
  if start_time is not None:
    duration = time.time() - start_time
    eta = duration / max(progress, 1e-7) * (1 - progress)
    tail = "ETA: {:.0f}s".format(eta)
  else:
    tail = "{:.0f}%".format(100 * progress)

  # Generate progress bar
  left = int(progress * bar_width)
  right = bar_width - left
  mid = '=' if progress == 1 else '>'
  clear_line()
  stdout.write('[%s%s%s] %s' %
               ('=' * left, mid, ' ' * right, tail))
  stdout.flush()


def clear_line(text_width=79):
  """Clear a line in console."""
  stdout.write("\r{}\r".format(" " * text_width))
  stdout.flush()

# endregion: Public Methods


if __name__ == '__main__':
  # The lines below will yield exactly the same outputs
  print(colored('Hello, World!', 'red', 'on_cyan'))
  write_line('Hello, World!', 'red', 'on_cyan')
  write_line('#{Hello, World!}{red}{on_cyan}')

  # The lines below will yield exactly the same outputs
  print(colored('Hello', 'red') + ', ' + colored('World', 'green') + '!')
  write_line('#{Hello}{red}, #{World}{green}!')
  write('#{Hello}{red}, #{World}{green}!')



