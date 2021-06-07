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
# ====-==============================================================-==========
"""A class that provides utilities to show information in terminal.
"""
import logging
import time
import warnings
from . import printer
from functools import wraps


def auto_clear(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    # Get the instance of Console class from args
    self = args[0]
    assert isinstance(self, Console)
    # Clear line if last called function is print_progress
    # Using 'is' instead of '==' does not work
    if self._last_func_called == self.print_progress:
      self.clear_line()
    self._last_func_called = func
    # Print
    return func(*args, **kwargs)
  return wrapper


class Console(object):

  __VERSION__ = (1, 0, 1)

  DEFAULT_TITLE = 'main'
  DEFAULT_PROMPT = '>>'
  INFO_PROMPT = '::'
  SUPPLEMENT_PROMPT = '..'
  WARNING_PROMPT = '!!'
  TEXT_WIDTH = 79

  def __init__(self, buffer_size=0, fancy_text=True):
    """Initiate a console.

    :param buffer_size: buffer size
    :param fancy_text: whether to allow fancy text. Notice that if this value
                       is set to False, all consoles will not be able to produce
                       fancy text.
    """
    # Public variables
    self.buffer_size = buffer_size
    assert isinstance(buffer_size, int) and buffer_size >= 0
    # Turn off fancy text forever if fancy_text is set to False
    if not fancy_text: self.disable_fancy_text()
    # Private variables
    self._buffer = []
    self._title = None
    self._last_func_called = None
    self._tic = None

  # region: Properties

  @property
  def buffer(self):
    return self._buffer

  @property
  def buffer_string(self):
    return '\n'.join(self._buffer)

  # endregion: Properties

  # region: Private Methods

  def _add_to_buffer(self, line):
    assert isinstance(line, str)
    if self.buffer_size == 0: return
    assert self.buffer_size > 0
    self._buffer.append(line)
    if len(self._buffer) > self.buffer_size: self._buffer.pop(0)

  # endregion: Private Methods
  
  # region: Public Methods

  @auto_clear
  def write_line(self, text, color=None, highlight=None, attributes=None,
                 buffer=True, **kwargs):
    """Write a line with fancy style.

    During parsing, changing the leading character is not supported currently.

    :param text: text to be written
    :param color: should be in
          {red, green, yellow, blue, magenta, cyan, white}
    :param highlight: should be in
          {on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white}
    :param attributes: should be a subset of
          {bold, dark, underline, blink, reverse, concealed}
    :param buffer: whether to add text to buffer
    :param kwargs: additional keyword arguments for python print function
    :return: raw text
    """
    text = printer.write_line(text, color, highlight, attributes, **kwargs)
    # Add to buffer if necessary
    if buffer: self._add_to_buffer(text)
    return text


  def write(self, text, color=None, highlight=None, attributes=None):
    """Write the given text with fancy style, as in write_line method.

    During parsing, changing the leading character is not supported currently.
    This method will neither return anything nor add content into buffer.

    :param text: text to be written
    """
    printer.write(text, color, highlight, attributes)


  def split(self, splitter='-', text_width=None, color=None, highlight=None,
            attributes=None):
    """Split terminal with fancy (if style is specified) splitter.

    Example:
      console.split('#{-}{red}#{-}{yellow}#{-}{blue}')
    """
    text_width = text_width or self.TEXT_WIDTH
    # Repeat number should be calculated using raw text
    ren, raw = printer.parse(splitter)
    num = int(text_width / len(raw))
    self.write_line(num * ren, color, highlight, attributes)


  def start(self, title=None, text_width=None, color='grey'):
    """Indicate the start of a program."""
    title = title or self.DEFAULT_TITLE
    text_width = text_width or self.TEXT_WIDTH
    self.write_line('-> Start of {}'.format(title), color)
    self.split(text_width=text_width, color=color)
    self._title = title


  def end(self, text_width=None, color='grey'):
    """Indicate the end of a program."""
    text_width = text_width or self.TEXT_WIDTH
    self.split(text_width=text_width, color=color)
    self.write_line('|> End of {}'.format(self._title), color)


  def section(self, section_title):
    """Indicate the begin of a section."""
    self.split()
    self.write_line(':: {}'.format(section_title))
    self.split()


  @auto_clear
  def show_status(self, text, color=None, highlight=None, attributes=None,
                 prompt=None, buffer=True, **kwargs):
    """Show text following the specified prompt.

    The text will be displayed in a fancy style if corresponding configurations
    are provided, as in self.write_line method.

    :param text: text to be written.
    :param prompt: The leading symbol, usually '>>' by default.
    :param buffer: Whether to add text to buffer
    """
    # Use default prompt symbol if not provided
    if prompt is None: prompt = self.DEFAULT_PROMPT
    # The type of 'text' should not be restricted
    assert isinstance(prompt, str)
    prompt_text = '{} {}'.format(prompt, text)
    # Print using write_line
    return self.write_line(
      prompt_text, color, highlight, attributes, buffer=buffer, **kwargs)


  def show_info(self, text, color=None, highlight=None, attributes=None):
    """Show information using self.show_status"""
    return self.show_status(
      text, color, highlight, attributes, self.INFO_PROMPT)


  def supplement(self, text, color=None, highlight=None, attributes=None,
                 level=1):
    """Show supplement using self.show_status"""
    assert isinstance(level, int) and level > 0
    return self.show_status(
      text, color, highlight, attributes, self.SUPPLEMENT_PROMPT * level)


  def warning(self, text, color='red', highlight=None, attributes=None):
    """Show supplement using self.show_status"""
    return self.show_status(
      text, color, highlight, attributes, self.WARNING_PROMPT)


  def print_progress(self, index=None, total=None, progress=None):
    """Show progress bar using printer.print_progress.

    :param index: positive scalar, indicating current working progress
    :param total: positive scalar, indicating the scale of total work
    :param progress: if provided, 'index' and 'total' will be ignored.
    """
    if index == 0: self._tic = time.time()
    printer.print_progress(index, total, self._tic, progress)
    # This method does not need to be decorated due to the line below
    self._last_func_called = self.print_progress

  # endregion: Public Methods

  # region: Static Methods
  
  @staticmethod
  def fancify(text, *args):
    """Wrap raw text in the format that can be parsed by printer (BETA)"""
    result = '#{' + text + '}'
    for arg in args:
      assert isinstance(arg, str)
      result += '{' + arg + '}'
    return result


  @staticmethod
  def clear_line():
    """Clear a line in which current cursor is positioned."""
    printer.clear_line(Console.TEXT_WIDTH)


  @staticmethod
  def disable_fancy_text():
    """Disable fancy text. Notice that this will disable fancy text for all
       instances of Console.
    """
    printer.fancy_text = False


  @staticmethod
  def disable_future_warnings():
    """Suppress the annoying future warnings for good."""
    warnings.simplefilter(action='ignore', category=FutureWarning)


  @staticmethod
  def disable_logging(pkg_name):
    """Suppress the annoying logging information in terminal.
    :param pkg_name: Name of the package producing the unwanted log.
                     e.g., 'tensorflow'
    """
    assert isinstance(pkg_name, str)
    logging.getLogger(pkg_name).disabled = True

  # endregion: Static Methods



