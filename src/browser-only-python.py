#!/usr/bin/python
# -*- coding: utf-8 -*-


## Created by Krushn Dayshmookh

## Forked fro PClinuxOS browser

## Here we imported both Gtk library and the WebKit engine.
import gi
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, GObject


class Browser:
    DEFAULT_SITE = "http://woods-os.github.io/fur-box"
    APP_NAME = "Tern"
    DEFAULT_ZOOM = 1.0

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def __init__(self):
        GObject.threads_init()
        self.window = Gtk.Window()
        self.window.set_resizable(True)
        self.window.set_default_size(1100, 950)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        #webkit.WebView allows us to embed a webkit browser
        #it takes care of going backwards/fowards/reloading
        #it even handles flash
        self.web_view = WebKit.WebView()

        #add zoom to right click context menu
        settings = self.web_view.get_settings()
        settings.set_property("enable-developer-extras", True)
        # scale other content besides text as well if set True
        self.web_view.set_full_content_zoom(False)
        # make sure the items will be added in the end
        # hence the reason for the connect_after
        self.web_view.connect_after("populate-popup", self.populate_popup)

        self.web_view.open(self.DEFAULT_SITE)
        self.window.set_title('%s' % self.APP_NAME)
        toolbar = Gtk.Toolbar()

        #create the back button and connect the action to
        #allow us to go backwards using webkit
        self.back_button = Gtk.ToolButton(Gtk.STOCK_GO_BACK)
        self.back_button.connect("clicked", self.go_back)

        #same idea for forward button
        self.forward_button = Gtk.ToolButton(Gtk.STOCK_GO_FORWARD)
        self.forward_button.connect("clicked", self.go_forward)

        #again for refresh
        refresh_button = Gtk.ToolButton(Gtk.STOCK_REFRESH)
        refresh_button.connect("clicked", self.refresh)

        #again for home
        home_button = Gtk.ToolButton(Gtk.STOCK_HOME)
        home_button.connect("clicked", self.go_home)

        #entry bar for typing in and display URLs, when they type in a site
        #and hit enter the on_active function is called
        self.url_bar = Gtk.Entry()
        self.url_bar.connect("activate", self.on_active)
        entry_tool = Gtk.ToolItem()
        entry_tool.set_expand(True)
        entry_tool.add(self.url_bar)
        self.url_bar.show()

        #anytime a site is loaded the update_buttons will be called
        self.web_view.connect("load_committed", self.update_buttons)

        scroll_window = Gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)

        #add the buttons to the toolbar
        toolbar.add(self.back_button)
        toolbar.add(self.forward_button)
        toolbar.add(refresh_button)
        toolbar.add(home_button)
        toolbar.add(entry_tool)


        vbox = Gtk.VBox(False, 0)
        vbox.pack_start(toolbar, False, True, 0)
        vbox.add(scroll_window)

        self.window.add(vbox)
        self.window.show_all()

    def populate_popup(self, view, menu):
        # zoom feature
        zoom_in = Gtk.ImageMenuItem(Gtk.STOCK_ZOOM_IN)
        zoom_in.connect('activate', zoom_in_cb, view)
        menu.append(zoom_in)

        zoom_out = Gtk.ImageMenuItem(Gtk.STOCK_ZOOM_OUT)
        zoom_out.connect('activate', zoom_out_cb, view)
        menu.append(zoom_out)

        menu.show_all()
        return False

    def on_active(self, widget, data=None):
        '''When the user enters an address in the bar, we check to make
           sure they added the http://, if not we add it for them.  Once
           the url is correct, we just ask webkit to open that site.'''
        url = self.url_bar.get_text()
        try:
            url.index("://")
        except:
            url = "http://"+url
        self.url_bar.set_text(url)
        self.web_view.open(url)

    def go_back(self, widget, data=None):
        '''Webkit will remember the links and this will allow us to go
           backwards.'''
        self.web_view.go_back()

    def go_forward(self, widget, data=None):
        '''Webkit will remember the links and this will allow us to go
           forwards.'''
        self.web_view.go_forward()

    def refresh(self, widget, data=None):
        '''Simple makes webkit reload the current back.'''
        self.web_view.reload()

    def go_home(self, widget, data=None):
        '''Returns to default site, Homepage'''
        self.web_view.open(self.DEFAULT_SITE)

    def update_buttons(self, widget, data=None):
        '''Gets the current url entry and puts that into the url bar.
           It then checks to see if we can go back, if we can it makes the
           back button clickable.  Then it does the same for the foward
           button.'''
        self.url_bar.set_text( widget.get_main_frame().get_uri() )
        self.back_button.set_sensitive(self.web_view.can_go_back())
        self.forward_button.set_sensitive(self.web_view.can_go_forward())
        self.web_view.set_zoom_level(self.DEFAULT_ZOOM)

    def main(self):
        Gtk.main()

# context menu item callbacks
def zoom_in_cb(menu_item, web_view):
    """Zoom into the page"""
    web_view.zoom_in()
    Browser.DEFAULT_ZOOM = web_view.get_zoom_level()

def zoom_out_cb(menu_item, web_view):
    """Zoom out of the page"""
    web_view.zoom_out()
    Browser.DEFAULT_ZOOM = web_view.get_zoom_level()

if __name__ == "__main__":
    browser = Browser()
    browser.main()
