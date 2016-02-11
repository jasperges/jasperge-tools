# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# The 'copy modifier settings' is from an addon by Sergey Sharybin.


bl_info = {
    "name": "jasperge tools",
    "description": "Assorted tools",
    "author": "jasperge",
    "version": (0, 3),
    "blender": (2, 62, 3),
    "location": "View 3D > Toolbar / View 3D - Shift + Q (gives a menu)",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

if "bpy" in locals():
    import imp
    if "jasperge_tools" in locals():
        imp.reload(jasperge_tools)


import bpy
from . import jasperge_tools


jasperge_tools_keymaps = list()


def register():
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.jasperge_tools_settings = bpy.props.PointerProperty(type=jasperge_tools.JaspergeToolsSettings)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:  # don't register keymaps from command line
        km = kc.keymaps.new(name="Window", space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new("wm.call_menu", "Q", "PRESS", shift=True)
        kmi.properties.name = "VIEW3D_MT_jasperge_tools_menu"
        jasperge_tools_keymaps.append(km)
        km = kc.keymaps.new("Timeline", space_type='TIMELINE', region_type='WINDOW')
        kmi = km.keymap_items.new("marker.jaspergetools_snap_to_current_frame", 'S', 'PRESS', shift=True)
        jasperge_tools_keymaps.append(km)
    bpy.app.handlers.load_post.append(jasperge_tools.update_jasperge_settings)
    bpy.types.TIME_MT_marker.append(jasperge_tools.draw_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    wm = bpy.context.window_manager
    for km in jasperge_tools_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del jasperge_tools_keymaps[:]
    del bpy.types.WindowManager.jasperge_tools_settings
    # Remove load_post handler
    for h in bpy.app.handlers.load_post:
        if h.__name__ == "update_jasperge_settings":
            bpy.app.handlers.load_post.remove(h)
    bpy.types.TIME_MT_marker.remove(jasperge_tools.draw_func)


if __name__ == "__main__":
    register()
