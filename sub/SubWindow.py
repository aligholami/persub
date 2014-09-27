# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('sub')

from sub_lib import Window
from sub.AboutSubDialog import AboutSubDialog
from sub.PreferencesSubDialog import PreferencesSubDialog

import subprocess
import os
import threading

# See sub_lib.Window.py for more details about how this class works

class SubWindow(Window):
    __gtype_name__ = "SubWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(SubWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutSubDialog
        self.PreferencesDialog = PreferencesSubDialog

        # Code for other initialization actions should be added here.
        
        self.openVideo = self.builder.get_object("openVideo")
        self.openSub = self.builder.get_object("openSub")
        
        self.burn = self.builder.get_object("brun")
        self.convertNburn = self.builder.get_object("convertNburn")
        
        self.fontSize = self.builder.get_object("fontSize")
        self.subFontScale = self.builder.get_object("subFontScale")
        self.subPos = self.builder.get_object("subPos")
        self.bgColor = self.builder.get_object("bgColor")
        self.bgAlpha = self.builder.get_object("bgAlpha")
        
        self.statusBar = self.builder.get_object("statusBar")
        
        self.spinner1 = self.builder.get_object("spinner1")
        self.spinner2 = self.builder.get_object("spinner2")
        
        
        self.scale = 3.0
        self.pos = 95
        self.bg_color = 25
        self.bg_alpha = 50
        self.statusBar.push(1, "Status: Select files")
        self.spinner1.hide()
        self.spinner2.hide()
        
    
    def on_openVideo_file_set(self, widget):
        self.videoInput = widget.get_filename()
        print "Video file Choosen: ", self.videoInput
        
    def on_openSub_file_set(self, widget):
        self.subInput = widget.get_filename()
        print "Subtitle file Choosen: ", self.subInput   

    def on_burn_clicked(self, widget):
        if os.path.exists(self.videoInput) and os.path.exists(self.subInput) :
            self.statusBar.push(1, "Status: Burning subtitle...")
            self.spinner1.show()
        else:
            self.statusBar.push(1, "Status: File doesn't exist")
            
        input_video = self.videoInput
        input_sub = self.subInput
        self.output_video = self.videoOutput = os.path.splitext(self.videoInput)[0] + "_sub.mp4"
        mencoder_command = 'mencoder "%s" -sub "%s" -utf8 -subfont-text-scale "%d" -subpos "%d" -sub-bg-color "%d" -sub-bg-alpha "%d" -o "%s" -oac pcm -ovc lavc' % (input_video, input_sub, self.scale, self.pos, self.bg_color, self.bg_alpha, self.output_video)
        threading.Thread(target=lambda: self._do_subproc(mencoder_command, self.statusBar)).start()
          
    def _do_subproc(self, command, bar):
        print subprocess.call(command,shell=True)
        print subprocess.call('chmod 777 "%s"' % self.output_video,shell=True)
        bar.push(1, "Status: Done!")
        self.spinner1.hide()   
             
    def on_convertNburn_clicked(self, widget):
        self.statusBar.push(1, "Status: Converting video & burning subtitle...")
        self.spinner2.show()
        input_video = self.videoInput
        input_sub = self.subInput
        self.output_video = os.path.splitext(self.videoInput)[0] + ".mp4"
        self.output_video_second = os.path.splitext(self.videoInput)[0] + "_sub.mp4"
        ffmpeg_command = 'ffmpeg -i "%s" -r 24 -strict -2 -y "%s" && mencoder "%s" -sub "%s" -utf8 -subfont-text-scale "%d" -subpos "%d" -sub-bg-color "%d" -sub-bg-alpha "%d" -o "%s" -oac pcm -ovc lavc' % (input_video, self.output_video, self.output_video, input_sub, self.scale, self.pos, self.bg_color, self.bg_alpha, self.output_video_second )
        threading.Thread(target=lambda: self._do_subproc2(ffmpeg_command, self.statusBar)).start()
    
    def _do_subproc2(self, command, bar):
        print subprocess.call(command,shell=True)
        print subprocess.call('chmod 777 "%s" "%s"' % (self.output_video, self.output_video_second),shell=True)
        bar.push(1, "Status: Done!")
        self.spinner2.hide() 

    def on_subFontScale_value_changed(self, SpinButton):
        self.scale = self.subFontScale.get_value()
        
    def on_subPos_value_changed(self, SpinButton):
        self.pos = self.subPos.get_value_as_int()
        
    def on_bgColor_value_changed(self, SpinButton):
        self.bg_color = self.bgColor.get_value_as_int()  
                  
    def on_bgAlpha_value_changed(self, SpinButton):
        self.bg_alpha = self.bgAlpha.get_value_as_int()
